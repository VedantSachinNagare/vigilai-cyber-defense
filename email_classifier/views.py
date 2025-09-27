"""
Views for email classification functionality.
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
from .models import EmailClassification, EmailSample
from .ml_models import EmailClassifier
from .serializers import EmailClassificationSerializer

logger = logging.getLogger('vigilai')


@login_required
def email_classifier_view(request):
    """
    Main email classifier view.
    """
    return render(request, 'email_classifier/classifier.html')


@login_required
@require_http_methods(["POST"])
def classify_email(request):
    """
    Classify an email and return results.
    """
    try:
        email_content = request.POST.get('email_content', '').strip()
        
        if not email_content:
            messages.error(request, 'Please provide email content to classify.')
            return redirect('email_classifier:classifier')
        
        # Initialize the ML model
        classifier = EmailClassifier()
        
        # Classify the email
        result = classifier.classify_email(email_content)
        
        # Save the classification result
        classification = EmailClassification.objects.create(
            user=request.user,
            email_content=email_content,
            classification=result['classification'],
            confidence_score=result['confidence'],
            spam_score=result['scores']['spam'],
            phishing_score=result['scores']['phishing'],
            legitimate_score=result['scores']['legitimate']
        )
        
        messages.success(request, f'Email classified as: {result["classification"].title()}')
        
        return render(request, 'email_classifier/classifier.html', {
            'classification_result': classification,
            'email_content': email_content
        })
        
    except Exception as e:
        logger.error(f"Error classifying email: {str(e)}")
        messages.error(request, 'An error occurred while classifying the email.')
        return redirect('email_classifier:classifier')


@login_required
def classification_history(request):
    """
    Display classification history for the current user.
    """
    classifications = EmailClassification.objects.filter(user=request.user).order_by('-created_at')[:50]
    return render(request, 'email_classifier/history.html', {
        'classifications': classifications
    })


@method_decorator(csrf_exempt, name='dispatch')
class ClassifyEmailAPIView(APIView):
    """
    API endpoint for email classification.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Classify an email via API.
        """
        try:
            email_content = request.data.get('email_content', '').strip()
            
            if not email_content:
                return Response({
                    'error': 'Email content is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Initialize the ML model
            classifier = EmailClassifier()
            
            # Classify the email
            result = classifier.classify_email(email_content)
            
            # Save the classification result
            classification = EmailClassification.objects.create(
                user=request.user,
                email_content=email_content,
                classification=result['classification'],
                confidence_score=result['confidence'],
                spam_score=result['scores']['spam'],
                phishing_score=result['scores']['phishing'],
                legitimate_score=result['scores']['legitimate']
            )
            
            serializer = EmailClassificationSerializer(classification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error in API email classification: {str(e)}")
            return Response({
                'error': 'An error occurred while classifying the email'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClassificationHistoryAPIView(APIView):
    """
    API endpoint for classification history.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get classification history for the current user.
        """
        try:
            classifications = EmailClassification.objects.filter(
                user=request.user
            ).order_by('-created_at')[:50]
            
            serializer = EmailClassificationSerializer(classifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching classification history: {str(e)}")
            return Response({
                'error': 'An error occurred while fetching classification history'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
