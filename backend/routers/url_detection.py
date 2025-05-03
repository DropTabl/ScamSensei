from fastapi import APIRouter, Query
from backend.url_checking.url_check import main
import asyncio
from fastapi import HTTPException


router = APIRouter()



@router.get("/")
async def process_text(
    url: str = Query(..., description="URL to check"),
    language: str = Query("en", description="Language of the content (default: en)")
):
    try:
        summary, explanation, score = await main(url=url, language=language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "summary": summary,
        "explanation": explanation,
        "score": score,
        "language": language
    }


