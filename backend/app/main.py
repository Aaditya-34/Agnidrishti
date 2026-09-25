from fastapi import FastAPI

from backend.app.routes.jobs import router as jobs_router


app = FastAPI(
    title="Agnidrishti API",
    description="Backend API for the Agnidrishti fire and smoke detection system",
    version="0.1.0",
)


app.include_router(jobs_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "agnidrishti-api",
    }
