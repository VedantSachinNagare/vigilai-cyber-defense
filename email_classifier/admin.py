"""
Admin configuration for email classifier app.
"""
from django.contrib import admin
from .models import EmailClassification, EmailSample, ClassificationMetrics


@admin.register(EmailClassification)
class EmailClassificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'classification', 'confidence_score', 'user', 'created_at']
    list_filter = ['classification', 'created_at', 'user']
    search_fields = ['email_content', 'classification']
    readonly_fields = ['created_at', 'processed_at']
    ordering = ['-created_at']


@admin.register(EmailSample)
class EmailSampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'classification', 'is_verified', 'created_at']
    list_filter = ['classification', 'is_verified', 'created_at']
    search_fields = ['subject', 'content', 'classification']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(ClassificationMetrics)
class ClassificationMetricsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'accuracy', 'precision', 'recall', 'f1_score', 'created_at']
    list_filter = ['model_name', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
