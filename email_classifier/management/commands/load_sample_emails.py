"""
Management command to load sample emails for testing.
"""
from django.core.management.base import BaseCommand
from email_classifier.models import EmailSample


class Command(BaseCommand):
    help = 'Load sample emails for testing the classification system'

    def handle(self, *args, **options):
        """
        Load sample emails into the database.
        """
        sample_emails = [
            {
                'subject': 'Meeting Reminder',
                'content': 'Hi John, I hope you\'re doing well. I wanted to follow up on our meeting yesterday about the project proposal. Could you please send me the updated document by Friday? Thanks!',
                'classification': 'legitimate'
            },
            {
                'subject': 'Project Update',
                'content': 'Hello team, I wanted to update you on the progress of our current project. We have completed 75% of the tasks and are on track to meet the deadline. Please let me know if you have any questions.',
                'classification': 'legitimate'
            },
            {
                'subject': 'Invoice #12345',
                'content': 'Dear Customer, Your invoice #12345 for $299.99 is due on 2024-01-15. Please make payment through our secure portal. Thank you for your business.',
                'classification': 'legitimate'
            },
            {
                'subject': 'URGENT! WIN $1000 CASH PRIZE!',
                'content': 'CONGRATULATIONS! You have been selected to win $1000 CASH PRIZE! Click here now to claim your prize! Limited time offer! Don\'t miss out!',
                'classification': 'spam'
            },
            {
                'subject': 'FREE MONEY - LIMITED TIME OFFER',
                'content': 'Get rich quick! Make $5000 in just one week! No experience needed! Click here to start earning money today! Guaranteed results!',
                'classification': 'spam'
            },
            {
                'subject': 'You\'ve Won a Free iPhone!',
                'content': 'Congratulations! You\'ve won a free iPhone 15! Click here to claim your prize now! Limited time offer! Don\'t miss out!',
                'classification': 'spam'
            },
            {
                'subject': 'Your Account Has Been Suspended',
                'content': 'Your account has been suspended due to suspicious activity. Please verify your identity by clicking the link below and entering your password and social security number to restore access.',
                'classification': 'phishing'
            },
            {
                'subject': 'Urgent: Verify Your Bank Account',
                'content': 'We have detected unusual activity on your bank account. Please click here to verify your account information immediately to prevent unauthorized access.',
                'classification': 'phishing'
            },
            {
                'subject': 'Update Your Payment Information',
                'content': 'Your payment method has expired. Please update your credit card information by clicking the link below to avoid service interruption.',
                'classification': 'phishing'
            },
            {
                'subject': 'Security Alert - Unusual Login',
                'content': 'We detected a login from an unrecognized device. If this wasn\'t you, please secure your account immediately by clicking here and changing your password.',
                'classification': 'phishing'
            }
        ]

        created_count = 0
        for email_data in sample_emails:
            email_sample, created = EmailSample.objects.get_or_create(
                subject=email_data['subject'],
                defaults={
                    'content': email_data['content'],
                    'classification': email_data['classification'],
                    'is_verified': True
                }
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {created_count} sample emails'
            )
        )
