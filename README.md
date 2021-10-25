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


> Editar `settings.py`

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
    ...
    # 3rd apps
    'dr_scaffold',
    'rest_framework',
    'django_extensions',
    'django_seed',
    # my apps
    'bookstore',
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')
```

```
# Link contrib
python contrib/env_gen.py
```


> Editar `models.py`

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

> Abrir `shell_plus`

`python manage.py shell_plus`


```python
import string
from random import choice, random, randint
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


> Crie uma pasta `api` e mova `serializers.py` e `viewsets.py` para lá.


```
cd bookstore
mkdir api_v1
mv serializers.py api_v1
mv views.py api_v1/viewsets.py
cd ..
```


> Editar `backend/urls.py`

> Editar `bookstore/urls.py`

> Editar `bookstore/api/viewsets.py`

```python
from bookstore.api_v1.serializers import ...
```

> Editar `bookstore/serializers.py`



## Django Ninja

```
pip install django-ninja

pip freeze | grep django-ninja >> requirements.txt
```

```
touch backend/api.py
touch bookstore/api.py
```


> editar primeiro books
> depois authors, publishers


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