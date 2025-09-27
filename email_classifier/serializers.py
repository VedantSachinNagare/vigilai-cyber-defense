"""
Serializers for email classifier app.
"""
from rest_framework import serializers
from .models import EmailClassification, EmailSample, ClassificationMetrics


class EmailClassificationSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailClassification model.
    """
    class Meta:
        model = EmailClassification
        fields = [
            'id', 'email_content', 'classification', 'confidence_score',
            'spam_score', 'phishing_score', 'legitimate_score',
            'created_at', 'processed_at'
        ]
        read_only_fields = ['id', 'created_at', 'processed_at']


class EmailSampleSerializer(serializers.ModelSerializer):
    """
    Serializer for EmailSample model.
    """
    class Meta:
        model = EmailSample
        fields = [
            'id', 'subject', 'content', 'classification',
            'is_verified', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ClassificationMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for ClassificationMetrics model.
    """
    class Meta:
        model = ClassificationMetrics
        fields = [
            'id', 'model_name', 'accuracy', 'precision',
            'recall', 'f1_score', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
