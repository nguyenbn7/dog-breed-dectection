from predicted_classes import dog_breeds

from os import path
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from numpy import argmax

from tensorflow import keras, get_logger
from keras.models import load_model
from keras.utils import get_file, load_img, img_to_array
from tensorflow import expand_dims
from tensorflow import nn

get_logger().setLevel(logging.ERROR)

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


model_name = "custom-mobilenetv2-Adam.h5"
model = load_model(path.join(".", "model", model_name))


@app.get("/")
def root():
    return {"Message": "Nothing in here"}


@app.get("/predict/image/link")
async def predict_dog_image(image_link=""):
    if not image_link:
        return {"Message": "No image link provided"}

    image_path = get_file(origin=image_link)

    image = load_img(image_path, target_size=(224, 224))

    img_array = img_to_array(image)
    img_array = expand_dims(img_array, 0)

    pred = model.predict(img_array)
    score = nn.softmax(pred[0])

    max_idx = argmax(score)
    class_prediction = dog_breeds[max_idx]
    model_score = round(score[max_idx].numpy() * 100, 2)

    return {
        "model-prediction": class_prediction,
        "model-prediction-confidence-score": model_score,
    }
