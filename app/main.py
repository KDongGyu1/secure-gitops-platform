from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from routers import health

app = FastAPI(title="Secure GitOps Platform")

# 라우터 등록
app.include_router(health.router)

# Prometheus 메트릭 자동 생성
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root() -> dict:
    return {"message": "Secure GitOps Platform is running"}