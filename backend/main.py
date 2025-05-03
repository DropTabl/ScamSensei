from fastapi import FastAPI
from backend.routers import scam_detection,url_detection,voice_detection
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from backend.utils.helper import init_llm



init_llm()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include routers
app.include_router(scam_detection.router, prefix="/scam", tags=["scam"])
app.include_router(voice_detection.router, prefix="/voice", tags=["url"])
app.include_router(url_detection.router, prefix="/url", tags=["url"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
