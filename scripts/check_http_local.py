"""Start an isolated Gunicorn process, exercise real HTTP, then cleanly stop it."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import requests

root = Path(__file__).resolve().parents[1]
with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
environment = dict(os.environ, PORT=str(port), MLFLOW_DISABLE_AGENT_HINT="1")
log_path = root / "reports" / "http_server.log"
log_path.parent.mkdir(exist_ok=True)
with log_path.open("w") as log:
    process = subprocess.Popen([sys.executable, "-m", "business_app", "serve"], cwd=root, env=environment, stdout=log, stderr=subprocess.STDOUT)
    try:
        for _ in range(200):
            try:
                if requests.get(f"http://127.0.0.1:{port}/health", timeout=1).ok:
                    break
            except requests.RequestException:
                pass
            if process.poll() is not None:
                raise RuntimeError(log_path.read_text())
            time.sleep(0.1)
        else:
            raise TimeoutError("Serving process did not become ready")
        subprocess.run([sys.executable, str(root / "scripts" / "http_smoke.py"), "--base-url", f"http://127.0.0.1:{port}", "--output", str(root / "reports" / "http_smoke.json")], check=True, cwd=root)
        result = subprocess.run(["curl", "--fail", "--silent", "--show-error", "-H", "Content-Type: application/json", "-d", '{"industry":"2382","establishments":100,"previous_establishments":95}', f"http://127.0.0.1:{port}/predict"], check=True, capture_output=True, text=True)
        (root / "reports" / "curl_prediction.json").write_text(result.stdout)
        print("Actual curl request passed")
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
