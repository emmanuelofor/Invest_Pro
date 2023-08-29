# investpro_app/forms.py

from django import forms
from .models import Investment, UserPortfolio, Resource

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['name', 'type', 'description', 'risk_level']

class UserPortfolioForm(forms.ModelForm):
    class Meta:
        model = UserPortfolio
        fields = ['investment', 'amount']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'content', 'link']