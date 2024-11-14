from django.db import models
from django.utils import timezone
import re

# Create your models here.

class Alert(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    log_entry = models.TextField()
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)
    source_ip = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.attack_type}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)

class Rule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    pattern = models.TextField()
    severity = models.CharField(max_length=10, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])

    def __str__(self):
        return f"{self.name} ({self.severity})"

    @staticmethod
    def apply_rules(log_entry, request_ip=None):
        alerts = []
        rules = Rule.objects.all()
        
        # Cải thiện regex pattern để bắt IP
        ip_patterns = [
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',  # IPv4 thông thường
            r'(?:^|\s)(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4}(?:\s|$)',  # IPv6
            r'(?:^|\s)(?:[0-9A-Fa-f]{1,4}:){0,6}(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?:\s|$)'  # IPv4-mapped IPv6
        ]
        
        source_ip = None
        for pattern in ip_patterns:
            ip_match = re.search(pattern, log_entry)
            if ip_match:
                source_ip = ip_match.group(0).strip()
                break
        
        # Sử dụng request_ip nếu không tìm thấy IP trong log
        if not source_ip:
            source_ip = request_ip
        
        for rule in rules:
            script_pattern = re.compile(rule.pattern, re.IGNORECASE)
            if script_pattern.search(log_entry):
                alert = Alert(
                    attack_type=rule.name,
                    severity=rule.severity,
                    log_entry=log_entry,
                    source_ip=source_ip
                )
                alert.save()
                alerts.append(alert)
        return alerts

