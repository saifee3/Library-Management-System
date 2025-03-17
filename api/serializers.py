from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Author, Book, Borrower
import re

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Book
        fields = '__all__'
    def validate_isbn(self, value):
        isbn_digits = re.sub(r'[^0-9X]', '', value.upper())
        if len(isbn_digits) != 13:
            raise ValidationError("ISBN must be 13 characters long.")
        return isbn_digits  

class BorrowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    # books_borrowed = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    class Meta:
        model = Borrower
        fields = '__all__'

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
