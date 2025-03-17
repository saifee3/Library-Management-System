from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from .serializers import *
from .permissions import *
from .models import *
from django.utils import timezone


class UserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, action):
        if action == 'register':
            return self.register(request)
        elif action == 'login':
            return self.login(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': serializer.data, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            user_data = UserRegisterSerializer(user).data
            return Response({'message': 'Login successful', 'user_data': user_data, 'token': { 'refresh': str(token), 'access': str(token.access_token), }  }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
############################################################################################################################################

class AuthorAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [StaffUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Author created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                author = Author.objects.get(pk=id)
                serializer = AuthorSerializer(author)
                return Response(serializer.data)
            except Author.DoesNotExist:
                return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cached_data = cache.get('author_list')
            if cached_data:
                return Response(cached_data)
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            response_data = serializer.data
            cache.set('author_list', response_data, 60*15)
            return Response(response_data)

    def put(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            serializer = AuthorSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Author updated successfully!', 'data': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            author.delete()
            return Response({'message': 'Author deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

############################################################################################################################################

class BookAPIView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            self.permission_classes = [StaffUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Book created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                book = Book.objects.get(pk=id)
                serializer = BookSerializer(book)
                return Response(serializer.data)
            except Book.DoesNotExist:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cached_data = cache.get('book_list')
            if cached_data:
                return Response(cached_data)
                
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            response_data = serializer.data
            cache.set('book_list', response_data, 60*15)
            return Response(response_data)

    def put(self, request, id):
        try:
            book = Book.objects.get(pk=id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Book updated successfully!', 'data': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return Response({'message': 'Book deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

############################################################################################################################################

class BorrowReturnBookAPIView(APIView):
    permission_classes = [RegularUser]
    def post(self, request, action):
        if action == 'borrow':
            return self.borrow(request)
        elif action == 'return':
            return self.return_book(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    def borrow(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if not book.available:
            return Response({'error': 'This book is not available for borrowing'}, status=status.HTTP_400_BAD_REQUEST)
        borrower = request.user.borrower
        if borrower.books_borrowed.count() >= 3:
            return Response({'error': 'You cannot borrow more than 3 books at a time'}, status=status.HTTP_400_BAD_REQUEST)
        borrower.books_borrowed.add(book)
        book.available = False
        book.last_borrowed_date = timezone.now()
        book.save()
        return Response({'message': 'Book borrowed successfully', 'book': BookSerializer(book).data}, status=status.HTTP_200_OK)

    def return_book(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        borrower = request.user.borrower
        if book not in borrower.books_borrowed.all():
            return Response({'error': 'You have not borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)
        borrower.books_borrowed.remove(book)
        book.available = True
        book.save()
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

############################################################################################################################################

class LibraryAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            if self.kwargs['action'] in ['statistics', 'borrowers']:
                self.permission_classes = [StaffUser]
            else:
                self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get(self, request, action):
        if action == 'search':
            return self.search_books(request)
        elif action == 'statistics':
            return self.library_statistics(request)
        elif action == 'borrowers':
            return self.borrower_list(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
#Search, Filter Books
    def search_books(self, request):
        query_params = request.query_params
        cache_key = f'book_search_{query_params}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        books = Book.objects.all()
        
        title_query = request.query_params.get('title', '')
        if title_query:
            books = books.filter(title__icontains=title_query) 
        author_query = request.query_params.get('author', '')
        if author_query:
            books = books.filter(author__name__icontains=author_query)  
        available_query = request.query_params.get('available')
        if available_query:
            books = books.filter(available=(available_query.lower() == 'true'))
            
        serializer = BookSerializer(books, many=True)
        response_data = serializer.data
        cache.set(cache_key, response_data, 60*15)
        return Response(response_data)
    
#Library Statistics
    def library_statistics(self, request):
        cached_data = cache.get('library_statistics')
        if cached_data:
            return Response(cached_data)
            
        total_books = Book.objects.count()
        available_books = Book.objects.filter(available=True).count()
        borrowed_books = total_books - available_books
        total_authors = Author.objects.count()
        total_borrowers = Borrower.objects.count()
        
        data = {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_authors': total_authors,
            'total_borrowers': total_borrowers,
        }
        cache.set('library_statistics', data, 60*15)
        return Response(data)
    
# Borrower List
    def borrower_list(self, request):
        cached_data = cache.get('borrower_list')
        if cached_data:
            return Response(cached_data)
            
        borrowers = Borrower.objects.filter(books_borrowed__isnull=False).distinct()
        serializer = BorrowerSerializer(borrowers, many=True)
        response_data = serializer.data
        cache.set('borrower_list', response_data, 60*15)
        return Response(response_data)
