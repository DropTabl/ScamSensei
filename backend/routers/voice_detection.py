from fastapi import APIRouter,Query
from backend.scam_detection.detect import detect_scam
from backend.voice_detector.v_detect import transcribe_audio_file
from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import os
from fastapi import HTTPException

router = APIRouter()




@router.post("/")
async def upload_audio(
    file: UploadFile = File(...),
    language: str = Query("en", description="Language of the audio (default: en)")
):
    if not file.filename.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Only .mp3 files are supported.")

    temp_filename = f"/tmp/{uuid.uuid4()}.mp3"

    with open(temp_filename, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        # Transcribe audio
        text = transcribe_audio_file(temp_filename, language=language)
        scam_indicators, score = await  detect_scam(text, language=language)

        print("Transcribed text:", text)

        return {
            "transcription": text,
            "scam_indicators": scam_indicators,
            "score": score,
            "language": language
        }

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)