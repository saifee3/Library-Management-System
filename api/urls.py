from django.urls import path
from .views import   AuthorAPIView, BookAPIView, BorrowReturnBookAPIView, LibraryAPIView, UserAPIView

urlpatterns = [
    path('user/<action>/', UserAPIView.as_view()),
    path('authors/<id>/', AuthorAPIView.as_view()),
    path('books/<id>/', BookAPIView.as_view()),
    path('borrowing/<action>/', BorrowReturnBookAPIView.as_view()),
    path('library/<action>/', LibraryAPIView.as_view()),
]
