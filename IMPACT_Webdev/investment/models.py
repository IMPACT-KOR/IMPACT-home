from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    accumulated_investment = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # 누적 투자받은 금액
    total_rounds_participated = models.IntegerField(default=0)  # 총 투자 라운드 참여 횟수
    first_place_count = models.IntegerField(default=0)  # 1등 선정된 횟수

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='investment_user_groups',  # related_name을 변경하여 충돌 방지
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='investment_user_permissions',  # related_name을 변경하여 충돌 방지
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username


# 투자 은행 모델
class InvestmentBank(models.Model):
    total_currency_issued = models.DecimalField(max_digits=12, decimal_places=2)  # 총 발행된 화폐 양
    total_investment_rounds = models.IntegerField()  # 투자 라운드 진행 횟수

    def __str__(self):
        return f"Investment Bank - {self.id}"

# 투자 세션 모델
class InvestmentSession(models.Model):
    session_name = models.CharField(max_length=255)  # 투자 세션 이름
    created_at = models.DateTimeField(default=timezone.now)  # 생성된 날짜 및 시간
    ideas = models.ManyToManyField('Idea', related_name='investment_sessions')  # 생성된 아이디어

    def __str__(self):
        return self.session_name

# 아이디어 모델
class Idea(models.Model):
    title = models.CharField(max_length=255)  # 아이디어 제목
    description = models.TextField()  # 아이디어 설명
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 아이디어 제시한 사용자
    investment_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # 투자받은 금액
    investment_session = models.ForeignKey(InvestmentSession, on_delete=models.CASCADE, null=True, blank=True)  # 투자 세션

    def __str__(self):
        return self.title
