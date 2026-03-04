import os
import logging
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agent import llama_agent

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Spam Detection Agent", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "🛡️ AI Spam Detection Agent is running!"}

@app.post("/analyze")
async def analyze(text: str = Form(None), file: UploadFile = File(None)):

    if not text and not file:
        raise HTTPException(
            status_code=400,
            detail="Provide either text or an image file."
        )

    # Text case
    if text:
        return llama_agent(user_input=text)

    # Image case
    if file:
        image_path = "temp_image.jpg"

        with open(image_path, "wb") as f:
            f.write(await file.read())

        try:
            return llama_agent(image_path=image_path)
        finally:
            if os.path.exists(image_path):
                os.remove(image_path)

@app.exception_handler(Exception)
def handle_exception(request, exc):
    logging.error(f"Error: {exc}")
    return JSONResponse(status_code=500, content={"error": str(exc)})