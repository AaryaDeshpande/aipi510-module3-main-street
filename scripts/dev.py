"""Development preview adapter; accepts the preview runner's host/port options."""
import argparse
import os
import sys
parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", type=int, default=8080)
parser.add_argument("--strictPort", action="store_true")
args = parser.parse_args()
os.execv(sys.executable, [sys.executable, "-m", "gunicorn", "--bind", f"{args.host}:{args.port}", "--workers", "1", "--threads", "4", "--timeout", "60", "business_app.wsgi:app"])
