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
class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Cherry_(including_sour)___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Grape___Black_rot','Grape___Esca_(Black_Measles)', 'Grape___healthy', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Peach___Bacterial_spot', 'Peach___healthy']

@app.get("/")
def index():
    return "Hello, I am alive"


@app.post("/predict")
async def predict(file : UploadFile = File(...)):
    #Read File
    image = read_image(await file.read())
    image = tf.image.resize(image,(224,224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    # # img_array
    predict = MODEL.predict(img_array)
    # return {
    #     'predict': predict[0].tolist()
    #         }
    pre = predict[0].tolist()
    confidence = max(pre)
    PREDICTED_CLASS = class_names[pre.index(confidence)]
    # # pass
    return {
        'class' : PREDICTED_CLASS,
        'confidence' : confidence
    }
    


if __name__ == "__main__":
    uvicorn.run(app, host='localhost',port=8021)