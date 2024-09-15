
from django.urls import path
from myapp import views

urlpatterns = [             
    # path('', views.index),
    # path('create/', views.create),
    # path('read/<id>/', views.read),
    # path('update/<id>/', views.update),
    # path('delete/', views.delete),
    path('', views.home, name='home'),
    path('luck/', views.luck_today, name='luck_today'),
    path('trelawney/', views.trelawney_conversation, name='trelawney_conversation'),  # Trelawney와 대화
    path('hooch/', views.hooch_conversation, name='hooch_conversation'),  # Hooch와 대화
    path('hooch/galaga/', views.galaga_game, name='galaga_game'),  # 비행 슈팅 게임 경로


]
