"""
URL configuration for network detection app.
"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'network_detection'

urlpatterns = [
    path('', login_required(views.network_detection_view), name='detection'),
    path('ddos/', login_required(views.ddos_detection_view), name='ddos'),
    path('mitm/', login_required(views.mitm_detection_view), name='mitm'),
    path('threats/', login_required(views.threats_view), name='threats'),
    path('logs/', login_required(views.network_logs_view), name='logs'),
    path('api/detect/', views.DetectionAPIView.as_view(), name='api_detect'),
    path('api/threats/', views.ThreatsAPIView.as_view(), name='api_threats'),
    path('api/logs/', views.NetworkLogsAPIView.as_view(), name='api_logs'),
]
