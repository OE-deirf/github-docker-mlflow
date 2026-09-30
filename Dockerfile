FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/churn/ ./churn/
COPY dvc.yaml  ./dvc.yaml
COPY params.yaml  ./params.yaml

CMD ["dvc", "repro"]
