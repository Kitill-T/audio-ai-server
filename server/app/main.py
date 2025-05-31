from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from asr.whisper import transcribe_audio
from llm.openai_client import generate_response
import os
from tempfile import NamedTemporaryFile

app = FastAPI()

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/api/process_audio")
async def process_audio(file: UploadFile):
    try:
        with NamedTemporaryFile(delete=True, suffix=".wav") as temp_audio:
            temp_audio.write(await file.read())

            # Транскрибация
            text = transcribe_audio(temp_audio.name)

            # Генерация ответа
            response = generate_response(text)

            return {
                "transcription": text,
                "ai_response": response
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))