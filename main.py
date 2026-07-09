from fastapi import FastAPI, status, Request, HTTPException
import os
from pathlib import Path
import subprocess
from dotenv import load_dotenv
import secrets

load_dotenv()


app = FastAPI()

@app.post(
    "/deploy",
status_code = status.HTTP_200_OK)
def try_deploy(request: Request):
    if authorize(request):
        try:
            deploy_path = Path("/home/deploy/chipin-api/deploy.sh")
            logs = subprocess.run(["bash", deploy_path], check=True, capture_output=True, text=True)
            print(logs.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print("Return code:", e.returncode)
            print("STDOUT:")
            print(e.stdout)
            print("STDERR:")
            print(e.stderr)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.stderr)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

def authorize(request: Request):
    auth_header = request.headers.get("Authorization")
    deploy_token = f"Bearer {os.getenv('DEPLOY_TOKEN')}"

    if secrets.compare_digest(auth_header, deploy_token):
        return True
    else:
        return False
