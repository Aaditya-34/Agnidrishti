import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [job, setJob] = useState(null)
  const [statistics, setStatistics] = useState(null)
  const [error, setError] = useState('')
  const [uploading, setUploading] = useState(false)
  const [executing, setExecuting] = useState(false)

  const fileInputRef = useRef(null)

  const isProcessing =
    job?.status === 'queued' || job?.status === 'processing'

  async function loadStatistics(jobId) {
    const response = await fetch(
      `${API_BASE}/api/jobs/${jobId}/statistics`,
    )

    if (!response.ok) {
      throw new Error('Unable to load processing statistics.')
    }

    const data = await response.json()
    setStatistics(data)
  }

  useEffect(() => {
    if (!job?.job_id || !isProcessing) {
      return
    }

    const interval = setInterval(async () => {
      try {
        const response = await fetch(
          `${API_BASE}/api/jobs/${job.job_id}`,
        )

        if (!response.ok) {
          throw new Error('Unable to read job status.')
        }

        const updatedJob = await response.json()
        setJob(updatedJob)

        if (updatedJob.status === 'completed') {
          clearInterval(interval)
          await loadStatistics(updatedJob.job_id)
        }

        if (updatedJob.status === 'failed') {
          clearInterval(interval)
          setError(updatedJob.error || 'Video processing failed.')
        }
      } catch (err) {
        setError(err.message)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [job?.job_id, isProcessing])

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    setError('')
    setStatistics(null)
    setJob(null)
    setUploadProgress(0)

    if (!file) {
      setSelectedFile(null)
      return
    }

    if (file.type !== 'video/mp4') {
      setSelectedFile(null)
      setError('Please select an MP4 video.')
      return
    }

    setSelectedFile(file)
  }

  function uploadFile() {
    if (!selectedFile) {
      return
    }

    setUploading(true)
    setError('')
    setUploadProgress(0)

    const formData = new FormData()
    formData.append('file', selectedFile)

    const xhr = new XMLHttpRequest()

    xhr.open('POST', `${API_BASE}/api/jobs`)

    xhr.upload.addEventListener('progress', (event) => {
      if (event.lengthComputable) {
        setUploadProgress(
          Math.round((event.loaded / event.total) * 100),
        )
      }
    })

    xhr.addEventListener('load', () => {
      setUploading(false)

      if (xhr.status >= 200 && xhr.status < 300) {
        const uploadedJob = JSON.parse(xhr.responseText)
        setJob(uploadedJob)
        setUploadProgress(100)
      } else {
        try {
          const response = JSON.parse(xhr.responseText)
          setError(response.detail || 'Video upload failed.')
        } catch {
          setError('Video upload failed.')
        }
      }
    })

    xhr.addEventListener('error', () => {
      setUploading(false)
      setError(
        'Unable to connect to the Agnidrishti backend.',
      )
    })

    xhr.send(formData)
  }

  async function executeJob() {
    if (!job?.job_id) {
      return
    }

    setExecuting(true)
    setError('')
    setStatistics(null)

    try {
      const response = await fetch(
        `${API_BASE}/api/jobs/${job.job_id}/execute`,
        {
          method: 'POST',
        },
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail || 'Unable to execute the video.',
        )
      }

      setJob(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setExecuting(false)
    }
  }

  function resetDashboard() {
    setSelectedFile(null)
    setUploadProgress(0)
    setJob(null)
    setStatistics(null)
    setError('')

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const outputVideoUrl = job?.job_id
    ? `${API_BASE}/api/jobs/${job.job_id}/output`
    : null

  return (
    <main className="app">
      <header className="header">
        <div>
          <p className="eyebrow">AI FIRE & SMOKE DETECTION</p>
          <h1>Agnidrishti</h1>
          <p className="subtitle">
            Upload a video, execute detection, and review the
            processed result.
          </p>
        </div>

        <div className="system-status">
          <span className="status-dot" />
          Backend connected
        </div>
      </header>

      <section className="dashboard-card">
        <div className="section-heading">
          <div>
            <span className="step-number">01</span>
            <h2>Upload video</h2>
          </div>

          <span className="format-label">MP4 only</span>
        </div>

        <div className="upload-area">
          <input
            ref={fileInputRef}
            type="file"
            accept="video/mp4"
            onChange={handleFileChange}
          />

          <button
            type="button"
            className="secondary-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
          >
            Choose MP4
          </button>

          {selectedFile && (
            <div className="file-info">
              <strong>{selectedFile.name}</strong>
              <span>
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
              </span>
            </div>
          )}

          {selectedFile && !job && (
            <button
              type="button"
              className="primary-button"
              onClick={uploadFile}
              disabled={uploading}
            >
              {uploading ? 'Uploading…' : 'Upload video'}
            </button>
          )}
        </div>

        {uploading && (
          <div className="progress-block">
            <div className="progress-label">
              <span>Upload progress</span>
              <strong>{uploadProgress}%</strong>
            </div>

            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        )}
      </section>

      {job && (
        <section className="dashboard-card">
          <div className="section-heading">
            <div>
              <span className="step-number">02</span>
              <h2>Execute detection</h2>
            </div>

            <span className={`job-status ${job.status}`}>
              {job.status}
            </span>
          </div>

          <div className="job-summary">
            <span>Job ID</span>
            <code>{job.job_id}</code>
          </div>

          {job.status === 'uploaded' && (
            <button
              type="button"
              className="primary-button"
              onClick={executeJob}
              disabled={executing}
            >
              {executing ? 'Starting…' : 'Execute detection'}
            </button>
          )}

          {isProcessing && (
            <div className="processing-state">
              <div className="spinner" />

              <div>
                <strong>Processing video</strong>
                <p>
                  YOLO is analyzing the uploaded frames. This may
                  take several minutes for long videos.
                </p>
              </div>
            </div>
          )}

          {job.status === 'completed' && (
            <div className="success-state">
              <strong>Detection completed successfully.</strong>
              <span>
                Processed output is ready for review.
              </span>
            </div>
          )}

          {job.status === 'failed' && (
            <div className="error-state">
              {job.error || 'Video processing failed.'}
            </div>
          )}
        </section>
      )}

      {statistics && job?.status === 'completed' && (
        <section className="dashboard-card">
          <div className="section-heading">
            <div>
              <span className="step-number">03</span>
              <h2>Detection results</h2>
            </div>
          </div>

          <div className="metrics-grid">
            <div className="metric">
              <span>Fire detections</span>

              <strong>
                {statistics.per_class.fire.detections.toLocaleString()}
              </strong>

              <small>
                Avg. confidence{' '}
                {(
                  statistics.per_class.fire.average_confidence * 100
                ).toFixed(2)}
                %
              </small>
            </div>

            <div className="metric">
              <span>Smoke detections</span>

              <strong>
                {statistics.per_class.smoke.detections.toLocaleString()}
              </strong>

              <small>
                Avg. confidence{' '}
                {(
                  statistics.per_class.smoke.average_confidence * 100
                ).toFixed(2)}
                %
              </small>
            </div>

            <div className="metric">
              <span>Frames processed</span>

              <strong>
                {statistics.processed_frames.toLocaleString()}
              </strong>

              <small>
                of {statistics.total_frames.toLocaleString()}
              </small>
            </div>
          </div>

          <div className="video-section">
            <h3>Processed video</h3>

            <video
              className="output-video"
              controls
              preload="metadata"
              src={outputVideoUrl}
            />
          </div>

          <button
            type="button"
            className="secondary-button"
            onClick={resetDashboard}
          >
            Process another video
          </button>
        </section>
      )}

      {error && (
        <div className="global-error">
          <strong>Error:</strong> {error}
        </div>
      )}
    </main>
  )
}

export default App