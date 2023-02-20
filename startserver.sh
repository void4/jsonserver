gunicorn -w 1 --threads 1 main:app -b 127.0.0.1:1337 --worker-class eventlet --reload --access-logfile - | tee access.log
