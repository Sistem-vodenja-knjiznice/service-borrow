from rest_framework import viewsets, status
from rest_framework.response import Response

from datetime import timedelta

from .models import Borrow
from .serializers import BorrowSerializer, BorrowRequestSerializer

class BorrowViewSet(viewsets.ViewSet):
    def list_by_user(self, request, pk=None):
        borrows = Borrow.objects.filter(user_id=pk)
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    def list_by_book(self, request, pk=None):
        borrows = Borrow.objects.filter(book_id=pk)
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    def list_overdue(self, request):
        borrows = Borrow.objects.filter(status='overdue')
        serializer = BorrowSerializer(borrows, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        book_id = serializer.validated_data['book_id']

        if Borrow.objects.filter(user_id=user_id, book_id=book_id).exists():
            return Response({'error': 'User already borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)

        borrow = serializer.save()
        borrow.due_date = borrow.borrow_date + timedelta(days=30)
        borrow.save()

        serializer = BorrowSerializer(borrow)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def return_book(self, request):
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

        borrow.status = 'returned'
        borrow.save()

        return Response(status=status.HTTP_202_ACCEPTED)

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
