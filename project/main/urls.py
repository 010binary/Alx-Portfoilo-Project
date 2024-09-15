from django.urls import path
from .views import index, register, login, about

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('about/', about, name='about'),
]
