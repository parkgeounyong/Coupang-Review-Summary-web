# 베이스 이미지 설정
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 소스 코드 복사
COPY . .

# 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 포트 노출
EXPOSE 5000

# 서버 실행
CMD ["python", "application.py"]