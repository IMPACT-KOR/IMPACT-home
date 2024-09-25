# views 에 필요한 화면 구성


from django import forms
from .models import InvestmentSession, Idea

class InvestmentSessionForm(forms.ModelForm):
    class Meta:
        model = InvestmentSession
        fields = ['session_name']

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'user']
