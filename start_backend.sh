#!/bin/bash
# Backend startup script - ALWAYS uses venv Python
cd /home/learnify/lt/learnify-teach/backend
./venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
