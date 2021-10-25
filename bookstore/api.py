from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import Author, Book, Publisher

router = Router()

AuthorSchema = create_schema(Author)
PublisherSchema = create_schema(Publisher)
BookSchema = create_schema(Book, depth=1)


class AuthorSchemaIn(Schema):
    name: str


class PublisherSchemaIn(Schema):
    name: str
    score: int


class BookSchemaIn(Schema):
    name: str
    isbn: str
    rating: float
    publisher_id: int
    price: float
    stock: int
    authors: List[int]


@router.get("/books", response=List[BookSchema])
def list_books(request):
    qs = Book.objects.all()
    return qs


@router.get("/books/{id}", response=BookSchema)
def get_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    return book


@router.post("/books", response={201: BookSchema})
def create_book(request, payload: BookSchemaIn):
    # Get params
    authors = payload.dict().pop('authors')
    publisher_id = payload.dict().pop('publisher_id')

    # Instance models
    # Get publisher
    publisher = get_object_or_404(Publisher, id=publisher_id)

    # Mount dict data
    data = {}
    for k, v in payload.dict().items():
        data[k] = v

    data['publisher'] = publisher
    # Necessário porque é uma lista, mas não pode ser salvo diretamente.
    data.pop('authors', None)

    # Save data
    book = Book.objects.create(**data)

    # Add authors
    for author in authors:
        # Get authors
        author_obj = get_object_or_404(Author, id=author)
        book.authors.add(author_obj)

    return 201, book


@router.put("/books/{id}", response=BookSchema)
def update_book(request, id: int, payload: BookSchemaIn):
    book = get_object_or_404(Book, id=id)
    for attr, value in payload.dict().items():
        if attr != 'authors':
            setattr(book, attr, value)
    book.save()

    authors = payload.dict().pop('authors')

    # Remove all authors
    book.authors.clear()

    # Add authors
    for author in authors:
        # Get authors
        author_obj = get_object_or_404(Author, id=author)
        book.authors.add(author_obj)

    return book


@router.delete("/books/{id}", response={204: None})
def delete_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return 204, None


@router.get("/authors", response=List[AuthorSchema])
def list_authors(request):
    qs = Author.objects.all()
    return qs


@router.get("/authors/{id}", response=AuthorSchema)
def get_author(request, id: int):
    author = get_object_or_404(Author, id=id)
    return author


@router.post("/authors", response={201: AuthorSchema})
def create_author(request, payload: AuthorSchemaIn):
    author = Author.objects.create(**payload.dict())
    return 201, author


@router.put("/authors/{id}", response=AuthorSchema)
def update_author(request, id: int, payload: AuthorSchemaIn):
    author = get_object_or_404(Author, id=id)
    for attr, value in payload.dict().items():
        setattr(author, attr, value)
    author.save()
    return author


@router.delete("/authors/{id}", response={204: None})
def delete_author(request, id: int):
    author = get_object_or_404(Author, id=id)
    author.delete()
    return 204, None


@router.get("/publishers", response=List[PublisherSchema])
def list_publishers(request):
    qs = Publisher.objects.all()
    return qs


@router.get("/publishers/{id}", response=PublisherSchema)
def get_publisher(request, id: int):
    publisher = get_object_or_404(Publisher, id=id)
    return publisher


@router.post("/publishers", response={201: PublisherSchema})
def create_publisher(request, payload: PublisherSchemaIn):
    publisher = Publisher.objects.create(**payload.dict())
    return 201, publisher


@router.put("/publishers/{id}", response=PublisherSchema)
def update_publisher(request, id: int, payload: PublisherSchemaIn):
    publisher = get_object_or_404(Publisher, id=id)
    for attr, value in payload.dict().items():
        setattr(publisher, attr, value)
    publisher.save()
    return publisher


@router.delete("/publishers/{id}", response={204: None})
def delete_publisher(request, id: int):
    publisher = get_object_or_404(Publisher, id=id)
    publisher.delete()
    return 204, None
