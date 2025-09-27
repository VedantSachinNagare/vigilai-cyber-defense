"""
Admin configuration for network detection app.
"""
from django.contrib import admin
from .models import (
    NetworkLog, DDoSAttack, MITMAttack, NetworkThreat, DetectionMetrics
)


@admin.register(NetworkLog)
class NetworkLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'timestamp', 'log_type', 'source_ip', 'destination_ip', 'port', 'protocol']
    list_filter = ['log_type', 'protocol', 'timestamp', 'user']
    search_fields = ['source_ip', 'destination_ip', 'user_agent', 'request_path']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']


@admin.register(DDoSAttack)
class DDoSAttackAdmin(admin.ModelAdmin):
    list_display = ['id', 'attack_type', 'severity', 'source_ip', 'target_ip', 'is_active', 'created_at']
    list_filter = ['attack_type', 'severity', 'is_active', 'created_at', 'user']
    search_fields = ['source_ip', 'target_ip', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(MITMAttack)
class MITMAttackAdmin(admin.ModelAdmin):
    list_display = ['id', 'attack_type', 'severity', 'source_ip', 'target_ip', 'domain', 'is_active', 'created_at']
    list_filter = ['attack_type', 'severity', 'is_active', 'created_at', 'user']
    search_fields = ['source_ip', 'target_ip', 'domain', 'certificate_issuer', 'certificate_subject']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(NetworkThreat)
class NetworkThreatAdmin(admin.ModelAdmin):
    list_display = ['id', 'threat_type', 'severity', 'source_ip', 'target_ip', 'is_active', 'created_at']
    list_filter = ['threat_type', 'severity', 'is_active', 'created_at', 'user']
    search_fields = ['source_ip', 'target_ip', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(DetectionMetrics)
class DetectionMetricsAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'detection_type', 'accuracy', 'precision', 'recall', 'f1_score', 'created_at']
    list_filter = ['model_name', 'detection_type', 'created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
