FROM python:3.9-slim AS compile-image

WORKDIR /app

COPY requirements.txt .

RUN pip install --prefix=/install -r requirements.txt --no-cache-dir


FROM python:3.9

WORKDIR /app

COPY ./app /app/app

COPY ./main.py /app/

COPY ./model_storage /app/model_storage

COPY --from=compile-image /install /usr/local

EXPOSE 30000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]