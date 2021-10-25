from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.orm import create_schema

from .models import Author, Book, Publisher

router = Router()

BookSchema = create_schema(Book, depth=1)


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
