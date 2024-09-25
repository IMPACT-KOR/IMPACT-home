from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),  # 회원가입 URL 패턴 추가
    path('create_session/', views.create_investment_session, name='create_investment_session'),
    path('invest/', views.invest_in_idea, name='invest_in_idea'),
    path('results/<int:session_id>/', views.investment_results, name='investment_results'),
]
