"""
Machine Learning models for email classification.
"""
import logging
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, List, Tuple
import re

logger = logging.getLogger('vigilai')


class EmailClassifier:
    """
    Email spam/phishing classifier using DistilBERT.
    """
    
    def __init__(self):
        """
        Initialize the email classifier with DistilBERT model.
        """
        self.model_name = "distilbert-base-uncased"
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """
        Load the DistilBERT model and tokenizer.
        """
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # For this demo, we'll use a simple approach
            # In production, you would fine-tune the model on your dataset
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=3  # legitimate, spam, phishing
            )
            
            logger.info("Email classifier model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading email classifier model: {str(e)}")
            raise
    
    def _extract_features(self, email_content: str) -> Dict[str, float]:
        """
        Extract features from email content for classification.
        """
        features = {}
        
        # Basic text features
        features['length'] = len(email_content)
        features['word_count'] = len(email_content.split())
        features['char_count'] = len(email_content.replace(' ', ''))
        
        # Suspicious patterns
        features['suspicious_words'] = self._count_suspicious_words(email_content)
        features['urgent_words'] = self._count_urgent_words(email_content)
        features['money_mentions'] = self._count_money_mentions(email_content)
        features['link_count'] = self._count_links(email_content)
        features['exclamation_count'] = email_content.count('!')
        features['caps_ratio'] = self._calculate_caps_ratio(email_content)
        
        # Phishing indicators
        features['suspicious_domains'] = self._count_suspicious_domains(email_content)
        features['personal_info_requests'] = self._count_personal_info_requests(email_content)
        
        return features
    
    def _count_suspicious_words(self, text: str) -> int:
        """
        Count suspicious words that might indicate spam/phishing.
        """
        suspicious_words = [
            'free', 'win', 'winner', 'congratulations', 'urgent', 'immediate',
            'click', 'here', 'limited', 'offer', 'deal', 'discount',
            'verify', 'account', 'suspended', 'expired', 'update', 'confirm'
        ]
        
        text_lower = text.lower()
        count = 0
        for word in suspicious_words:
            count += text_lower.count(word)
        
        return count
    
    def _count_urgent_words(self, text: str) -> int:
        """
        Count urgent words that might indicate phishing.
        """
        urgent_words = [
            'urgent', 'immediate', 'asap', 'expires', 'deadline',
            'act now', 'limited time', 'hurry', 'rush'
        ]
        
        text_lower = text.lower()
        count = 0
        for word in urgent_words:
            count += text_lower.count(word)
        
        return count
    
    def _count_money_mentions(self, text: str) -> int:
        """
        Count mentions of money amounts.
        """
        money_pattern = r'\$[\d,]+(?:\.\d{2})?|\d+\s*(?:dollars?|USD|usd)'
        return len(re.findall(money_pattern, text, re.IGNORECASE))
    
    def _count_links(self, text: str) -> int:
        """
        Count number of links in the text.
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return len(re.findall(url_pattern, text))
    
    def _calculate_caps_ratio(self, text: str) -> float:
        """
        Calculate the ratio of uppercase letters.
        """
        if len(text) == 0:
            return 0.0
        
        uppercase_count = sum(1 for c in text if c.isupper())
        return uppercase_count / len(text)
    
    def _count_suspicious_domains(self, text: str) -> int:
        """
        Count suspicious domain patterns.
        """
        # Look for domains that might be trying to mimic legitimate ones
        suspicious_patterns = [
            r'[a-zA-Z0-9]+\.tk',
            r'[a-zA-Z0-9]+\.ml',
            r'[a-zA-Z0-9]+\.ga',
            r'[a-zA-Z0-9]+\.cf',
            r'bit\.ly',
            r'tinyurl\.com',
            r'short\.link'
        ]
        
        count = 0
        for pattern in suspicious_patterns:
            count += len(re.findall(pattern, text, re.IGNORECASE))
        
        return count
    
    def _count_personal_info_requests(self, text: str) -> int:
        """
        Count requests for personal information.
        """
        personal_info_words = [
            'password', 'ssn', 'social security', 'credit card',
            'bank account', 'routing number', 'pin', 'ssn',
            'date of birth', 'mother\'s maiden name'
        ]
        
        text_lower = text.lower()
        count = 0
        for word in personal_info_words:
            count += text_lower.count(word)
        
        return count
    
    def _rule_based_classification(self, features: Dict[str, float]) -> Tuple[str, float]:
        """
        Rule-based classification as a fallback.
        """
        score = 0.0
        
        # Spam indicators
        if features['suspicious_words'] > 3:
            score += 0.3
        if features['caps_ratio'] > 0.3:
            score += 0.2
        if features['exclamation_count'] > 5:
            score += 0.2
        
        # Phishing indicators
        if features['urgent_words'] > 2:
            score += 0.3
        if features['personal_info_requests'] > 0:
            score += 0.4
        if features['suspicious_domains'] > 0:
            score += 0.3
        
        # Determine classification
        if score >= 0.7:
            return 'phishing', score
        elif score >= 0.4:
            return 'spam', score
        else:
            return 'legitimate', 1.0 - score
    
    def classify_email(self, email_content: str) -> Dict[str, any]:
        """
        Classify an email as legitimate, spam, or phishing.
        
        Args:
            email_content (str): The email content to classify
            
        Returns:
            Dict containing classification results
        """
        try:
            # Extract features
            features = self._extract_features(email_content)
            
            # For this demo, we'll use rule-based classification
            # In production, you would use the trained DistilBERT model
            classification, confidence = self._rule_based_classification(features)
            
            # Calculate individual scores
            scores = {
                'legitimate': 1.0 - confidence if classification == 'legitimate' else 0.1,
                'spam': confidence if classification == 'spam' else 0.1,
                'phishing': confidence if classification == 'phishing' else 0.1
            }
            
            # Normalize scores
            total_score = sum(scores.values())
            scores = {k: v / total_score for k, v in scores.items()}
            
            return {
                'classification': classification,
                'confidence': confidence,
                'scores': scores,
                'features': features
            }
            
        except Exception as e:
            logger.error(f"Error classifying email: {str(e)}")
            # Return default classification
            return {
                'classification': 'legitimate',
                'confidence': 0.5,
                'scores': {
                    'legitimate': 0.6,
                    'spam': 0.2,
                    'phishing': 0.2
                },
                'features': {}
            }
