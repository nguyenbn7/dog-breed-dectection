from io import BytesIO
import json
from predicted_classes import dog_breeds

from os import path
import logging

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import numpy as np

from tensorflow import keras, get_logger, nn, expand_dims, math
from keras.models import load_model
from keras.utils import load_img, img_to_array

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

IMG_SIZE = 224
model_name = "custom-mobilenetv2-Adam.h5"
model = load_model(path.join(".", "model", model_name))


def process_image(image_bytes_io: BytesIO):

    image = load_img(image_bytes_io, target_size=(IMG_SIZE, IMG_SIZE))
    image_array = img_to_array(image)
    return expand_dims(image_array, 0) / 255.0


@app.get("/")
def root():
    return {"Message": "Nothing in here"}


@app.post("/predict")
async def predict_image_base_64(image_file: UploadFile):
    image_bytes = bytearray(await image_file.read())
    img = process_image(BytesIO(image_bytes))

    pred = model.predict(img)
    score = nn.softmax(pred[0])

    max_idx = np.argmax(score)
    class_prediction = dog_breeds[max_idx]

    top_5 = math.top_k(score, 5)

    top_5_values = top_5.values.numpy()
    top_5_indices = top_5.indices.numpy()

    top_5_preds_scores = {
        dog_breeds[top_5_indices[i]]: round(top_5_values[i] * 100, 2) for i in range(5)
    }

    return {
        "model-prediction": class_prediction,
        "model-prediction-confidence-score-percentage": top_5_preds_scores[
            class_prediction
        ],
        "model-top-5-predictions-scores-percentage": top_5_preds_scores,
    }
