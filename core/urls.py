
from django.urls import path
from .views import HomeView, PricingView, RegisterView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path ('register/', RegisterView.as_view(), name='register'),
]
