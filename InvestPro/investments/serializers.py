from rest_framework import serializers
from .models import CustomUser, Investment, Portfolio, Transaction

# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'date_of_birth', 'profile_picture')

# Investment Serializer
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'

# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Portfolio Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ('id', 'user', 'name', 'description', 'created_at', 'transactions')