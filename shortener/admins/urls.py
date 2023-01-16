from django.urls import path
from .views import url_list
from shortener.forms import UrlCreateForm
from django.contrib import admin
from rest_framework import routers
from shortener.urls.apis import *


urlpatterns = [
    path('',url_list, name='admin_url_list'),
]