from django.shortcuts import render
from django.views.generic import ListView
from .models import Alert

# Create your views here.

class AlertListView(ListView):
    model = Alert
    template_name = 'alert_list.html'
    context_object_name = 'alerts'
    ordering = ['-timestamp']
