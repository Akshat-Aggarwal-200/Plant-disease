from fastapi import FastAPI, UploadFile, File
import uvicorn
from io import BytesIO
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf
import os
from fastapi.middleware.cors import CORSMiddleware


def read_image(image_encodd) -> np.ndarray:
    pil_image = np.array(Image.open(BytesIO(image_encodd)))
    return pil_image


app = FastAPI()


origin = ["http://localhost","http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MODEL = tf.keras.models.load_model("model\classifiers")
class_names = os.listdir("dataset")

@app.get("/")
def index():
    return "Hello, I am alive"


@app.post("/predict")
async def predict(file : UploadFile = File(...)):
    #Read File
    image = read_image(await file.read())
    img_batch = np.expand_dims(image,0)
    predict = MODEL.predict(img_batch)
    PREDICTED_CLASS = class_names[np.argmax(predict[0])]
    confidence = np.argmax(predict[0])
    return {
        'class' : PREDICTED_CLASS,
        'confidence' : confidence
    }
    


if __name__ == "__main__":
    uvicorn.run(app, host='localhost',port=8021)