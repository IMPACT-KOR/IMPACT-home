from django.shortcuts import render

# Create your views here.
# invest_app/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
import json, os

from .invest_analysis import parse_investment_file, assign_teams, balance_teams

# 사용자 데이터 불러오기
def load_user_data():
    with open('user_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

USER_DATA = {
    "admin": "admin123",
    "김대성": "990307",
    "홍길동": "750808",
    "서진영": "010910",
    "이도형": "010103",
    "신채범": "010508",
    "구도윤": "000506",
    "권태희": "980617",
    "임관훈": "040617",
    "전해성": "991102",
    "김동우": "000403",
    "오경빈": "001030",
    "김강현": "980413",
    "임도원": "000323",
    "한민우": "000822",
    "문진우": "000605"
}

def home(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 유효성 검사를 수행
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'investment/login.html')
        
        # 사용자 인증
        if username in USER_DATA and USER_DATA[username] == password:
            request.session['username'] = username
            request.session['balance'] = 1000  # 기본 잔액
            request.session['is_admin'] = (username == 'admin')  # 관리자인지 여부 확인
            messages.success(request, f'Welcome, {username}!')  # 로그인 성공 메시지
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    # GET 요청 또는 로그인 실패 시 로그인 페이지 렌더링
    return render(request, 'investment/login.html')

def dashboard(request):
    if 'username' not in request.session:
        return redirect('login')
    
    context = {
        'balance': request.session.get('balance', 1000),
        'error': messages.get_messages(request),
        'is_admin': request.session.get('is_admin', False)
    }
    return render(request, 'investment/dashboard.html', context)

def invest(request):
    if 'username' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        username = request.session['username']
        investee = request.POST['investee']
        amount = int(request.POST['amount'])
        
        if investee not in USER_DATA:
            messages.error(request, '투자할 사용자가 존재하지 않습니다.')
            return redirect('dashboard')
        
        if request.session['balance'] < amount:
            messages.error(request, '잔액이 부족합니다.')
            return redirect('dashboard')

        request.session['balance'] -= amount
        
        log_entry = f"ID: {username}, 투자 대상: {investee}, 투자 금액: {amount}\n"
        with open('investment_log.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)

        messages.success(request, f"{investee}에게 {amount} 포인트를 성공적으로 투자했습니다.")
        return redirect('dashboard')

def view_log(request):
    if 'username' not in request.session or not request.session.get('is_admin', False):
        return redirect('login')

    if os.path.exists('investment_log.txt'):
        with open('investment_log.txt', 'r', encoding='utf-8') as f:
            log_content = f.read()
    else:
        log_content = "No investment log available."
    
    return render(request, 'log.html', {'log_content': log_content})

def clear_log(request):
    if 'username' not in request.session or not request.session.get('is_admin', False):
        return redirect('login')

    open('investment_log.txt', 'w').close()
    messages.success(request, '로그가 초기화되었습니다.')
    return redirect('dashboard')

def assign_teams_view(request):
    if 'username' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        try:
            team_count = int(request.POST['team_count'])
            investment_data = parse_investment_file('investment_log.txt')
            teams = assign_teams(investment_data, team_count)
            balanced_teams = balance_teams(teams)
            return render(request, 'team_assignment.html', {'teams': balanced_teams})
        except Exception as e:
            messages.error(request, str(e))
            return redirect('dashboard')

def logout_view(request):
    request.session.flush()  # 세션 초기화
    return redirect('login')
