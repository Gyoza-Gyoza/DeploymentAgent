from pathlib import Path
import subprocess

def deploy():
    try:
        deploy_path = Path("/home/deploy/chipin-api/deploy.sh")
        logs = subprocess.run(["bash", deploy_path], check = True, capture_output = True, text = True)
        print(logs.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(e.stderr)
        return False
