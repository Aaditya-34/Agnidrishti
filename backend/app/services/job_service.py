import json
import uuid
from pathlib import Path

from backend.app.models.job import Job, JobStatus


UPLOAD_DIR = Path("backend/storage/uploads")
OUTPUT_DIR = Path("backend/storage/outputs")
JOBS_FILE = Path("backend/storage/jobs.json")


UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _load_jobs() -> dict[str, Job]:
    if not JOBS_FILE.exists():
        return {}

    try:
        with JOBS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            job_id: Job.model_validate(job_data)
            for job_id, job_data in data.items()
        }

    except (json.JSONDecodeError, OSError, ValueError):
        return {}


def _save_jobs(jobs: dict[str, Job]) -> None:
    data = {
        job_id: job.model_dump(mode="json")
        for job_id, job in jobs.items()
    }

    with JOBS_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


jobs: dict[str, Job] = _load_jobs()


def create_job(filename: str) -> Job:
    job_id = uuid.uuid4().hex

    input_path = UPLOAD_DIR / f"{job_id}_{filename}"

    job = Job(
        job_id=job_id,
        filename=filename,
        status=JobStatus.UPLOADED,
        input_path=str(input_path),
        total_frames=0,
        processed_frames=0,
        progress=0,
    )

    jobs[job_id] = job
    _save_jobs(jobs)

    return job


def get_job(job_id: str) -> Job | None:
    return jobs.get(job_id)


def update_job(job_id: str, **changes) -> Job | None:
    job = jobs.get(job_id)

    if job is None:
        return None

    updated_job = job.model_copy(update=changes)

    jobs[job_id] = updated_job
    _save_jobs(jobs)

    return updated_job