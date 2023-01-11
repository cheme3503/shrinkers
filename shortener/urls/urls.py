from django.contrib import admin
from django.urls import path
from shortener.urls.views import *
from rest_framework import routers
from shortener.urls.apis import *

router = routers.DefaultRouter()   # router 초기화
router.register(r'urls', UrlListView)  #different view set을 등록
                                        #  첫번째 argument : REST url prefix, 두번째 Argument : vieset

#localhost:8000/api/urls/?

urlpatterns = [
    path('', url_list, name="url_list"),
    path('create', url_create, name='url_create'),
    path('<str:action>/<int:url_id>', url_change, name='url_change'),
]