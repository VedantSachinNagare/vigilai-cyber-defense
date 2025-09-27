"""
URL configuration for email classifier app.
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'email_classifier'

urlpatterns = [
    path('', login_required(views.email_classifier_view), name='classifier'),
    path('classify/', login_required(views.classify_email), name='classify'),
    path('history/', login_required(views.classification_history), name='history'),
    path('api/classify/', views.ClassifyEmailAPIView.as_view(), name='api_classify'),
    path('api/history/', views.ClassificationHistoryAPIView.as_view(), name='api_history'),
]
