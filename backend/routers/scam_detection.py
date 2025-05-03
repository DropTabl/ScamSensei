from fastapi import APIRouter,Query
from backend.scam_detection.detect import detect_scam
from fastapi import HTTPException


router = APIRouter()


@router.get("/")
async def process_text(
    text: str = Query(..., description="Text to process"),
    language: str = Query("en", description="Language of the text (default: en)")
):
    try:
        scam_indicators, score = await  detect_scam(text, language)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "scam_indicators": scam_indicators,
        "score": score,
        "language": language
    }
