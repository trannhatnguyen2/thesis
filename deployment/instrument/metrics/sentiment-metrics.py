from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from loguru import logger
from time import time 

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server

from model import predict_pipeline
from preprocess.preprocessing  import preprocessing


# Start Prometheus client
start_http_server(port=8099, addr="0.0.0.0")

# Service name is required for most backends
resource = Resource(attributes={SERVICE_NAME: "sentiment-service"})

# Exporter to export metrics to Prometheus
reader = PrometheusMetricReader()

# Meter is responsible for creating and recording metrics
provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("mysentiment", "0.1.2")

# Create your first counter
counter = meter.create_counter(
    name="Sentiment_request_counter",
    description="Number of Sentiment requests"
)

histogram = meter.create_histogram(
    name="Sentiment_response_histogram",
    description="Sentiment response histogram",
    unit="seconds",
)

app = FastAPI()

class TextIn(BaseModel):
    review: str

class PredictionOut(BaseModel):
    sentiment: str

@app.post("/predict", response_model=PredictionOut)
async def predict(payload: TextIn):

    starting_time = time()

    label = {"api": "/predict"}

    counter.add(10, label)

    if payload.review != '':
        review_handled = preprocessing(payload.review)
        sentiment = predict_pipeline(review_handled)

        ending_time = time()
        elapsed_time = ending_time - starting_time
        logger.info("elapsed time: ", elapsed_time)
        logger.info(elapsed_time)
        histogram.record(elapsed_time, label)

        return {"sentiment": sentiment}
    else:
        ending_time = time()
        elapsed_time = ending_time - starting_time
        logger.info("elapsed time: ", elapsed_time)
        logger.info(elapsed_time)
        histogram.record(elapsed_time, label)

        return {"error": "Please try again!"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)