"""
URL configuration for dashboard app.
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', login_required(views.dashboard_view), name='dashboard'),
    path('analytics/', login_required(views.analytics_view), name='analytics'),
    path('reports/', login_required(views.reports_view), name='reports'),
    path('settings/', login_required(views.settings_view), name='settings'),
    path('api/stats/', views.DashboardStatsAPIView.as_view(), name='api_stats'),
    path('api/alerts/', views.AlertsAPIView.as_view(), name='api_alerts'),
]
