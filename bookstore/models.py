from django.db import models
from django.urls import reverse_lazy


class Author(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def get_absolute_url(self):
        return reverse_lazy('bookstore:author_detail', kwargs={'pk': self.pk})


class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Editora'
        verbose_name_plural = 'Editoras'

    def get_absolute_url(self):
        return reverse_lazy('bookstore:publisher_detail', kwargs={'pk': self.pk})


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

    def get_absolute_url(self):
        return reverse_lazy('bookstore:book_detail', kwargs={'pk': self.pk})
