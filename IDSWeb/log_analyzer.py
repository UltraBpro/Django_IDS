import time
from .models import Alert
from .rules import apply_rules

def analyze_log(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)  # Di chuyển con trỏ đến cuối file
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.1)  # Đợi nếu không có dữ liệu mới
                continue
            
            # Áp dụng các quy tắc
            print(line);
            alerts = apply_rules(line)
            for alert in alerts:
                Alert.objects.create(**alert)
