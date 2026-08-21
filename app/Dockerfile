# 베이스 이미지
FROM python:3.11-slim

# 작업 디렉토리
WORKDIR /app

# 의존성 먼저 복사 (레이어 캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 포트 노출
EXPOSE 8080

# 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]