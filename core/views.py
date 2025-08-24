from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import Group

# Create your views here.
class HomeView (TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name=group.name
        context['group_name']= group_name   
        
        return context
    
class PricingView(TemplateView):
    template_name = 'pricing.html'    