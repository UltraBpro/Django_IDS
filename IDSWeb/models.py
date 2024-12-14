from django.db import models
from django.utils import timezone
import re

# Create your models here.

class Alert(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    log_entry = models.TextField()
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.attack_type}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)

class Rule(models.Model):
    SEVERITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    name = models.CharField(max_length=100)
    pattern = models.TextField(help_text="Regular expression pattern to match")
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.attack_type})"

    def match(self, log_entry):
        try:
            return bool(re.search(self.pattern, log_entry, re.IGNORECASE))
        except re.error:
            return False
