from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from backend.app.models.job import Job, JobStatus
from backend.app.services.job_service import create_job, get_job, update_job
from scripts.inference.worker import process_video


router = APIRouter(prefix="/api/jobs", tags=["jobs"])


ALLOWED_VIDEO_TYPES = {
    "video/mp4",
}

MODEL_PATH = Path(
    "runs/detect/runs/detect/yolov8n_960_mixed/weights/best.pt"
)

OUTPUT_DIR = Path("backend/storage/outputs")


def process_job(job_id: str) -> None:
    job = get_job(job_id)

    if job is None:
        return

    update_job(
        job_id,
        status=JobStatus.PROCESSING,
        total_frames=0,
        processed_frames=0,
        progress=0,
        error=None,
    )

    output_path = OUTPUT_DIR / f"{job_id}_output.mp4"
    statistics_path = OUTPUT_DIR / f"{job_id}_statistics.json"

    def handle_progress(
        processed_frames: int,
        total_frames: int,
    ) -> None:
        if total_frames > 0:
            progress = int(
                (processed_frames / total_frames) * 100
            )
        else:
            progress = 0

        progress = max(0, min(100, progress))

        update_job(
            job_id,
            processed_frames=processed_frames,
            total_frames=total_frames,
            progress=progress,
        )

    result = process_video(
        input_video=job.input_path,
        model_path=str(MODEL_PATH),
        output_video=str(output_path),
        statistics_file=str(statistics_path),
        confidence_threshold=0.35,
        detector_type="yolo",
        progress_callback=handle_progress,
    )

    if result.status == "completed":
        update_job(
            job_id,
            status=JobStatus.COMPLETED,
            output_path=result.output_video,
            statistics_path=result.statistics_file,
            processed_frames=result.processed_frames,
            total_frames=result.total_frames,
            progress=100,
        )
    else:
        update_job(
            job_id,
            status=JobStatus.FAILED,
            error=result.error or "Video processing failed.",
        )


@router.post("", response_model=Job)
async def upload_video(
    file: UploadFile = File(...),
):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only MP4 video files are supported.",
        )

    job = create_job(file.filename or "uploaded_video.mp4")

    input_path = Path(job.input_path)

    with input_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    return get_job(job.job_id)


@router.post("/{job_id}/execute", response_model=Job)
def execute_job(
    job_id: str,
    background_tasks: BackgroundTasks,
):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.status != JobStatus.UPLOADED:
        raise HTTPException(
            status_code=409,
            detail=f"Job cannot be executed from status '{job.status}'.",
        )

    if not Path(job.input_path).exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded video file not found.",
        )

    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Model file not found: {MODEL_PATH}",
        )

    update_job(
        job_id,
        status=JobStatus.QUEUED,
        total_frames=0,
        processed_frames=0,
        progress=0,
        error=None,
    )

    background_tasks.add_task(process_job, job_id)

    return get_job(job_id)


@router.get("/{job_id}/output")
def get_job_output(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=409,
            detail="Video processing is not completed.",
        )

    if not job.output_path:
        raise HTTPException(
            status_code=404,
            detail="Output video is not available.",
        )

    output_path = Path(job.output_path)

    if not output_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Output video file not found.",
        )

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"{job.job_id}_output.mp4",
    )


@router.get("/{job_id}/statistics")
def get_job_statistics(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=409,
            detail="Video processing is not completed.",
        )

    if not job.statistics_path:
        raise HTTPException(
            status_code=404,
            detail="Statistics file is not available.",
        )

    statistics_path = Path(job.statistics_path)

    if not statistics_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Statistics file not found.",
        )

    return FileResponse(
        path=statistics_path,
        media_type="application/json",
        filename=f"{job.job_id}_statistics.json",
    )


@router.get("/{job_id}", response_model=Job)
def get_job_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found.",
        )

    return job