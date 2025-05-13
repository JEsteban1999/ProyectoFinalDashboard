import multiprocessing

workers = 1
threads = 1
timeout = 300
bind = "0.0.0.0:$PORT"
worker_class = "sync"
preload_app = True