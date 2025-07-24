from django.urls import path
from .views import (HomePageView, post_detail, add_comment,
                    like_post, TermsOfServiceView, PrivacyPolicyView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('post/<slug:slug>/like/', like_post, name='like_post'),
    path('terms-of-service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),

]