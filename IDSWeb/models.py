from django.db import models

# Create your models here.

class Alert(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    log_entry = models.TextField()
    attack_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.timestamp} - {self.attack_type}"
