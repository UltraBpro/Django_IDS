import re
from .models import Rule, Alert

def extract_ip(log_entry):
    ip_pattern = r'\[([\d\.]+)\]'
    match = re.search(ip_pattern, log_entry)
    if match:
        return match.group(1)
    return None

def apply_rules(log_entry):
    alerts = []
    ip = extract_ip(log_entry)
    
    # Lấy tất cả rules đang active
    active_rules = Rule.objects.filter(is_active=True)
    
    for rule in active_rules:
        if rule.match(log_entry):
            print(f"{rule.attack_type} detected")
            alerts.append({
                "log_entry": log_entry,
                "attack_type": rule.attack_type,
                "severity": rule.severity,
                "ip_address": ip
            })
    
    return alerts
