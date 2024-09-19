from django.urls import path
from .views import index, register, login, about, logout_view, profile, vote_rules, success_vote, steps, update_profile, competition_view, competition_detail_view

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('about/', about, name='about'),
    path('logout/', logout_view, name='logout'),
    path('steps/', steps, name='steps'),
    path('vote/', vote_rules, name='vote'),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('successvote/', success_vote, name='successful vote'),
    path('vote/competitions/', competition_view, name='competition_view'),
    path('competition/<int:id>/', competition_detail_view, name='competition_detail'),
]
