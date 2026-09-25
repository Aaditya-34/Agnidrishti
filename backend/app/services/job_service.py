import uuid
from pathlib import Path

from backend.app.models.job import Job, JobStatus


UPLOAD_DIR = Path("backend/storage/uploads")
OUTPUT_DIR = Path("backend/storage/outputs")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


jobs: dict[str, Job] = {}


def create_job(filename: str) -> Job:
    job_id = uuid.uuid4().hex

    input_path = UPLOAD_DIR / f"{job_id}_{filename}"

    job = Job(
        job_id=job_id,
        filename=filename,
        status=JobStatus.UPLOADED,
        input_path=str(input_path),
    )

    jobs[job_id] = job
    return job


def get_job(job_id: str) -> Job | None:
    return jobs.get(job_id)
