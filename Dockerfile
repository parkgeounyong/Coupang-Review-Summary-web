# 베이스 이미지로 Python 3.9 버전을 사용합니다.
FROM python:3.9

# 작업 디렉토리를 설정합니다.
WORKDIR /app

# 필요한 패키지를 설치합니다.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*



# 소스 코드를 복사합니다.
COPY . .

# Flask 실행을 위해 필요한 환경변수를 설정합니다.
ENV FLASK_APP=server.py

# 서버를 실행합니다.
CMD ["flask", "run", "--host", "0.0.0.0"]