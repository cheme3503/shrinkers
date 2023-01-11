from shortener.index.views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('',index, name = 'index'),
    path('register/', register, name = 'register'),
    path('login', login_view, name ='login'),
    path('logout', logout_view, name='logout'),
]