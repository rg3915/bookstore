from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)

from .forms import AuthorForm, BookForm, PublisherForm
from .models import Author, Book, Publisher


class AuthorListView(ListView):
    model = Author
    paginate_by = 20


class AuthorDetailView(DetailView):
    model = Author


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('bookstore:author_list')


class PublisherListView(ListView):
    model = Publisher
    paginate_by = 20


class PublisherDetailView(DetailView):
    model = Publisher


class PublisherCreateView(CreateView):
    model = Publisher
    form_class = PublisherForm


class PublisherUpdateView(UpdateView):
    model = Publisher
    form_class = PublisherForm


class PublisherDeleteView(DeleteView):
    model = Publisher
    success_url = reverse_lazy('bookstore:publisher_list')


class BookListView(ListView):
    model = Book
    paginate_by = 20


class BookDetailView(DetailView):
    model = Book


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('bookstore:book_list')
