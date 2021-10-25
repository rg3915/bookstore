from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response

from bookstore.models import Author, Book, Publisher
from bookstore.serializers import (
    AuthorSerializer,
    BookSerializer,
    PublisherSerializer
)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

