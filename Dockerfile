# 사용할 Python 버전을 지정합니다. (현재 3.12.7로 설정됨)
FROM python:3.10-slim-bullseye
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 복사
COPY . /app/

# 포트 노출
EXPOSE 8000

# 애플리케이션 시작 명령
CMD ["gunicorn", "galatea.wsgi:application", "--bind", "0.0.0.0:8000"]
