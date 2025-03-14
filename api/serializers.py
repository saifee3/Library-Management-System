from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import *
from django.contrib.auth import authenticate

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'author', 'author_name', 'published_date', 'available', 'last_borrowed_date']
    
    def validate_isbn(self, value):
        isbn_digits = re.sub(r'[^0-9X]', '', value.upper())
        if len(isbn_digits) != 13:
            raise ValidationError("ISBN must be 13 characters long.")
        return isbn_digits  


class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    books_borrowed = BookSerializer(many=True)
    class Meta:
        model = Borrower
        fields = ['id', 'username', 'books_borrowed']
      

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, data):
        user = authenticate(**data)
        return {'user': user}
