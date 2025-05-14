import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 1
timeout = 120
bind = "0.0.0.0:10000"
preload_app = True
