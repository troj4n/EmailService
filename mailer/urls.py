from django.conf.urls import url
from django.urls import path,re_path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),

]