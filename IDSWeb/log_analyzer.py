import time
from .models import Alert, Rule

def analyze_log(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_file.seek(0, 2)  # Di chuyển con trỏ đến cuối file
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.1)  # Đợi nếu không có dữ liệu mới
                continue
            
            # Áp dụng các quy tắc từ cơ sở dữ liệu sử dụng hàm apply_rules
            alerts = Rule.apply_rules(line)
            
            # Các đối tượng Alert đã được lưu trong apply_rules, không cần lưu lại
            for alert in alerts:
                print(f"Alert created: {alert}")
