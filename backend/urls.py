from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('bookstore.urls', namespace='bookstore')),
    path('admin/', admin.site.urls),
]
