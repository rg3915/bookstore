from django.urls import include, path
from rest_framework import routers

from bookstore import views as v
from bookstore.api_drf.viewsets import (
    AuthorViewSet,
    BookViewSet,
    PublisherViewSet
)

app_name = 'bookstore'

router = routers.DefaultRouter()

router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

authors_urlpatterns = [
    path('', v.AuthorListView.as_view(), name='author_list'),
    path('<int:pk>/', v.AuthorDetailView.as_view(), name='author_detail'),
    path('create/', v.AuthorCreateView.as_view(), name='author_create'),
    path('<int:pk>/update/', v.AuthorUpdateView.as_view(), name='author_update'),
    path('<int:pk>/delete/', v.AuthorDeleteView.as_view(), name='author_delete'),
]

publishers_urlpatterns = [
    path('', v.PublisherListView.as_view(), name='publisher_list'),
    path('<int:pk>/', v.PublisherDetailView.as_view(), name='publisher_detail'),
    path('create/', v.PublisherCreateView.as_view(), name='publisher_create'),
    path('<int:pk>/update/', v.PublisherUpdateView.as_view(), name='publisher_update'),
    path('<int:pk>/delete/', v.PublisherDeleteView.as_view(), name='publisher_delete'),
]

books_urlpatterns = [
    path('', v.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', v.BookDetailView.as_view(), name='book_detail'),
    path('create/', v.BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/update/', v.BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', v.BookDeleteView.as_view(), name='book_delete'),
]

urlpatterns = [
    path('api/v1/bookstore/', include(router.urls)),
    path('author/', include(authors_urlpatterns)),
    path('publisher/', include(publishers_urlpatterns)),
    path('book/', include(books_urlpatterns)),
]
