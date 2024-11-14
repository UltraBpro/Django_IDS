from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Rule, Alert
from django.utils import timezone
from django.http import JsonResponse
from .forms import RuleForm, PatternForm

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
                    'timestamp': alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'attack_type': alert.attack_type,
                    'severity': alert.severity,
                    'source_ip': alert.source_ip or request.client_ip,
                    'log_entry': alert.log_entry
                })
            return JsonResponse(data, safe=False)
        return super().get(request, *args, **kwargs)

def add_rule_view(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('IDSWeb:alert_list') 
    else:
        form = RuleForm()
    return render(request, 'add_rule.html', {'form': form})

def edit_pattern(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    rule = get_object_or_404(Rule, name=alert.attack_type) 

    if request.method == 'POST':
        form = PatternForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('IDSWeb:alert_list')  # Redirect về danh sách alert sau khi lưu
    else:
        form = PatternForm(instance=rule)

    return render(request, 'edit_pattern.html', {'form': form, 'alert': alert})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Trong view xử lý log, thêm IP từ request
def process_log(request):  # Giả sử đây là view xử lý log của bạn
    log_entry = request.POST.get('log_entry')  # hoặc cách khác để lấy log
    client_ip = get_client_ip(request)
    
    alerts = Rule.apply_rules(log_entry, request_ip=client_ip)
    # ... xử lý tiếp ...

def process_log_entry(request, log_entry):
    # Lấy IP từ request đã được xử lý bởi middleware
    client_ip = request.client_ip
    
    # Áp dụng rules và truyền IP vào
    alerts = Rule.apply_rules(log_entry, request_ip=client_ip)
    return alerts