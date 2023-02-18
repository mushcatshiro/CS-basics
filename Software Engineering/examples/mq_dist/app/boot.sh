#!/bin/sh
cd /home/app
echo $MODE
if [ "$MODE" = "app" ]; then
    venv/bin/python app.py
elif [ "$MODE" = "client" ]; then
    venv/bin/rq worker -u redis://redis:6379/0
else
    echo "MODE not found $MODE"
fi