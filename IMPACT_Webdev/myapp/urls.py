
from django.urls import path
from myapp import views

urlpatterns = [             
    path('', views.index),
    path('create/', views.create),
    path('read/<id>/', views.read),
    path('update/<id>/', views.update),
    path('delete/', views.delete),
    path('homepage/', views.homepage_view, name='homepage'),
    path('homepage/contact/', views.homepage_contact, name='contact')
]
