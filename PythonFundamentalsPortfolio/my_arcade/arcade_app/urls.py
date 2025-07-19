# arcade_app/urls.py

from django.urls import path

from . import views

app_name = 'arcade_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('play_game/', views.play_game, name='play_game'),
    path('get_high_scores/', views.get_high_scores, name='get_high_scores'),
    path('save_high_score/', views.save_high_score, name='save_high_score'),
]
