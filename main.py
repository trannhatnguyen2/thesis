from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from loguru import logger
from time import time 

from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server

from app.model import predict_pipeline
from app.preprocess.preprocessing  import preprocessing


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

set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "sentiment-service-manual"}))
)
tracer = get_tracer_provider().get_tracer("mysentiment", "0.1.2")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()

class TextIn(BaseModel):
    review: str

class PredictionOut(BaseModel):
    sentiment: str

@app.get('/')
async def home():
    return {'script': "Nguyen's Thesis"}

@app.post("/predict", response_model=PredictionOut)
async def predict(payload: TextIn):

    starting_time = time()

    label = {"api": "/predict"}

    counter.add(10, label)

    if payload.review != '':
        with tracer.start_as_current_span("processors") as processors:
            with tracer.start_as_current_span(
                "preprocessing", links=[trace.Link(processors.get_span_context())]
            ):
                review_handled = preprocessing(payload.review)

            with tracer.start_as_current_span(
                "predictor", links=[trace.Link(processors.get_span_context())]
            ):
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
    FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host='0.0.0.0', port=30000)




# from fastapi import FastAPI
# import uvicorn
# from pydantic import BaseModel
# from loguru import logger

# from model.model import predict_pipeline
# from preprocess.preprocessing import preprocessing

# cache = {}

# app = FastAPI()

# class TextIn(BaseModel):
#     review: str

# class PredictionOut(BaseModel):
#     sentiment: str

# @app.get('/')
# async def home():
#     return {'text': "Nguyen's Thesis"}

# @app.post("/predict", response_model=PredictionOut)
# async def predict(payload: TextIn):

#     if payload.review != '':
#         review_handled = preprocessing(payload.review)
#         sentiment = predict_pipeline(review_handled)

#     return {"sentiment": sentiment}

# if __name__ == '__main__':
#     uvicorn.run(app)

