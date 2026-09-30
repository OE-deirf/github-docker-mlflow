FROM python:3.12-slim
RUN pip install -v --no-cache-dir boto3==1.43.75
COPY src/docker/init_bucket.py /init_bucket.py
CMD ["python", "/init_bucket.py"]
