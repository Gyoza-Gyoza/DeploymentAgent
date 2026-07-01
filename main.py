from fastapi import FastAPI, status
from deploy import deploy

app = FastAPI()

@app.post(
    "/deploy",
status_code = status.HTTP_200_OK)
def try_deploy():
    deploy()
