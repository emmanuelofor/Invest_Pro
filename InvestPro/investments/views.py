from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status, permissions 
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .models import CustomUser, Investment, Portfolio, Transaction
from .serializers import CustomUserSerializer, InvestmentSerializer, PortfolioSerializer, TransactionSerializer

# Custom User ViewSet
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Investment ViewSet
class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

# Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Portfolio ViewSet
class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    # Overriding the create method to include transactions
    def create(self, request, *args, **kwargs):
        transactions_data = request.data.pop('transactions')
        portfolio = Portfolio.objects.create(**request.data)
        for transaction_data in transactions_data:
            Transaction.objects.create(portfolio=portfolio, **transaction_data)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Home View
def home(request):
    return render(request, 'home.html')

# Investment Research View
def research(request):
    # You could populate this view dynamically with context data from your models
    return render(request, 'research.html')

# Portfolio Management View
def portfolio(request):
    # You could populate this view dynamically with context data from your models
    return render(request, 'portfolio.html')

# Educational Resources View
def resources(request):
    # You could populate this view dynamically with context data from your models
    return render(request, 'resources.html')
