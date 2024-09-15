from django.shortcuts import render, redirect
from .models import PostIt

def guestbook_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            PostIt.objects.create(content=content)  # 새 방명록 항목 생성
            return redirect('guestbook')  # 방명록 페이지로 리디렉션

    postits = PostIt.objects.all().order_by('-created_at')  # 작성된 방명록 목록
    return render(request, 'guestbook/guestbook.html', {'postits': postits})
