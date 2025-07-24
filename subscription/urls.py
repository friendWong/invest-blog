from django.urls import path
from .views import SubscriptionPageView

urlpatterns = [
    path('subscribe/', SubscriptionPageView.as_view(), name='subscribe'),
]