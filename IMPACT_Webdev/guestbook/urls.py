from django.urls import path
from .views import guestbook_view

urlpatterns = [
    path('', guestbook_view, name='guestbook'),  # 방명록 메인 페이지
]
