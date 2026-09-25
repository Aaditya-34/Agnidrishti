from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.models.job import Job
from backend.app.services.job_service import create_job, get_job


router = APIRouter(prefix="/api/jobs", tags=["jobs"])


ALLOWED_VIDEO_TYPES = {
    "video/mp4",
}


@router.post("", response_model=Job)
async def upload_video(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only MP4 video files are supported.",
        )

    job = create_job(file.filename or "uploaded_video.mp4")

    output_path = Path(job.input_path)

    with output_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    return job


@router.get("/{job_id}", response_model=Job)
def get_job_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job
