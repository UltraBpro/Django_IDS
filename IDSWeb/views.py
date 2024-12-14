from django.shortcuts import render
from django.views.generic import ListView
from .models import Alert, Rule
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
import json
from datetime import datetime

# Create your views here.

class AlertListView(ListView):
    model = Alert
    template_name = 'alert_list.html'
    context_object_name = 'alerts'
    ordering = ['-timestamp']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Xử lý sort
        sort_by = self.request.GET.get('sort', '-timestamp')
        if sort_by.startswith('-'):
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by(sort_by)
            
        # Lọc theo attack_type
        attack_type = self.request.GET.get('attack_type')
        if attack_type:
            queryset = queryset.filter(attack_type=attack_type)
            
        # Lọc theo severity
        severity = self.request.GET.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
            
        # Lọc theo khoảng thời gian
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)

        # Chuyển đổi timezone
        for alert in queryset:
            alert.timestamp = alert.timestamp.astimezone(timezone.get_current_timezone())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Thêm thông tin sort hiện tại
        context['current_sort'] = self.request.GET.get('sort', '-timestamp')
        # Thêm các giá trị unique cho các dropdown
        context['attack_types'] = Alert.objects.values_list('attack_type', flat=True).distinct()
        context['severities'] = Alert.objects.values_list('severity', flat=True).distinct()
        return context

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
                    'ip_address': alert.ip_address,
                    'log_entry': alert.log_entry
                })
            return JsonResponse(data, safe=False)
        return super().get(request, *args, **kwargs)

class RuleListView(ListView):
    model = Rule
    template_name = 'rule_list.html'
    context_object_name = 'rules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_import_export'] = True
        return context


class RuleDeleteView(DeleteView):
    model = Rule
    success_url = reverse_lazy('IDSWeb:rule_list')
    template_name = 'rule_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Rule "{self.get_object().name}" was successfully deleted.')
        return super().delete(request, *args, **kwargs)

@require_http_methods(["POST"])
def export_rules(request):
    rules = Rule.objects.all()
    rules_data = []
    
    for rule in rules:
        rules_data.append({
            'name': rule.name,
            'pattern': rule.pattern,
            'attack_type': rule.attack_type,
            'severity': rule.severity,
            'is_active': rule.is_active
        })
    
    response = HttpResponse(
        json.dumps(rules_data, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="ids_rules_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response

@require_http_methods(["POST"])
def import_rules(request):
    try:
        if 'rules_file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        rules_file = request.FILES['rules_file']
        if not rules_file.name.endswith('.json'):
            return JsonResponse({'error': 'File must be JSON format'}, status=400)
        
        rules_data = json.loads(rules_file.read())
        
        # Validate rules format
        required_fields = ['name', 'pattern', 'attack_type', 'severity']
        for rule in rules_data:
            if not all(field in rule for field in required_fields):
                return JsonResponse({'error': 'Invalid rule format'}, status=400)
        
        # Clear existing rules if specified
        if request.POST.get('clear_existing') == 'true':
            Rule.objects.all().delete()
        
        # Import new rules
        for rule_data in rules_data:
            Rule.objects.create(**rule_data)
        
        messages.success(request, f'Successfully imported {len(rules_data)} rules')
        return JsonResponse({'message': f'Successfully imported {len(rules_data)} rules'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON file'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
