# invest_project/urls.py

from django.contrib import admin
from django.urls import path
from investment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('invest/', views.invest, name='invest'),
    path('log/', views.view_log, name='log'),
    path('clear_log/', views.clear_log, name='clear_log'),
    path('assign_teams/', views.assign_teams_view, name='assign_teams'),
    path('logout/', views.logout_view, name='logout'),
]
