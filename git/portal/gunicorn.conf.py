# Python 3.11 최적화된 Gunicorn 설정
import multiprocessing

# 서버 소켓
bind = "0.0.0.0:8001"
backlog = 2048

# Worker 프로세스
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# 타임아웃 설정
timeout = 30
keepalive = 2

# 로깅
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Python 3.11 최적화
preload_app = True
worker_tmp_dir = "/dev/shm"
