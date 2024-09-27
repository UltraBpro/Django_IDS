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
    if file_upload_vulnerability(log_entry):
        print("File Upload Vulnerability")
        alerts.append({
            "log_entry": log_entry,
            "attack_type": "File Upload Vulnerability",
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
    pattern = r"(Forbidden \(CSRF cookie|token (missing|incorrect|not set).*?\)|CSRF verification failed)"
    return bool(re.search(pattern, log_entry, re.IGNORECASE))

def file_upload_vulnerability(log_entry):
    dangerous_extensions = [
        r"\.php",
        r"\.phtml",
        r"\.php3",
        r"\.php4",
        r"\.php5",
        r"\.phps",
        r"\.asp",
        r"\.aspx",
        r"\.jsp",
        r"\.jspx",
        r"\.exe",
        r"\.dll",
        r"\.bat",
        r"\.cmd",
        r"\.sh",
        r"\.cgi",
        r"\.pl",
        r"\.py",
        r"\.rb",
    ]
    
    pattern = r'"\w+\s+.*?/media/.*?({})'.format('|'.join(dangerous_extensions))
    return bool(re.search(pattern, log_entry, re.IGNORECASE))


# Thêm các quy tắc khác tùy theo nhu cầu
