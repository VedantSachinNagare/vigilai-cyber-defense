"""
Machine Learning models for network threat detection.
"""
import logging
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import statistics

logger = logging.getLogger('vigilai')


class DDoSDetector:
    """
    DDoS attack detection using anomaly detection.
    """
    
    def __init__(self):
        """
        Initialize the DDoS detector.
        """
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def _extract_features(self, logs) -> List[Dict]:
        """
        Extract features from network logs for DDoS detection.
        """
        features = []
        
        # Group logs by source IP
        ip_groups = {}
        for log in logs:
            ip = log.source_ip
            if ip not in ip_groups:
                ip_groups[ip] = []
            ip_groups[ip].append(log)
        
        for ip, ip_logs in ip_groups.items():
            if len(ip_logs) < 5:  # Skip IPs with too few requests
                continue
            
            # Calculate features for this IP
            feature_dict = self._calculate_ip_features(ip, ip_logs)
            features.append(feature_dict)
        
        return features
    
    def _calculate_ip_features(self, ip: str, logs: List) -> Dict:
        """
        Calculate features for a specific IP address.
        """
        # Basic statistics
        request_count = len(logs)
        unique_destinations = len(set(log.destination_ip for log in logs))
        unique_ports = len(set(log.port for log in logs))
        
        # Time-based features
        timestamps = [log.timestamp for log in logs]
        time_span = (max(timestamps) - min(timestamps)).total_seconds()
        requests_per_second = request_count / max(time_span, 1)
        
        # Request pattern features
        response_codes = [log.response_code for log in logs if log.response_code]
        error_rate = sum(1 for code in response_codes if code >= 400) / max(len(response_codes), 1)
        
        # Data transfer features
        total_bytes_sent = sum(log.bytes_sent for log in logs)
        total_bytes_received = sum(log.bytes_received for log in logs)
        avg_bytes_per_request = (total_bytes_sent + total_bytes_received) / max(request_count, 1)
        
        # User agent analysis
        user_agents = [log.user_agent for log in logs if log.user_agent]
        unique_user_agents = len(set(user_agents))
        user_agent_diversity = unique_user_agents / max(len(user_agents), 1)
        
        # Protocol analysis
        protocols = [log.protocol for log in logs]
        protocol_counts = {}
        for protocol in protocols:
            protocol_counts[protocol] = protocol_counts.get(protocol, 0) + 1
        
        # Suspicious patterns
        suspicious_patterns = self._detect_suspicious_patterns(logs)
        
        return {
            'ip': ip,
            'request_count': request_count,
            'unique_destinations': unique_destinations,
            'unique_ports': unique_ports,
            'requests_per_second': requests_per_second,
            'error_rate': error_rate,
            'avg_bytes_per_request': avg_bytes_per_request,
            'user_agent_diversity': user_agent_diversity,
            'suspicious_patterns': suspicious_patterns,
            'logs': logs
        }
    
    def _detect_suspicious_patterns(self, logs: List) -> Dict:
        """
        Detect suspicious patterns in network logs.
        """
        patterns = {
            'rapid_requests': False,
            'same_user_agent': False,
            'high_error_rate': False,
            'unusual_ports': False,
            'bot_like_behavior': False
        }
        
        if len(logs) < 2:
            return patterns
        
        # Rapid requests (more than 10 requests per second)
        timestamps = [log.timestamp for log in logs]
        time_span = (max(timestamps) - min(timestamps)).total_seconds()
        if time_span > 0 and len(logs) / time_span > 10:
            patterns['rapid_requests'] = True
        
        # Same user agent for all requests
        user_agents = [log.user_agent for log in logs if log.user_agent]
        if len(set(user_agents)) == 1 and len(user_agents) > 5:
            patterns['same_user_agent'] = True
        
        # High error rate
        response_codes = [log.response_code for log in logs if log.response_code]
        if response_codes:
            error_rate = sum(1 for code in response_codes if code >= 400) / len(response_codes)
            if error_rate > 0.5:
                patterns['high_error_rate'] = True
        
        # Unusual ports (non-standard ports)
        ports = [log.port for log in logs]
        unusual_ports = sum(1 for port in ports if port not in [80, 443, 22, 21, 25, 53, 110, 143, 993, 995])
        if unusual_ports / len(ports) > 0.3:
            patterns['unusual_ports'] = True
        
        # Bot-like behavior (very regular intervals)
        if len(timestamps) > 10:
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)
            
            if intervals:
                interval_std = statistics.stdev(intervals) if len(intervals) > 1 else 0
                if interval_std < 1.0:  # Very regular intervals
                    patterns['bot_like_behavior'] = True
        
        return patterns
    
    def _prepare_features_for_ml(self, features: List[Dict]) -> np.ndarray:
        """
        Prepare features for machine learning model.
        """
        feature_matrix = []
        
        for feature_dict in features:
            feature_vector = [
                feature_dict['request_count'],
                feature_dict['unique_destinations'],
                feature_dict['unique_ports'],
                feature_dict['requests_per_second'],
                feature_dict['error_rate'],
                feature_dict['avg_bytes_per_request'],
                feature_dict['user_agent_diversity'],
                sum(feature_dict['suspicious_patterns'].values())
            ]
            feature_matrix.append(feature_vector)
        
        return np.array(feature_matrix)
    
    def detect_attacks(self, logs) -> List[Dict]:
        """
        Detect DDoS attacks in network logs.
        """
        try:
            if len(logs) < 10:
                return []
            
            # Extract features
            features = self._extract_features(logs)
            
            if len(features) < 3:
                return []
            
            # Prepare features for ML
            feature_matrix = self._prepare_features_for_ml(features)
            
            # Scale features
            feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
            
            # Detect anomalies
            anomaly_scores = self.isolation_forest.fit_predict(feature_matrix_scaled)
            
            # Identify attacks
            attacks = []
            for i, (feature_dict, score) in enumerate(zip(features, anomaly_scores)):
                if score == -1:  # Anomaly detected
                    attack = self._create_attack_record(feature_dict, 'ddos')
                    attacks.append(attack)
            
            return attacks
            
        except Exception as e:
            logger.error(f"Error detecting DDoS attacks: {str(e)}")
            return []
    
    def _create_attack_record(self, feature_dict: Dict, attack_type: str) -> Dict:
        """
        Create an attack record from detected features.
        """
        # Determine severity based on features
        severity = 'low'
        if feature_dict['requests_per_second'] > 50:
            severity = 'high'
        elif feature_dict['requests_per_second'] > 20:
            severity = 'medium'
        
        # Calculate confidence score
        confidence = min(0.9, feature_dict['requests_per_second'] / 100.0)
        
        return {
            'attack_type': 'volumetric',
            'severity': severity,
            'source_ip': feature_dict['ip'],
            'target_ip': '0.0.0.0',  # Will be updated with actual target
            'start_time': datetime.now(),
            'request_count': feature_dict['request_count'],
            'bytes_transferred': feature_dict['request_count'] * feature_dict['avg_bytes_per_request'],
            'confidence_score': confidence,
            'description': f'DDoS attack detected from {feature_dict["ip"]} with {feature_dict["requests_per_second"]:.1f} requests/second'
        }


class MITMDetector:
    """
    MITM attack detection using SSL/TLS analysis.
    """
    
    def __init__(self):
        """
        Initialize the MITM detector.
        """
        self.suspicious_certificates = set()
        self.known_good_certificates = set()
    
    def _extract_ssl_features(self, logs) -> List[Dict]:
        """
        Extract SSL/TLS features from network logs.
        """
        features = []
        
        # Group logs by connection
        connections = {}
        for log in logs:
            if log.log_type in ['https', 'ssl', 'tls']:
                key = f"{log.source_ip}_{log.destination_ip}_{log.port}"
                if key not in connections:
                    connections[key] = []
                connections[key].append(log)
        
        for connection_key, connection_logs in connections.items():
            if len(connection_logs) < 2:
                continue
            
            feature_dict = self._analyze_ssl_connection(connection_key, connection_logs)
            if feature_dict:
                features.append(feature_dict)
        
        return features
    
    def _analyze_ssl_connection(self, connection_key: str, logs: List) -> Dict:
        """
        Analyze SSL/TLS connection for MITM indicators.
        """
        # Extract connection info
        source_ip = logs[0].source_ip
        dest_ip = logs[0].destination_ip
        port = logs[0].port
        
        # Analyze SSL/TLS patterns
        ssl_indicators = {
            'certificate_issues': False,
            'weak_cipher': False,
            'suspicious_issuer': False,
            'certificate_mismatch': False,
            'ssl_stripping': False
        }
        
        # Check for certificate issues
        for log in logs:
            if hasattr(log, 'certificate_valid') and not log.certificate_valid:
                ssl_indicators['certificate_issues'] = True
            
            if hasattr(log, 'certificate_issuer'):
                if self._is_suspicious_issuer(log.certificate_issuer):
                    ssl_indicators['suspicious_issuer'] = True
            
            if hasattr(log, 'cipher_suite'):
                if self._is_weak_cipher(log.cipher_suite):
                    ssl_indicators['weak_cipher'] = True
        
        # Check for SSL stripping (HTTP requests to HTTPS ports)
        http_requests = sum(1 for log in logs if log.log_type == 'http' and log.port == 443)
        if http_requests > 0:
            ssl_indicators['ssl_stripping'] = True
        
        # Calculate confidence score
        confidence = sum(ssl_indicators.values()) / len(ssl_indicators)
        
        return {
            'connection_key': connection_key,
            'source_ip': source_ip,
            'dest_ip': dest_ip,
            'port': port,
            'ssl_indicators': ssl_indicators,
            'confidence': confidence,
            'logs': logs
        }
    
    def _is_suspicious_issuer(self, issuer: str) -> bool:
        """
        Check if certificate issuer is suspicious.
        """
        if not issuer:
            return False
        
        suspicious_issuers = [
            'self-signed',
            'unknown',
            'fake',
            'phishing'
        ]
        
        issuer_lower = issuer.lower()
        return any(suspicious in issuer_lower for suspicious in suspicious_issuers)
    
    def _is_weak_cipher(self, cipher_suite: str) -> bool:
        """
        Check if cipher suite is weak.
        """
        if not cipher_suite:
            return False
        
        weak_ciphers = [
            'RC4',
            'DES',
            'MD5',
            'SHA1'
        ]
        
        cipher_upper = cipher_suite.upper()
        return any(weak in cipher_upper for weak in weak_ciphers)
    
    def detect_attacks(self, logs) -> List[Dict]:
        """
        Detect MITM attacks in network logs.
        """
        try:
            if len(logs) < 5:
                return []
            
            # Extract SSL features
            features = self._extract_ssl_features(logs)
            
            if not features:
                return []
            
            # Identify attacks
            attacks = []
            for feature_dict in features:
                if feature_dict['confidence'] > 0.3:  # Threshold for MITM detection
                    attack = self._create_mitm_attack_record(feature_dict)
                    attacks.append(attack)
            
            return attacks
            
        except Exception as e:
            logger.error(f"Error detecting MITM attacks: {str(e)}")
            return []
    
    def _create_mitm_attack_record(self, feature_dict: Dict) -> Dict:
        """
        Create a MITM attack record from detected features.
        """
        # Determine attack type
        attack_type = 'suspicious_cert'
        if feature_dict['ssl_indicators']['ssl_stripping']:
            attack_type = 'ssl_strip'
        elif feature_dict['ssl_indicators']['certificate_issues']:
            attack_type = 'certificate_spoof'
        
        # Determine severity
        severity = 'low'
        if feature_dict['confidence'] > 0.7:
            severity = 'high'
        elif feature_dict['confidence'] > 0.5:
            severity = 'medium'
        
        return {
            'attack_type': attack_type,
            'severity': severity,
            'source_ip': feature_dict['source_ip'],
            'target_ip': feature_dict['dest_ip'],
            'confidence_score': feature_dict['confidence'],
            'description': f'MITM attack detected: {attack_type} between {feature_dict["source_ip"]} and {feature_dict["dest_ip"]}'
        }
