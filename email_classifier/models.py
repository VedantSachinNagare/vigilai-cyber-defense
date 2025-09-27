"""
Email classification models for VigilAI Cyber Defense System.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmailClassification(models.Model):
    """
    Model to store email classification results.
    """
    CLASSIFICATION_CHOICES = [
        ('legitimate', 'Legitimate'),
        ('spam', 'Spam'),
        ('phishing', 'Phishing'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email_content = models.TextField(help_text="The email content to be classified")
    classification = models.CharField(
        max_length=20, 
        choices=CLASSIFICATION_CHOICES,
        help_text="The classification result"
    )
    confidence_score = models.FloatField(
        help_text="Confidence score (0-1) for the classification"
    )
    spam_score = models.FloatField(
        default=0.0,
        help_text="Spam probability score"
    )
    phishing_score = models.FloatField(
        default=0.0,
        help_text="Phishing probability score"
    )
    legitimate_score = models.FloatField(
        default=0.0,
        help_text="Legitimate probability score"
    )
    created_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Classification'
        verbose_name_plural = 'Email Classifications'
    
    def __str__(self):
        return f"Email Classification - {self.classification} ({self.confidence_score:.2f})"


class EmailSample(models.Model):
    """
    Model to store sample emails for training/testing.
    """
    CLASSIFICATION_CHOICES = [
        ('legitimate', 'Legitimate'),
        ('spam', 'Spam'),
        ('phishing', 'Phishing'),
    ]
    
    subject = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    classification = models.CharField(max_length=20, choices=CLASSIFICATION_CHOICES)
    is_verified = models.BooleanField(default=False, help_text="Whether this sample has been verified by experts")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Sample'
        verbose_name_plural = 'Email Samples'
    
    def __str__(self):
        return f"Sample Email - {self.classification}"


class ClassificationMetrics(models.Model):
    """
    Model to store classification performance metrics.
    """
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Classification Metrics'
        verbose_name_plural = 'Classification Metrics'
    
    def __str__(self):
        return f"Metrics for {self.model_name} - Accuracy: {self.accuracy:.3f}"
