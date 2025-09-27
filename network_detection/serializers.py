"""
Serializers for network detection app.
"""
from rest_framework import serializers
from .models import (
    NetworkLog, DDoSAttack, MITMAttack, NetworkThreat, DetectionMetrics
)


class NetworkLogSerializer(serializers.ModelSerializer):
    """
    Serializer for NetworkLog model.
    """
    class Meta:
        model = NetworkLog
        fields = [
            'id', 'timestamp', 'log_type', 'source_ip', 'destination_ip',
            'port', 'protocol', 'user_agent', 'request_path', 'response_code',
            'bytes_sent', 'bytes_received', 'duration', 'raw_log'
        ]
        read_only_fields = ['id', 'timestamp']


class DDoSAttackSerializer(serializers.ModelSerializer):
    """
    Serializer for DDoSAttack model.
    """
    class Meta:
        model = DDoSAttack
        fields = [
            'id', 'attack_type', 'severity', 'source_ip', 'target_ip',
            'start_time', 'end_time', 'request_count', 'bytes_transferred',
            'confidence_score', 'is_active', 'description', 'mitigation_applied',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class MITMAttackSerializer(serializers.ModelSerializer):
    """
    Serializer for MITMAttack model.
    """
    class Meta:
        model = MITMAttack
        fields = [
            'id', 'attack_type', 'severity', 'source_ip', 'target_ip',
            'domain', 'certificate_issuer', 'certificate_subject',
            'certificate_valid', 'ssl_version', 'cipher_suite',
            'confidence_score', 'is_active', 'description', 'mitigation_applied',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class NetworkThreatSerializer(serializers.ModelSerializer):
    """
    Serializer for NetworkThreat model.
    """
    class Meta:
        model = NetworkThreat
        fields = [
            'id', 'threat_type', 'severity', 'source_ip', 'target_ip',
            'port', 'protocol', 'confidence_score', 'is_active',
            'description', 'mitigation_applied', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DetectionMetricsSerializer(serializers.ModelSerializer):
    """
    Serializer for DetectionMetrics model.
    """
    class Meta:
        model = DetectionMetrics
        fields = [
            'id', 'model_name', 'detection_type', 'accuracy', 'precision',
            'recall', 'f1_score', 'false_positive_rate', 'true_positive_rate',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
