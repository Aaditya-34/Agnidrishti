from enum import Enum
from pydantic import BaseModel


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
