# FROM anibali/pytorch:2.0.1-cuda11.8-ubuntu22.04

FROM python:3.9

WORKDIR /app

LABEL maintainer="nguyentn"

COPY ./app /app/app

COPY ./main.py /app/

COPY ./model_storage /app/model_storage

COPY ./requirements.txt /app/

EXPOSE 30000

RUN pip install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
