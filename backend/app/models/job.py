from enum import Enum

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    UPLOADED = "uploaded"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(BaseModel):
    job_id: str
    filename: str
    status: JobStatus

    input_path: str

    output_path: str | None = None
    statistics_path: str | None = None
    error: str | None = None

    total_frames: int = Field(default=0, ge=0)
    processed_frames: int = Field(default=0, ge=0)
    progress: int = Field(default=0, ge=0, le=100)