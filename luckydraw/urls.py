from django.urls import path

from .views import *

urlpatterns = [
    
    path('' , home , name='home'),
    path('winners/' , winnners , name='winners'),
    path('logout/' , logout_view , name='logout')
    
]
