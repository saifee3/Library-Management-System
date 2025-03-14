from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import *
from .models import *
from .serializers import *
from .permissions import *
from django.views.decorators.cache import cache_page

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'user': serializer.data, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = RefreshToken.for_user(user)
        user_data = UserRegisterSerializer(user).data
        return Response(  {'message': 'Login successful', 'user_data': user_data, 'token': {  'refresh': str(token),   'access': str(token.access_token),  }},  status=status.HTTP_200_OK )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##############################################################################################################

@api_view(['POST'])
@permission_classes([StaffUser])
def author_create(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Author created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 15) 
def author_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 15) 
def get_author(request, id):
    try:
        author = Author.objects.get(pk=id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([StaffUser])
def update_author(request, id):
    try:
        author = Author.objects.get(pk=id)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Author updated successfully!', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([StaffUser])
def delete_author(request, id):
    try:
        author = Author.objects.get(pk=id)
        author.delete()
        return Response({'message': 'Author deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Author.DoesNotExist:
        return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

##############################################################################################################

@api_view(['POST'])
@permission_classes([StaffUser])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Book created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 15) 
def book_list(request):
    books = Book.objects.select_related('author').all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_book(request, id):
    try:
        book = Book.objects.get(pk=id)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([StaffUser])
def update_book(request, id):
    try:
        book = Book.objects.get(pk=id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Book updated successfully!', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([StaffUser])
def delete_book(request, id):
    try:
        book = Book.objects.get(pk=id)
        book.delete()
        return Response({'message': 'Book deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

##############################################################################################################

@api_view(['POST'])
@permission_classes([RegularUser])  
def borrow_book(request):
        
        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id).first()
        if not book:
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
        return Response({'message': 'Book borrowed successfully',  'book': BookSerializer(book).data  }, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([RegularUser])
def return_book(request):
    book_id = request.data.get('book_id')
    book = Book.objects.get(id=book_id)
    borrower = request.user.borrower
    if book not in borrower.books_borrowed.all():
        return Response({'error': 'You have not borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)
    
    borrower.books_borrowed.remove(book)
    book.available = True
    book.save()
    return Response({ 'message': 'Book returned successfully' }, status=status.HTTP_200_OK)

##############################################################################################################

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 15) 
def book_search(request):
    books = Book.objects.select_related('author').all()
    title_query = request.query_params.get('title', '')
    author_query = request.query_params.get('author', '')
    available_query = request.query_params.get('available')
    
    if title_query:
        books = books.filter(title__icontains=title_query)
    if author_query:
        books = books.filter(author__name__icontains=author_query)
    if available_query:
        books = books.filter(available=available_query.lower() == 'true')
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

##############################################################################################################

@api_view(['GET'])
@permission_classes([StaffUser])
# @cache_page(60 * 15) 
def library_statistics(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available=True).count()
    borrowed_books = total_books - available_books
    total_authors = Author.objects.count()
    total_borrowers = Borrower.objects.count()

    authors = Author.objects.prefetch_related('books').all()
    authors_books = [
        {
            'author': author.name,
            'books': [book.title for book in author.books.all()]
        }
        for author in authors
    ]

    data = {
        'total_books': total_books,
        'available_books': available_books,
        'borrowed_books': borrowed_books,
        'total_authors': total_authors,
        'total_borrowers': total_borrowers,
        'authors_books': authors_books,
    }
    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@cache_page(60 * 15) 
@permission_classes([StaffUser])
def borrower_list(request):
    borrowers = Borrower.objects.select_related('user').prefetch_related('books_borrowed').filter(books_borrowed__isnull=False)
    serializer = BorrowerSerializer(borrowers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)