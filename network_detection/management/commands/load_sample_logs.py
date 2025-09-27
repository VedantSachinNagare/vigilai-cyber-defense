"""
Management command to load sample network logs for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from network_detection.models import NetworkLog, DDoSAttack, MITMAttack, NetworkThreat
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample network logs and threats for testing the detection system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username to associate logs with',
            default='admin'
        )

    def handle(self, *args, **options):
        """
        Load sample network logs and threats into the database.
        """
        # Get or create user
        user, created = User.objects.get_or_create(
            username=options['user'],
            defaults={'email': f'{options["user"]}@example.com'}
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(f'Created user: {user.username}')

        # Generate sample network logs
        self.generate_network_logs(user)
        
        # Generate sample threats
        self.generate_sample_threats(user)

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample network data')
        )

    def generate_network_logs(self, user):
        """
        Generate sample network logs.
        """
        now = datetime.now()
        log_types = ['http', 'https', 'tcp', 'udp']
        protocols = ['HTTP/1.1', 'HTTPS/1.1', 'TCP', 'UDP']
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'curl/7.68.0',
            'Python-urllib/3.8'
        ]
        
        # Generate normal traffic
        for i in range(100):
            log = NetworkLog.objects.create(
                user=user,
                timestamp=now - timedelta(minutes=random.randint(0, 1440)),
                log_type=random.choice(log_types),
                source_ip=f'192.168.1.{random.randint(1, 254)}',
                destination_ip=f'10.0.0.{random.randint(1, 254)}',
                port=random.choice([80, 443, 22, 21, 25, 53]),
                protocol=random.choice(protocols),
                user_agent=random.choice(user_agents),
                request_path=f'/api/v1/endpoint{random.randint(1, 10)}',
                response_code=random.choice([200, 201, 404, 500]),
                bytes_sent=random.randint(100, 10000),
                bytes_received=random.randint(100, 10000),
                duration=random.uniform(0.1, 5.0)
            )

        # Generate suspicious traffic (DDoS-like)
        for i in range(50):
            log = NetworkLog.objects.create(
                user=user,
                timestamp=now - timedelta(minutes=random.randint(0, 60)),
                log_type='http',
                source_ip='192.168.100.1',  # Same source IP (suspicious)
                destination_ip='10.0.0.1',
                port=80,
                protocol='HTTP/1.1',
                user_agent='curl/7.68.0',
                request_path='/api/v1/endpoint1',
                response_code=200,
                bytes_sent=random.randint(50, 200),
                bytes_received=random.randint(50, 200),
                duration=random.uniform(0.01, 0.1)
            )

    def generate_sample_threats(self, user):
        """
        Generate sample network threats.
        """
        now = datetime.now()
        
        # Generate DDoS attacks
        for i in range(3):
            DDoSAttack.objects.create(
                user=user,
                attack_type='volumetric',
                severity=random.choice(['medium', 'high']),
                source_ip='192.168.100.1',
                target_ip='10.0.0.1',
                start_time=now - timedelta(hours=random.randint(1, 24)),
                end_time=now - timedelta(hours=random.randint(0, 1)),
                request_count=random.randint(1000, 10000),
                bytes_transferred=random.randint(1000000, 10000000),
                confidence_score=random.uniform(0.7, 0.95),
                is_active=random.choice([True, False]),
                description=f'DDoS attack detected from {random.choice(["192.168.100.1", "10.0.0.100"])} with high request rate'
            )

        # Generate MITM attacks
        for i in range(2):
            MITMAttack.objects.create(
                user=user,
                attack_type=random.choice(['ssl_strip', 'certificate_spoof']),
                severity=random.choice(['medium', 'high']),
                source_ip='192.168.200.1',
                target_ip='10.0.0.2',
                domain=f'example{random.randint(1, 10)}.com',
                certificate_issuer='Suspicious CA',
                certificate_subject='Fake Certificate',
                certificate_valid=False,
                ssl_version='TLS 1.0',
                cipher_suite='RC4-MD5',
                confidence_score=random.uniform(0.6, 0.9),
                is_active=random.choice([True, False]),
                description=f'MITM attack detected: {random.choice(["SSL stripping", "Certificate spoofing"])} between 192.168.200.1 and 10.0.0.2'
            )

        # Generate general network threats
        threat_types = ['ddos', 'mitm', 'port_scan', 'brute_force', 'malware']
        for i in range(10):
            NetworkThreat.objects.create(
                user=user,
                threat_type=random.choice(threat_types),
                severity=random.choice(['low', 'medium', 'high', 'critical']),
                source_ip=f'192.168.{random.randint(1, 255)}.{random.randint(1, 255)}',
                target_ip=f'10.0.0.{random.randint(1, 255)}',
                port=random.choice([22, 80, 443, 3389, 5900]),
                protocol=random.choice(['TCP', 'UDP']),
                confidence_score=random.uniform(0.5, 0.95),
                is_active=random.choice([True, False]),
                description=f'{random.choice(threat_types).title()} threat detected from {f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"}'
            )
