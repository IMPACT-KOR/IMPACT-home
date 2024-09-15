from django.db import models

class PostIt(models.Model):
    content = models.TextField()  # 방명록 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 날짜

    def __str__(self):
        return self.content[:20]  # 방명록 내용의 앞 20자를 표시
