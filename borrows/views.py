from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from datetime import timedelta

from .models import Borrow
from .serializers import BorrowSerializer, BorrowRequestSerializer
from .producer import publish
from client import check_book_availability

@extend_schema_view(
    list=extend_schema(
        summary="List all borrows",
        description="Returns a list of all borrows.",
        responses=BorrowSerializer,
    ),
    list_by_user=extend_schema(
        summary="List all borrows by user",
        description="Returns a list of all borrows by user.",
        responses=BorrowSerializer,
    ),
    list_by_book=extend_schema(
        summary="List all borrows by book",
        description="Returns a list of all borrows by book.",
        responses=BorrowSerializer,
    ),
    list_overdue=extend_schema(
        summary="List all overdue borrows",
        description="Returns a list of all overdue borrows.",
        responses=BorrowSerializer,
    ),
    create=extend_schema(
        summary="Borrow a book",
        description="Borrows a book. A user can borrow a book only once .The due date is 30 days from the borrow date."
                    "Sends a message to the book service to decrement the book's stock.",
        request=BorrowRequestSerializer,
        responses=BorrowSerializer,
    ),
    return_book=extend_schema(
        summary="Return a book",
        description="Returns a book. A user can return a book only once. Sends a message to the book service to "
                    "increment the book's stock",
        request=BorrowRequestSerializer,
    ),
    extend=extend_schema(
        summary="Extend a book",
        description="Extends a book. A user can extend a book only once. An extended book is due 14 days from the "
                    "extension date.",
        request=BorrowRequestSerializer,
    ),
)
class BorrowViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['get'])
    def list(self, request):
        borrows = Borrow.objects.all()
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def list_by_user(self, request, pk=None):
        borrows = Borrow.objects.filter(user_id=pk)
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def list_by_book(self, request, pk=None):
        borrows = Borrow.objects.filter(book_id=pk)
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_overdue(self, request):
        borrows = Borrow.objects.filter(status='overdue')
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        book_id = serializer.validated_data['book_id']

        is_available = check_book_availability(book_id)
        if not is_available:
            return Response({'error': 'No more books available'}, status=status.HTTP_400_BAD_REQUEST)

        if Borrow.objects.filter(user_id=user_id, book_id=book_id).exclude(status='returned').exists():
            return Response({'error': 'User already borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)

        borrow = serializer.save()
        borrow.due_date = borrow.borrow_date + timedelta(days=30)
        borrow.save()

        publish('book_borrowed', book_id)

        serializer = BorrowSerializer(borrow)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def return_book(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        book_id = serializer.validated_data['book_id']

        try:
            borrow = Borrow.objects.exclude(status='returned').get(user_id=user_id, book_id=book_id)
        except Borrow.DoesNotExist:
            return Response({'error': 'User did not borrow this book'}, status=status.HTTP_400_BAD_REQUEST)

        if borrow.status == 'returned':
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

        borrow.status = 'returned'
        borrow.save()

        publish('book_returned', book_id)

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['put'])
    def extend(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        book_id = serializer.validated_data['book_id']

        try:
            borrow = Borrow.objects.get(user_id=user_id, book_id=book_id)
        except Borrow.DoesNotExist:
            return Response({'error': 'User did not borrow this book'}, status=status.HTTP_400_BAD_REQUEST)

        if borrow.status == 'returned':
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

        borrow.status = 'extended'
        borrow.due_date = borrow.due_date + timedelta(days=14)
        borrow.save()

        return Response(status=status.HTTP_202_ACCEPTED)
