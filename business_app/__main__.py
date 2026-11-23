from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Main Street Business Explorer")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("prepare")
    training = commands.add_parser("train")
    training.add_argument("--data-uri")
    training.add_argument("--output-dir", type=Path)
    commands.add_parser("serve")
    commands.add_parser("verify")
    upload = commands.add_parser("upload-data")
    upload.add_argument("--bucket", required=True)
    upload.add_argument("--object", default="aipi510-module3/business-panel.csv")
    args = parser.parse_args()
    if args.command == "prepare":
        from .prepare import prepare
        result = prepare()
    elif args.command == "train":
        from .train import train_project
        result = train_project(args.data_uri, args.output_dir)
    elif args.command == "serve":
        os.execv(sys.executable, [sys.executable, "-m", "gunicorn", "--bind", "0.0.0.0:" + os.environ.get("PORT", "8080"), "--workers", "1", "--threads", "4", "--timeout", "60", "business_app.wsgi:app"])
        return
    elif args.command == "verify":
        from .verify import verify
        result = verify()
    else:
        from .cloud import upload_data
        result = upload_data(args.bucket, args.object)
    print(json.dumps(result, indent=2, allow_nan=False))

if __name__ == "__main__":
    main()
