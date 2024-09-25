# views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('investment_sessions')  # 로그인 후 이동할 페이지


# 투자 세션 생성 화면
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import InvestmentSession, Idea, User
from .forms import InvestmentSessionForm, IdeaForm

def create_investment_session(request):
    if request.method == 'POST':
        session_form = InvestmentSessionForm(request.POST)
        idea_form = IdeaForm(request.POST)
        
        if session_form.is_valid() and idea_form.is_valid():
            investment_session = session_form.save(commit=False)
            investment_session.created_at = timezone.now()
            investment_session.save()

            idea = idea_form.save(commit=False)
            idea.investment_session = investment_session
            idea.save()
            
            # 사용자에게 돈을 배분하는 로직 (배분할 양을 결정하는 로직을 추가할 수 있습니다)
            selected_user = request.POST.get('selected_user')
            allocated_money = request.POST.get('allocated_money')
            
            # 해당 사용자에게 배분된 돈을 처리하는 로직
            user = User.objects.get(id=selected_user)
            user.accumulated_investment += allocated_money
            user.save()

            return redirect('investment_sessions')  # 세션 목록 페이지로 이동
    else:
        session_form = InvestmentSessionForm()
        idea_form = IdeaForm()

    return render(request, 'create_investment_session.html', {
        'session_form': session_form,
        'idea_form': idea_form,
    })



# 투자 화면
def invest_in_idea(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        idea_id = request.POST.get('idea_id')
        investment_amount = request.POST.get('investment_amount')

        idea = Idea.objects.get(id=idea_id)
        user = request.user

        # 사용자가 총 돈 이내로 투자했는지 확인
        if user.accumulated_investment >= float(investment_amount):
            idea.investment_received += float(investment_amount)
            idea.save()
            
            user.accumulated_investment -= float(investment_amount)
            user.save()

            return redirect('investment_results', session_id=session_id)
        else:
            return render(request, 'investment_failed.html', {'error': '투자 금액이 초과되었습니다.'})
    
    else:
        sessions = InvestmentSession.objects.all()
        return render(request, 'invest_in_idea.html', {'sessions': sessions})



# 투자 결과 확인 화면
from django.db.models import Sum

def investment_results(request, session_id):
    session = InvestmentSession.objects.get(id=session_id)
    ideas = session.ideas.all()
    investment_data = []

    for idea in ideas:
        total_investment = idea.investment_received
        investors = User.objects.filter(idea=idea).order_by('-accumulated_investment')

        investment_data.append({
            'idea': idea,
            'total_investment': total_investment,
            'investors': investors,
        })

    return render(request, 'investment_results.html', {
        'session': session,
        'investment_data': investment_data,
    })



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('investment_sessions')  # 회원가입 후 이동할 페이지
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
