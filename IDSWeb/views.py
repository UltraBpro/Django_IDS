from django.shortcuts import render
from django.views.generic import ListView
from .models import Alert
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class AlertListView(ListView):
    model = Alert
    template_name = 'alert_list.html'
    context_object_name = 'alerts'
    ordering = ['-timestamp']

    def get_queryset(self):
        queryset = super().get_queryset()
        for alert in queryset:
            alert.timestamp = alert.timestamp.astimezone(timezone.get_current_timezone())
        return queryset
