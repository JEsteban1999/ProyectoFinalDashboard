import multiprocessing
import os

workers = 1
threads = 1
timeout = 300
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"
worker_class = "sync"
preload_app = True