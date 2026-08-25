from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from database import Base, engine
from routers import health, items

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure GitOps Platform")

# 라우터 등록
app.include_router(health.router)
app.include_router(items.router)

# Prometheus 메트릭 자동 생성
Instrumentator().instrument(app).expose(app)


@app.get("/")
def root() -> dict:
    return {"message": "Secure GitOps Platform is running"}