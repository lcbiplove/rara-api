from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    # path('.well-known/jwks.json', include('core.urls')),
]
