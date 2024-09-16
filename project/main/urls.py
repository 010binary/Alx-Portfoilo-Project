from django.urls import path
from .views import index, register, login, about, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('about/', about, name='about'),
    path('logout/', logout_view, name='logout'),
]
