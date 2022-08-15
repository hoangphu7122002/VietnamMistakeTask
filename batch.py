import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel,conlist
from CorrectTeencode.corrector import correct_sent
from CorrectAccent.accent_model_LSTM import Model,returnRealOutput
from typing import List
from predictEmotion.predict import predictBatch


app = FastAPI()
model = Model()

class BatchRequest(BaseModel):
    batches: List[conlist(item_type=str)]

@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. This new version allows for batching. Now head over to http://localhost:81/docs"

@app.post("/batch-teencode")
def predict(batch: BatchRequest):
    batches = batch.batches[0]
    pred = []
    for text in batches:
        corrected = correct_sent(text)
        pred.append(corrected)
    return {"Prediction": pred}

@app.post("/accent")
def accent(batch: BatchRequest):
    batches = batch.batches[0]
    pred = []
    for text in batches:
        corrected = returnRealOutput(text,model)
        pred.append(corrected)
    return {"Prediction": pred}

@app.post("/emotion")
def emotion(batch: BatchRequest):
    batches = batch.batches[0]
    batches = [returnRealOutput(correct_sent(text),model)  for text in batches]
    return {"Prediction": predictBatch(batches)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)