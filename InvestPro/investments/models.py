from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Custom User Model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Fix the clashes here
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

# Investment Model
class Investment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)  # e.g., Stocks, Bonds, Real Estate
    risk_level = models.IntegerField()  # e.g., 1 (Low Risk) to 5 (High Risk)

    def __str__(self):
        return self.name

# Portfolio Model
class Portfolio(models.Model):
    user = models.ForeignKey(CustomUser, related_name='portfolios', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

# Transaction Model
class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='transactions', on_delete=models.CASCADE)
    investment = models.ForeignKey(Investment, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES, default='BUY')

    def __str__(self):
        return f"{self.transaction_type} - {self.investment.name}"

# Resources model
class Resource(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title
