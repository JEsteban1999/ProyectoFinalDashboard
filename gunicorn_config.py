import multiprocessing

workers = 1
threads = 2
timeout = 120
bind = "0.0.0.0:8080"
worker_class = "sync"
keepalive = 5