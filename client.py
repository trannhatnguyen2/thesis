from time import sleep
import requests
from loguru import logger
from pydantic import BaseModel

class TextIn(BaseModel):
    review: str

def predict():
    logger.info("Sending POST requests!")
    data = TextIn(review='Xấu tệ.')
    response = requests.post(
        "http://localhost:30000/predict",
        headers={
            "accept": "application/json",
        },
        data=data.json()
    )


if __name__ == "__main__":
    while True:
        predict()
        sleep(0.5)
