from django.urls import include, path
from rest_framework import routers

from bookstore.views import AuthorViewSet, BookViewSet, PublisherViewSet

router = routers.DefaultRouter()

router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]