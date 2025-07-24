from django.shortcuts import render
from django.views.generic import TemplateView

class SubscriptionPageView(TemplateView):
    template_name = 'subscribe.html'