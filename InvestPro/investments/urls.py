from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'custom_users', views.CustomUserViewSet)
router.register(r'investments', views.InvestmentViewSet)
router.register(r'transactions', views.TransactionViewSet)
router.register(r'portfolios', views.PortfolioViewSet)

# The API URLs are determined automatically by the router.
# Additionally, we include the regular views for templates.
urlpatterns = [
    path('api/', include(router.urls)),
    path('home/', views.home, name='home'),
    path('research/', views.research, name='research'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('resources/', views.resources, name='resources'),
]