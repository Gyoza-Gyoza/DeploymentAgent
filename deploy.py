import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv

load_dotenv()

from fastapi import Request, HTTPException
import secrets

def deploy(request: Request):
    auth_header = request.headers.get("Authorization")
    deploy_token = f"Bearer {os.getenv('DEPLOY_TOKEN')}"
    print(f"Received: {repr(auth_header)}")
    print(f"Expected: {repr(deploy_token)}")
    if secrets.compare_digest(auth_header, deploy_token):
        try:
            deploy_path = Path("/home/deploy/chipin-api/deploy.sh")
            logs = subprocess.run(["bash", deploy_path], check = True, capture_output = True, text = True)
            print(logs.stdout)
            return True
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code = e.returncode, detail = e.stderr)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")