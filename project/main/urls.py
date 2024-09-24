from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
    path('steps/', views.steps, name='steps'),
    path('vote/', views.vote_rules, name='vote'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('successvote/', views.success_vote, name='success_vote'),
    path('competitions/', views.competition_view, name='competition_view'),
    path('competition/<int:id>/', views.competition_detail_view,
         name='competition_detail'),
    path('vote/<int:competition_id>/<int:candidate_id>/', views.vote, name='vote'),
    path('competitions/closed/', views.closed_competitions,
         name='closed_competitions'),
    path('competition/ranking/<int:competition_id>/',
         views.competition_ranking, name='competition_ranking'),
    path('api/competitions/', views.get_competition_list, name='competition_list'),
    path('api/competitions/ranking/<int:competition_id>/',
         views.get_competition_ranking, name='competition_list'),
    path('api/competitions/result/<int:competition_id>/',
         views.get_competition_result, name='competition_list'),
]
