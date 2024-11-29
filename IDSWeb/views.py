from django.shortcuts import render
from django.views.generic import ListView
from .models import Alert
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

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

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            last_id = request.GET.get('last_id', 0)
            new_alerts = Alert.objects.filter(id__gt=last_id).order_by('id')
            data = []
            for alert in new_alerts:
                data.append({
                    'id': alert.id,
                    'timestamp': alert.timestamp.astimezone(timezone.get_current_timezone()).isoformat(),
                    'attack_type': alert.attack_type,
                    'severity': alert.severity,
                    'log_entry': alert.log_entry
                })
            return JsonResponse(data, safe=False)
        return super().get(request, *args, **kwargs)
