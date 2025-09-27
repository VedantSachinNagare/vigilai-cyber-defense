"""
Views for dashboard functionality.
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from email_classifier.models import EmailClassification
from network_detection.models import NetworkThreat, DDoSAttack, MITMAttack, NetworkLog

logger = logging.getLogger('vigilai')


@login_required
def dashboard_view(request):
    """
    Main dashboard view.
    """
    # Get statistics for the last 24 hours
    now = timezone.now()
    yesterday = now - timedelta(days=1)
    
    # Email classification stats
    email_classifications = EmailClassification.objects.filter(
        user=request.user,
        created_at__gte=yesterday
    )
    
    email_stats = {
        'total': email_classifications.count(),
        'legitimate': email_classifications.filter(classification='legitimate').count(),
        'spam': email_classifications.filter(classification='spam').count(),
        'phishing': email_classifications.filter(classification='phishing').count(),
    }
    
    # Network threat stats
    network_threats = NetworkThreat.objects.filter(
        user=request.user,
        created_at__gte=yesterday
    )
    
    ddos_attacks = DDoSAttack.objects.filter(
        user=request.user,
        created_at__gte=yesterday
    )
    
    mitm_attacks = MITMAttack.objects.filter(
        user=request.user,
        created_at__gte=yesterday
    )
    
    network_stats = {
        'total_threats': network_threats.count(),
        'active_threats': network_threats.filter(is_active=True).count(),
        'ddos_attacks': ddos_attacks.count(),
        'mitm_attacks': mitm_attacks.count(),
        'high_severity': network_threats.filter(severity='high').count() + 
                        ddos_attacks.filter(severity='high').count() + 
                        mitm_attacks.filter(severity='high').count(),
    }
    
    # Recent activity
    recent_classifications = email_classifications.order_by('-created_at')[:5]
    recent_threats = network_threats.order_by('-created_at')[:5]
    
    # System health
    system_health = {
        'email_classifier_status': 'operational',
        'ddos_detector_status': 'operational',
        'mitm_detector_status': 'operational',
        'database_status': 'operational',
    }
    
    context = {
        'email_stats': email_stats,
        'network_stats': network_stats,
        'recent_classifications': recent_classifications,
        'recent_threats': recent_threats,
        'system_health': system_health,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def analytics_view(request):
    """
    Analytics and reporting view.
    """
    # Get data for the last 7 days
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    
    # Email classification trends
    email_trends = []
    for i in range(7):
        date = now - timedelta(days=i)
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        day_classifications = EmailClassification.objects.filter(
            user=request.user,
            created_at__gte=start_date,
            created_at__lt=end_date
        )
        
        email_trends.append({
            'date': start_date.strftime('%Y-%m-%d'),
            'legitimate': day_classifications.filter(classification='legitimate').count(),
            'spam': day_classifications.filter(classification='spam').count(),
            'phishing': day_classifications.filter(classification='phishing').count(),
        })
    
    # Network threat trends
    network_trends = []
    for i in range(7):
        date = now - timedelta(days=i)
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        day_threats = NetworkThreat.objects.filter(
            user=request.user,
            created_at__gte=start_date,
            created_at__lt=end_date
        )
        
        network_trends.append({
            'date': start_date.strftime('%Y-%m-%d'),
            'total_threats': day_threats.count(),
            'high_severity': day_threats.filter(severity='high').count(),
        })
    
    # Top threat sources
    top_threat_sources = NetworkThreat.objects.filter(
        user=request.user,
        created_at__gte=week_ago
    ).values('source_ip').annotate(
        count=models.Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'email_trends': email_trends,
        'network_trends': network_trends,
        'top_threat_sources': top_threat_sources,
    }
    
    return render(request, 'dashboard/analytics.html', context)


@login_required
def reports_view(request):
    """
    Reports and exports view.
    """
    return render(request, 'dashboard/reports.html')


@login_required
def settings_view(request):
    """
    Settings and configuration view.
    """
    if request.method == 'POST':
        # Handle settings updates
        messages.success(request, 'Settings updated successfully.')
        return redirect('dashboard:settings')
    
    return render(request, 'dashboard/settings.html')


class DashboardStatsAPIView(APIView):
    """
    API endpoint for dashboard statistics.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get dashboard statistics for the current user.
        """
        try:
            # Get statistics for the last 24 hours
            now = timezone.now()
            yesterday = now - timedelta(days=1)
            
            # Email classification stats
            email_classifications = EmailClassification.objects.filter(
                user=request.user,
                created_at__gte=yesterday
            )
            
            email_stats = {
                'total': email_classifications.count(),
                'legitimate': email_classifications.filter(classification='legitimate').count(),
                'spam': email_classifications.filter(classification='spam').count(),
                'phishing': email_classifications.filter(classification='phishing').count(),
            }
            
            # Network threat stats
            network_threats = NetworkThreat.objects.filter(
                user=request.user,
                created_at__gte=yesterday
            )
            
            ddos_attacks = DDoSAttack.objects.filter(
                user=request.user,
                created_at__gte=yesterday
            )
            
            mitm_attacks = MITMAttack.objects.filter(
                user=request.user,
                created_at__gte=yesterday
            )
            
            network_stats = {
                'total_threats': network_threats.count(),
                'active_threats': network_threats.filter(is_active=True).count(),
                'ddos_attacks': ddos_attacks.count(),
                'mitm_attacks': mitm_attacks.count(),
                'high_severity': network_threats.filter(severity='high').count() + 
                                ddos_attacks.filter(severity='high').count() + 
                                mitm_attacks.filter(severity='high').count(),
            }
            
            return Response({
                'email_stats': email_stats,
                'network_stats': network_stats,
                'timestamp': now.isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching dashboard stats: {str(e)}")
            return Response({
                'error': 'An error occurred while fetching statistics'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AlertsAPIView(APIView):
    """
    API endpoint for system alerts.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get system alerts for the current user.
        """
        try:
            # Get recent high-severity threats
            now = timezone.now()
            yesterday = now - timedelta(days=1)
            
            high_severity_threats = NetworkThreat.objects.filter(
                user=request.user,
                severity__in=['high', 'critical'],
                created_at__gte=yesterday
            ).order_by('-created_at')[:10]
            
            alerts = []
            for threat in high_severity_threats:
                alerts.append({
                    'id': threat.id,
                    'type': 'threat',
                    'severity': threat.severity,
                    'message': f'{threat.threat_type.title()} threat detected from {threat.source_ip}',
                    'timestamp': threat.created_at.isoformat(),
                    'is_active': threat.is_active
                })
            
            return Response({
                'alerts': alerts,
                'total_count': len(alerts)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching alerts: {str(e)}")
            return Response({
                'error': 'An error occurred while fetching alerts'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
