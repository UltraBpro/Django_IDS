from django.db import models
from django.utils import timezone

# Create your models here.

class Alert(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    log_entry = models.TextField()
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.timestamp} - {self.attack_type}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.timestamp = timezone.now()
        super().save(*args, **kwargs)
