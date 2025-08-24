
from django.urls import path
from .views import HomeView, PricingView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing')
]
