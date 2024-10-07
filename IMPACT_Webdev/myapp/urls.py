
from django.urls import path
from myapp import views

urlpatterns = [             
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read),
    path('update/<id>/', views.update),
    path('delete/', views.delete),
    path('homepage/', views.homepage_view, name='homepage'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),  # 리더보드 페이지로 연결
    path('challenge-info/', views.challenge_info, name='challenge_info'),  # Challenge Information 페이지
]
