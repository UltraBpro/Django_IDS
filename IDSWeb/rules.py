import re

def apply_rules(log_entry):
    alerts = []
    if sql_injection(log_entry):
        print("SQL Injection")
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "SQL Injection",
            "severity": "High"
        })
    if xss_attack(log_entry):
        print("XSS Attack")
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "XSS Attack",
            "severity": "Medium"
        })
    if csrf_attack(log_entry):
        print("CSRF Attack")
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "CSRF Attack",
            "severity": "Medium"
        })
    # Thêm các quy tắc khác ở đây
    return alerts

def sql_injection(log_entry):
    # Kiểm tra các mẫu SQL injection tiềm ẩn trong toàn bộ log entry
    suspicious_patterns = [
        r"(\s|^)UNION(\s|$)",
        r"(\s|^)OR\s+1\s*=\s*1(\s|$)",
        r"(\s|^)AND\s+1\s*=\s*1(\s|$)",
        r"(\s|^)--",
        r"(\s|^)#",
        r"(\s|^)\/\*.*?\*\/",
        r"'(\s|^)OR(\s|$)'",
        r"'(\s|^)AND(\s|$)'",
        r"(\s|^)SLEEP\s*\(",
        r"(\s|^)BENCHMARK\s*\(",
        r"(\s|^)WAITFOR\s+DELAY",
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, log_entry, re.IGNORECASE):
            # Kiểm tra xem mẫu đáng ngờ có nằm trong phần tham số của truy vấn không
            if "args=" in log_entry:
                args_start = log_entry.index("args=")
                if re.search(pattern, log_entry[args_start:], re.IGNORECASE):
                    return True
            else:
                return True
    
    return False

def xss_attack(log_entry):
    pattern = r"(<script>|<\/script>|javascript:)"
    return bool(re.search(pattern, log_entry, re.IGNORECASE))

def csrf_attack(log_entry):
    pattern = r"(Forbidden \(CSRF token (missing|incorrect).*?\)|CSRF verification failed)"
    return bool(re.search(pattern, log_entry, re.IGNORECASE))

# Thêm các quy tắc khác tùy theo nhu cầu
