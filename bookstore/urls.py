from django.urls import include, path
from rest_framework import routers

from bookstore.api_drf.viewsets import AuthorViewSet, BookViewSet, PublisherViewSet

app_name = 'bookstore'

router = routers.DefaultRouter()

router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/v1/bookstore/', include(router.urls)),
]
