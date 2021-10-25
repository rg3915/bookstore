from django.contrib import admin
from django.urls import include, path

from .api import api


urlpatterns = [
    path('', include('core.urls')),
    path('', include('bookstore.urls', namespace='bookstore')),
    path('api/v2/', api.urls),
    path('admin/', admin.site.urls),
]
