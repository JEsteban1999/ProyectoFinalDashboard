import multiprocessing

workers = 1
threads = 1
timeout = 180
bind = "0.0.0.0:$PORT"
worker_class = "sync"
keepalive = 5