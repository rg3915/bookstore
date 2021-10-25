# Bookstore

Exemplo de biblioteca feito com Django.


## Este projeto foi feito com:

* [Python 3.9.7](https://www.python.org/)
* [Django 3.2.8](https://www.djangoproject.com/)
* [Django Rest Framework 3.12.4](https://www.django-rest-framework.org/)
* [Bootstrap 4.0](https://getbootstrap.com/)
* [VueJS 2.6.11](https://vuejs.org/)
* [jQuery 3.4.1](https://jquery.com/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/bookstore.git
cd bookstore
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

# Passo a passo

## Criando virtualenv

```
python -m venv .venv
source .venv/bin/activate
```


## Instalando os pacotes

```
pip install dr_scaffold djangorestframework

pip freeze | grep 'Django\|djangorestframework\|dr-scaffold' >> requirements.txt
```


```
pip install django-extensions python-decouple django-seed

pip freeze | grep 'django-extensions\|python-decouple\|django-seed\|faker' >> requirements.txt
```

## Criando o projeto

`django-admin startproject backend .`

> Editar `settings.py` e incluir `dr_scaffold` em `INSTALLED_APPS`.

```python
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd apps
    'dr_scaffold',
    'rest_framework',
    'django_extensions',
    'django_seed',
    # my apps
]


LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
```

#### contrib

https://github.com/rg3915/bookstore/blob/main/contrib/env_gen.py

```
mkdir contrib
touch contrib/env_gen.py
python contrib/env_gen.py
```


```
python manage.py dr_scaffold bookstore Author name:charfield

python manage.py dr_scaffold bookstore Publisher name:charfield score:positiveintegerfield

python manage.py dr_scaffold bookstore Book \
name:charfield \
isbn:charfield \
rating:decimalfield \
authors:manytomany:Author \
publisher:foreignkey:Publisher \
price:decimalfield \
stock:integerfield
```


> Editar `models.py`

```python
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'


class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.0)
    stock = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

```

#### Rode as migrações

> Adicione `bookstore` em `INSTALLED_APPS`.

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


```
python manage.py seed bookstore --number=160
```


```
pip install psycopg2-binary

pip freeze | grep psycopg2-binary >> requirements.txt
```


```
python manage.py runserver
```


> Editar `admin.py`

```python
from django.contrib import admin

from bookstore.models import Author, Book, Publisher


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'score')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'isbn', 'rating', 'price', 'stock')
    search_fields = ('name', 'isbn', 'authors__name', 'publisher__name')

```

> Abrir `shell_plus`

`python manage.py shell_plus`


```python
import string
from random import choice, randint, random

from faker import Faker

faker = Faker('pt-br')

def gen_digits(max_length):
    return str(''.join(choice(string.digits) for i in range(max_length)))

def gen_rating():
    return random() + choice((3, 4))

def gen_price():
    return random() + randint(10, 100)

def gen_name():
    return faker.name()

books = Book.objects.all()
for book in books:
    book.isbn = '978' + gen_digits(10)
    book.rating = gen_rating()
    book.price = gen_price()

Book.objects.bulk_update(books, ['isbn', 'rating', 'price'])

authors = Author.objects.all()
for _ in authors:
    Author.objects.update_or_create(name=gen_name())
```


> Crie uma pasta `api_drf` e mova `serializers.py` e `viewsets.py` para lá.


```
cd bookstore
mkdir api_drf
mv serializers.py api_drf
mv views.py api_drf/viewsets.py
cd ..
```


> Editar `backend/urls.py`

```python
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('bookstore.urls', namespace='bookstore')),
    path('admin/', admin.site.urls),
]
```

> Editar `bookstore/urls.py`

```python
from bookstore.api_drf.viewsets import AuthorViewSet, BookViewSet, PublisherViewSet

app_name = 'bookstore'

urlpatterns = [
    path('api/v1/bookstore/', include(router.urls)),
]
```

> Editar `bookstore/api/viewsets.py`

```python
from bookstore.api_drf.serializers import ...

```

> Editar `bookstore/serializers.py`

```python
from rest_framework import serializers

from bookstore.models import Author, Book, Publisher


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = '__all__'

```

## Django Ninja

```
pip install django-ninja

pip freeze | grep django-ninja >> requirements.txt
```

```
touch backend/api.py
touch bookstore/api.py
```

> Editar `backend/api.py`

```python
from ninja import NinjaAPI

from bookstore.api import router as bookstore_router

api = NinjaAPI()

api.add_router('/bookstore/', bookstore_router)

```

> Editar `bookstore/api.py` primeiro `books`

```python
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

```

> depois `authors, publishers`

```python
AuthorSchema = create_schema(Author)
PublisherSchema = create_schema(Publisher)


class AuthorSchemaIn(Schema):
    name: str


class PublisherSchemaIn(Schema):
    name: str
    score: int

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

```

> Editar `backend/urls.py`

```python
from .api import api

    ...
    path('api/v2/', api.urls),
    ...

```


## Templates

```
python manage.py startapp core
rm -f core/{admin,models,tests}.py
rm -rf core/migrations
touch core/urls.py
```


> Editar `settings.py`

```python
INSTALLED_APPS = [
    ...
    'core',
    ...
```
> Editar `backend/urls.py`

```python
path('', include('core.urls')),
```

> Editar `core/urls.py`
> Editar `core/views.py`

```
mkdir -p core/static/css
touch core/static/css/style.css

mkdir -p core/templates/includes
touch core/templates/{base,index}.html
touch core/templates/includes/{nav,pagination}.html
# copiar o conteúdo

mkdir -p bookstore/templates/bookstore
touch bookstore/templates/bookstore/{book,author,publisher}_{list,detail,form,confirm_delete}.html
```


> Editar `bookstore/urls.py`
> Editar `bookstore/views.py`
> Editar `bookstore/forms.py`
> Editar `bookstore/models.py`

> Editar os templates



---

Vídeos no meu canal

* [A Essência do Django](https://youtu.be/mlaCLGItR7Q)
* [Introdução a Arquitetura do Django - Pyjamas 2019](https://youtu.be/XjXpwZhOKOs)
* [VueJS + Django Ninja](https://youtu.be/cZ7n3HN9MiU)
