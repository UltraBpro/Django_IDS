import time
import requests
import json
from sseclient import SSEClient
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
            
            alerts = apply_rules(line)
            for alert in alerts:
                Alert.objects.create(**alert)

def analyze_stream(stream_url):
    """Analyze logs from SSE stream"""
    try:
        response = requests.get(stream_url, stream=True)
        client = SSEClient(response)
        for event in client.events():
            if event.data:
                # Xử lý log line từ stream
                alerts = apply_rules(event.data)
                for alert in alerts:
                    Alert.objects.create(**alert)
    except Exception as e:
        print(f"Stream error: {e}")
        time.sleep(5)  # Đợi trước khi thử lại
        return analyze_stream(stream_url)  # Thử kết nối lại
