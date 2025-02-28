from django.db import models

class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'declined', 'Declined'

class SubscriptionChoices(models.TextChoices):
    MONTHLY = 'monthly', 'Monthly'
    YEARLY = 'yearly', 'Yearly' 

class LanguageChoices(models.TextChoices):
    ENGLISH = 'en', 'English'
    UZBEK = 'uz', 'Uzbek'
    RUSSIAN = 'ru', 'Russian'
