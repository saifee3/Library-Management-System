from django.urls import path
from .views import *

# Group URLs by functionality and user roles
urlpatterns = [
    path('auth/register/', register_user),
    path('auth/login/', login_user),
    
    path('search-filter/', book_search,),

    path('authors/create/', author_create), 
    path('authors/', author_list),                                          
    path('authors/<id>/', get_author),                 
    path('authors/<id>/update/', update_author),    
    path('authors/<id>/delete/', delete_author),       
    
    path('books/create/', book_create),
    path('books/borrow/', borrow_book),          
    path('books/return/', return_book),  
    path('books/', book_list),
    path('books/<id>/', get_book),       
    path('books/<id>/update/', update_book),
    path('books/<id>/delete/', delete_book),                               

    path('library/statistics/', library_statistics),
    
    path('borrowers/', borrower_list),     

    
]