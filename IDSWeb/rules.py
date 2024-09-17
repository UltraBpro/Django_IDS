import re

def apply_rules(log_entry):
    alerts = []
    if sql_injection(log_entry):
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "SQL Injection",
            "severity": "High"
        })
    if xss_attack(log_entry):
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "XSS Attack",
            "severity": "Medium"
        })
    # Thêm các quy tắc khác ở đây
    return alerts

def sql_injection(log_entry):
    pattern = r"(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|TABLE|FROM|WHERE|AND|OR)\s"
    return bool(re.search(pattern, log_entry, re.IGNORECASE))

def xss_attack(log_entry):
    pattern = r"(<script>|<\/script>|javascript:)"
    return bool(re.search(pattern, log_entry, re.IGNORECASE))

# Thêm các quy tắc khác tùy theo nhu cầu
