from fastapi import FastAPI, UploadFile, File, HTTPException
from tensorflow.keras.models import load_model
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import keras_cv
import base64
import io
from PIL import Image
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

try:
    model = load_model('my_model.h5', custom_objects={"DeepLabV3Plus": keras_cv.models.DeepLabV3Plus})
except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")

def preprocess_image(image):
    image = cv2.resize(image, (256, 256))
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def overlay_anomaly_on_image(image, mask):
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

    overlay = image.copy()
    overlay[mask > 0] = (0, 0, 255) 

    overlay_pil = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    buffered = io.BytesIO()
    overlay_pil.save(buffered, format="JPEG")
    overlay_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return overlay_base64

@app.post("/predict/")
async def predict_anomaly(file: UploadFile = File(...)):
    try:
        file_bytes = np.frombuffer(await file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading image: {e}")

    preprocessed_image = preprocess_image(image)

    try:
        prediction = model.predict(preprocessed_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model prediction: {e}")

    binary_mask = (prediction[0, :, :, 1] > 0.5).astype(np.uint8) * 255

    has_anomaly = bool(np.any(binary_mask > 0))

    overlay_base64 = overlay_anomaly_on_image(image, binary_mask)

    return {"anomaly_detected": has_anomaly, "overlay_image": overlay_base64}
def overlay_anomaly_on_image(image, mask):
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]))

    overlay = image.copy()
    overlay[mask > 0] = (0, 0, 255)  

    overlay_pil = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    buffered = io.BytesIO()
    overlay_pil.save(buffered, format="JPEG")
    overlay_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return overlay_base64

@app.post("/predict_multiple/")
async def predict_anomaly_multiple(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            file_bytes = np.frombuffer(await file.read(), np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image format")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading image: {e}")

        preprocessed_image = preprocess_image(image)

        try:
            prediction = model.predict(preprocessed_image)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during model prediction: {e}")

        binary_mask = (prediction[0, :, :, 1] > 0.5).astype(np.uint8) * 255

        has_anomaly = bool(np.any(binary_mask > 0))

        overlay_base64 = overlay_anomaly_on_image(image, binary_mask)

        results.append({
            "filename": file.filename,
            "anomaly_detected": has_anomaly,
            "overlay_image": overlay_base64
        })

    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
