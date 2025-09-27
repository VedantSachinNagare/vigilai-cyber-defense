"""
Network detection models for VigilAI Cyber Defense System.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class NetworkLog(models.Model):
    """
    Model to store network logs for analysis.
    """
    LOG_TYPE_CHOICES = [
        ('http', 'HTTP Request'),
        ('https', 'HTTPS Request'),
        ('tcp', 'TCP Connection'),
        ('udp', 'UDP Connection'),
        ('dns', 'DNS Query'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    log_type = models.CharField(max_length=10, choices=LOG_TYPE_CHOICES)
    source_ip = models.GenericIPAddressField()
    destination_ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField()
    protocol = models.CharField(max_length=10)
    user_agent = models.TextField(blank=True)
    request_path = models.CharField(max_length=500, blank=True)
    response_code = models.PositiveIntegerField(null=True, blank=True)
    bytes_sent = models.PositiveIntegerField(default=0)
    bytes_received = models.PositiveIntegerField(default=0)
    duration = models.FloatField(default=0.0)  # in seconds
    raw_log = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Network Log'
        verbose_name_plural = 'Network Logs'
    
    def __str__(self):
        return f"Network Log - {self.source_ip} -> {self.destination_ip} ({self.timestamp})"


class DDoSAttack(models.Model):
    """
    Model to store detected DDoS attacks.
    """
    ATTACK_TYPE_CHOICES = [
        ('volumetric', 'Volumetric Attack'),
        ('protocol', 'Protocol Attack'),
        ('application', 'Application Layer Attack'),
        ('suspicious', 'Suspicious Activity'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    attack_type = models.CharField(max_length=20, choices=ATTACK_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    source_ip = models.GenericIPAddressField()
    target_ip = models.GenericIPAddressField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    request_count = models.PositiveIntegerField(default=0)
    bytes_transferred = models.PositiveBigIntegerField(default=0)
    confidence_score = models.FloatField(help_text="Confidence score (0-1) for the detection")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    mitigation_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'DDoS Attack'
        verbose_name_plural = 'DDoS Attacks'
    
    def __str__(self):
        return f"DDoS Attack - {self.attack_type} from {self.source_ip} ({self.severity})"


class MITMAttack(models.Model):
    """
    Model to store detected MITM attacks.
    """
    ATTACK_TYPE_CHOICES = [
        ('ssl_strip', 'SSL Stripping'),
        ('certificate_spoof', 'Certificate Spoofing'),
        ('dns_hijack', 'DNS Hijacking'),
        ('arp_spoof', 'ARP Spoofing'),
        ('suspicious_cert', 'Suspicious Certificate'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    attack_type = models.CharField(max_length=20, choices=ATTACK_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    source_ip = models.GenericIPAddressField()
    target_ip = models.GenericIPAddressField()
    domain = models.CharField(max_length=255, blank=True)
    certificate_issuer = models.CharField(max_length=255, blank=True)
    certificate_subject = models.CharField(max_length=255, blank=True)
    certificate_valid = models.BooleanField(default=True)
    ssl_version = models.CharField(max_length=20, blank=True)
    cipher_suite = models.CharField(max_length=100, blank=True)
    confidence_score = models.FloatField(help_text="Confidence score (0-1) for the detection")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    mitigation_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'MITM Attack'
        verbose_name_plural = 'MITM Attacks'
    
    def __str__(self):
        return f"MITM Attack - {self.attack_type} targeting {self.target_ip} ({self.severity})"


class NetworkThreat(models.Model):
    """
    Model to store general network threats and anomalies.
    """
    THREAT_TYPE_CHOICES = [
        ('ddos', 'DDoS Attack'),
        ('mitm', 'MITM Attack'),
        ('port_scan', 'Port Scan'),
        ('brute_force', 'Brute Force Attack'),
        ('malware', 'Malware Communication'),
        ('suspicious', 'Suspicious Activity'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    threat_type = models.CharField(max_length=20, choices=THREAT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    source_ip = models.GenericIPAddressField()
    target_ip = models.GenericIPAddressField()
    port = models.PositiveIntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=10, blank=True)
    confidence_score = models.FloatField(help_text="Confidence score (0-1) for the detection")
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    mitigation_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Network Threat'
        verbose_name_plural = 'Network Threats'
    
    def __str__(self):
        return f"Network Threat - {self.threat_type} from {self.source_ip} ({self.severity})"


class DetectionMetrics(models.Model):
    """
    Model to store detection performance metrics.
    """
    model_name = models.CharField(max_length=100)
    detection_type = models.CharField(max_length=20)  # ddos, mitm, general
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    false_positive_rate = models.FloatField()
    true_positive_rate = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Detection Metrics'
        verbose_name_plural = 'Detection Metrics'
    
    def __str__(self):
        return f"Metrics for {self.model_name} - {self.detection_type} (Accuracy: {self.accuracy:.3f})"
