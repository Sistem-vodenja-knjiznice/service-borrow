from django.urls import path

from .views import BorrowViewSet

urlpatterns = [
    path('borrows', BorrowViewSet.as_view({
        'get': 'list'
    })),
    path('borrows/user/<str:pk>', BorrowViewSet.as_view({
        'get': 'list_by_user'
    })),
    path('borrows/book/<str:pk>', BorrowViewSet.as_view({
        'get': 'list_by_book'
    })),
    path('borrows/overdue', BorrowViewSet.as_view({
        'get': 'list_overdue'
    })),
    path('borrows/borrow', BorrowViewSet.as_view({
        'post': 'create'
    })),
    path('borrows/return', BorrowViewSet.as_view({
        'put': 'return_book',
    })),
    path('borrows/extend', BorrowViewSet.as_view({
        'put': 'extend',
    })),
    path('borrows/health', BorrowViewSet.as_view({
        'get': 'health_check',
    }))
]