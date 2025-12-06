# Gunicorn 설정 파일
import multiprocessing
import os

# 워커 프로세스 수
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))

# 바인드 주소
bind = f"0.0.0.0:{os.getenv('PORT', 5000)}"

# 타임아웃 설정 (초)
timeout = 120

# 워커 클래스
worker_class = "gevent"

# 워커 연결 수
worker_connections = 1000

# 로그 설정
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 프로세스 이름
proc_name = "textai-backend"

