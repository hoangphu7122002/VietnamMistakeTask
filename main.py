import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel,conlist
from CorrectTeencode.corrector import correct_sent
from CorrectAccent.accent_model_LSTM import Model,returnRealOutput
from typing import List

app = FastAPI()
model = Model()

class Request(BaseModel):
    text: str

@app.post("/correctTeencode")
def teencode(data: Request):
    data = data.dict()
    corrected = correct_sent(data["text"])
    return {"result": corrected}

@app.post("/accent")
def accent(data: Request):
    data = data.dict()
    corrected = returnRealOutput(data["text"],model)
    return {"result": corrected}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)