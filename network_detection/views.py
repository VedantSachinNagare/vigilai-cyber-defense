"""
Views for network detection functionality.
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from .models import NetworkLog, DDoSAttack, MITMAttack, NetworkThreat
from .ml_models import DDoSDetector, MITMDetector
from .serializers import (
    NetworkLogSerializer, DDoSAttackSerializer, 
    MITMAttackSerializer, NetworkThreatSerializer
)

logger = logging.getLogger('vigilai')


@login_required
def network_detection_view(request):
    """
    Main network detection dashboard.
    """
    # Get recent threats
    recent_threats = NetworkThreat.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Get statistics
    total_threats = NetworkThreat.objects.filter(user=request.user).count()
    active_threats = NetworkThreat.objects.filter(user=request.user, is_active=True).count()
    ddos_attacks = DDoSAttack.objects.filter(user=request.user).count()
    mitm_attacks = MITMAttack.objects.filter(user=request.user).count()
    
    context = {
        'recent_threats': recent_threats,
        'total_threats': total_threats,
        'active_threats': active_threats,
        'ddos_attacks': ddos_attacks,
        'mitm_attacks': mitm_attacks,
    }
    
    return render(request, 'network_detection/detection.html', context)


@login_required
def ddos_detection_view(request):
    """
    DDoS detection view.
    """
    ddos_attacks = DDoSAttack.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(ddos_attacks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network_detection/ddos.html', {
        'page_obj': page_obj,
        'ddos_attacks': ddos_attacks
    })


@login_required
def mitm_detection_view(request):
    """
    MITM detection view.
    """
    mitm_attacks = MITMAttack.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(mitm_attacks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network_detection/mitm.html', {
        'page_obj': page_obj,
        'mitm_attacks': mitm_attacks
    })


@login_required
def threats_view(request):
    """
    Network threats view.
    """
    threats = NetworkThreat.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(threats, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network_detection/threats.html', {
        'page_obj': page_obj,
        'threats': threats
    })


@login_required
def network_logs_view(request):
    """
    Network logs view.
    """
    logs = NetworkLog.objects.filter(user=request.user).order_by('-timestamp')
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network_detection/logs.html', {
        'page_obj': page_obj,
        'logs': logs
    })


@login_required
@require_http_methods(["POST"])
def analyze_network_logs(request):
    """
    Analyze network logs for threats.
    """
    try:
        # Get logs from the last hour
        from django.utils import timezone
        from datetime import timedelta
        
        one_hour_ago = timezone.now() - timedelta(hours=1)
        recent_logs = NetworkLog.objects.filter(
            user=request.user,
            timestamp__gte=one_hour_ago
        )
        
        # Initialize detectors
        ddos_detector = DDoSDetector()
        mitm_detector = MITMDetector()
        
        # Analyze for DDoS attacks
        ddos_threats = ddos_detector.detect_attacks(recent_logs)
        
        # Analyze for MITM attacks
        mitm_threats = mitm_detector.detect_attacks(recent_logs)
        
        # Save detected threats
        for threat in ddos_threats:
            DDoSAttack.objects.create(
                user=request.user,
                **threat
            )
        
        for threat in mitm_threats:
            MITMAttack.objects.create(
                user=request.user,
                **threat
            )
        
        messages.success(request, f'Analysis complete. Found {len(ddos_threats)} DDoS threats and {len(mitm_threats)} MITM threats.')
        
        return redirect('network_detection:detection')
        
    except Exception as e:
        logger.error(f"Error analyzing network logs: {str(e)}")
        messages.error(request, 'An error occurred while analyzing network logs.')
        return redirect('network_detection:detection')


@method_decorator(csrf_exempt, name='dispatch')
class DetectionAPIView(APIView):
    """
    API endpoint for network threat detection.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Analyze network logs for threats via API.
        """
        try:
            # Get logs from the last hour
            from django.utils import timezone
            from datetime import timedelta
            
            one_hour_ago = timezone.now() - timedelta(hours=1)
            recent_logs = NetworkLog.objects.filter(
                user=request.user,
                timestamp__gte=one_hour_ago
            )
            
            # Initialize detectors
            ddos_detector = DDoSDetector()
            mitm_detector = MITMDetector()
            
            # Analyze for threats
            ddos_threats = ddos_detector.detect_attacks(recent_logs)
            mitm_threats = mitm_detector.detect_attacks(recent_logs)
            
            # Save detected threats
            ddos_attacks = []
            for threat in ddos_threats:
                attack = DDoSAttack.objects.create(
                    user=request.user,
                    **threat
                )
                ddos_attacks.append(attack)
            
            mitm_attacks = []
            for threat in mitm_threats:
                attack = MITMAttack.objects.create(
                    user=request.user,
                    **threat
                )
                mitm_attacks.append(attack)
            
            # Serialize results
            ddos_serializer = DDoSAttackSerializer(ddos_attacks, many=True)
            mitm_serializer = MITMAttackSerializer(mitm_attacks, many=True)
            
            return Response({
                'ddos_attacks': ddos_serializer.data,
                'mitm_attacks': mitm_serializer.data,
                'total_threats': len(ddos_threats) + len(mitm_threats)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in API threat detection: {str(e)}")
            return Response({
                'error': 'An error occurred while detecting threats'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThreatsAPIView(APIView):
    """
    API endpoint for network threats.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get network threats for the current user.
        """
        try:
            threats = NetworkThreat.objects.filter(
                user=request.user
            ).order_by('-created_at')[:100]
            
            serializer = NetworkThreatSerializer(threats, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching network threats: {str(e)}")
            return Response({
                'error': 'An error occurred while fetching threats'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NetworkLogsAPIView(APIView):
    """
    API endpoint for network logs.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get network logs for the current user.
        """
        try:
            logs = NetworkLog.objects.filter(
                user=request.user
            ).order_by('-timestamp')[:100]
            
            serializer = NetworkLogSerializer(logs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching network logs: {str(e)}")
            return Response({
                'error': 'An error occurred while fetching logs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
