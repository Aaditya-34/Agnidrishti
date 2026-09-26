import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [page, setPage] = useState('landing')
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [job, setJob] = useState(null)
  const [statistics, setStatistics] = useState(null)
  const [error, setError] = useState('')
  const [uploading, setUploading] = useState(false)
  const [executing, setExecuting] = useState(false)

  const fileInputRef = useRef(null)

  const isProcessing =
    job?.status === 'queued' ||
    job?.status === 'processing'

  async function loadStatistics(jobId) {
    try {
      const response = await fetch(
        `${API_BASE}/api/jobs/${jobId}/statistics`,
      )

      if (!response.ok) {
        throw new Error(
          'Unable to load processing statistics.',
        )
      }

      const data = await response.json()

      setStatistics(data)

      return data
    } catch (err) {
      setError(err.message)

      return null
    }
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
          throw new Error(
            'Unable to read job status.',
          )
        }

        const updatedJob = await response.json()

        setJob(updatedJob)

        if (updatedJob.status === 'completed') {
          clearInterval(interval)

          await loadStatistics(
            updatedJob.job_id,
          )

          setTimeout(() => {
            setPage('results')
          }, 700)
        }

        if (updatedJob.status === 'failed') {
          clearInterval(interval)

          setError(
            updatedJob.error ||
              'Video processing failed.',
          )
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

    formData.append(
      'file',
      selectedFile,
    )

    const xhr = new XMLHttpRequest()

    xhr.open(
      'POST',
      `${API_BASE}/api/jobs`,
    )

    xhr.upload.addEventListener(
      'progress',
      (event) => {
        if (event.lengthComputable) {
          setUploadProgress(
            Math.round(
              (event.loaded /
                event.total) *
                100,
            ),
          )
        }
      },
    )

    xhr.addEventListener(
      'load',
      () => {
        setUploading(false)

        if (
          xhr.status >= 200 &&
          xhr.status < 300
        ) {
          const uploadedJob =
            JSON.parse(
              xhr.responseText,
            )

          setJob(uploadedJob)
          setUploadProgress(100)

          setTimeout(() => {
            setPage('detect')
          }, 500)
        } else {
          try {
            const response =
              JSON.parse(
                xhr.responseText,
              )

            setError(
              response.detail ||
                'Video upload failed.',
            )
          } catch {
            setError(
              'Video upload failed.',
            )
          }
        }
      },
    )

    xhr.addEventListener(
      'error',
      () => {
        setUploading(false)

        setError(
          'Unable to connect to the Agnidrishti backend.',
        )
      },
    )

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

      const data =
        await response.json()

      if (!response.ok) {
        throw new Error(
          data.detail ||
            'Unable to execute the video.',
        )
      }

      setJob(data)

      if (data.status === 'completed') {
        await loadStatistics(
          data.job_id,
        )

        setTimeout(() => {
          setPage('results')
        }, 700)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setExecuting(false)
    }
  }

  function continueToUpload() {
    setPage('upload')
  }

  function resetDashboard() {
    setSelectedFile(null)
    setUploadProgress(0)
    setJob(null)
    setStatistics(null)
    setError('')
    setUploading(false)
    setExecuting(false)
    setPage('upload')

    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const outputVideoUrl =
    job?.job_id
      ? `${API_BASE}/api/jobs/${job.job_id}/output`
      : null

  const detectionProgress = Math.max(
    0,
    Math.min(
      100,
      Number(job?.progress ?? 0),
    ),
  )

  const processedFrames =
    Number(
      job?.processed_frames ?? 0,
    )

  const totalFrames =
    Number(
      job?.total_frames ?? 0,
    )

  return (
    <main className="agnidrishti-app">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />
      <div className="ambient ambient-three" />

      {page === 'landing' && (
        <section className="landing-page page-enter">
          <div className="landing-grid" />

          <div className="landing-vignette" />

          <div className="ember-field">
            {Array.from(
              { length: 20 },
              (_, index) => (
                <i key={index} />
              ),
            )}
          </div>

          <div className="system-orbit orbit-main">
            <div className="orbit-light" />
          </div>

          <div className="system-orbit orbit-secondary">
            <div className="orbit-light" />
          </div>

          <div className="system-orbit orbit-tertiary">
            <div className="orbit-light" />
          </div>

          <div className="scan-beam" />

          <div className="landing-center">
            <div className="brand-mark">
              <div className="brand-halo halo-one" />
              <div className="brand-halo halo-two" />
              <div className="brand-halo halo-three" />

              <div className="brand-core">
                <div className="brand-symbol">
                  <span />
                  <span />
                  <span />
                </div>
              </div>

              <div className="brand-spark spark-one" />
              <div className="brand-spark spark-two" />
              <div className="brand-spark spark-three" />
              <div className="brand-spark spark-four" />
            </div>

            <h1 className="landing-title">
              AGNIDRISHTI
            </h1>

            <button
              type="button"
              className="continue-button"
              onClick={
                continueToUpload
              }
            >
              <span>
                CONTINUE
              </span>

              <span className="continue-arrow">
                <span>→</span>
              </span>
            </button>
          </div>

          <div className="landing-corner corner-top-left" />
          <div className="landing-corner corner-top-right" />
          <div className="landing-corner corner-bottom-left" />
          <div className="landing-corner corner-bottom-right" />

          <div className="landing-scan-line" />
        </section>
      )}

      {page === 'upload' && (
        <section className="workflow-page page-enter upload-page">
          <WorkflowHeader
            current={1}
            onBack={() =>
              setPage('landing')
            }
          />

          <div className="workflow-content">
            <div className="page-intro">
              <h2>
                GIVE AGNIDRISHTI
                <br />
                <span>
                  SOMETHING TO SEE.
                </span>
              </h2>

              <p>
                Upload an MP4 surveillance
                or scene video. The system
                will prepare it for
                intelligent fire and smoke
                analysis.
              </p>
            </div>

            <div
              className={`upload-orbit ${
                selectedFile
                  ? 'has-file'
                  : ''
              }`}
            >
              <div className="orbit-line orbit-line-one" />
              <div className="orbit-line orbit-line-two" />
              <div className="orbit-line orbit-line-three" />

              <div className="upload-card">
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="video/mp4"
                  onChange={
                    handleFileChange
                  }
                />

                <button
                  type="button"
                  className="upload-trigger"
                  onClick={() =>
                    fileInputRef.current?.click()
                  }
                  disabled={uploading}
                >
                  <span className="upload-icon">
                    ↑
                  </span>

                  <strong>
                    {selectedFile
                      ? 'CHOOSE ANOTHER VIDEO'
                      : 'CHOOSE MP4 VIDEO'}
                  </strong>

                  <small>
                    ONE CLICK. MP4 ONLY.
                  </small>
                </button>

                {selectedFile && (
                  <div className="selected-file">
                    <div className="file-pulse" />

                    <div>
                      <strong>
                        {selectedFile.name}
                      </strong>

                      <span>
                        {(
                          selectedFile.size /
                          (1024 * 1024)
                        ).toFixed(2)}{' '}
                        MB
                      </span>
                    </div>
                  </div>
                )}

                {selectedFile && (
                  <button
                    type="button"
                    className="action-button"
                    onClick={uploadFile}
                    disabled={uploading}
                  >
                    {uploading ? (
                      <>
                        <span className="mini-loader" />
                        UPLOADING{' '}
                        {uploadProgress}%
                      </>
                    ) : (
                      <>
                        UPLOAD VIDEO
                        <span>→</span>
                      </>
                    )}
                  </button>
                )}

                {uploading && (
                  <div className="upload-progress">
                    <div
                      className="upload-progress-fill"
                      style={{
                        width: `${uploadProgress}%`,
                      }}
                    />
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="page-tip">
            <span>01</span>

            <p>
              YOUR ORIGINAL VIDEO
              REMAINS UNTOUCHED.
            </p>
          </div>
        </section>
      )}

      {page === 'detect' && (
        <section className="workflow-page page-enter detect-page">
          <WorkflowHeader
            current={2}
            onBack={() =>
              setPage('upload')
            }
          />

          <div className="detect-content">
            <div className="page-intro centered">
              <h2>
                LET THE VISION
                <br />
                <span>
                  ENGINE LOOK DEEPER.
                </span>
              </h2>

              <p>
                YOLO IS EXAMINING THE
                SCENE FRAME BY FRAME FOR
                FIRE AND SMOKE.
              </p>
            </div>

            {!isProcessing &&
              job?.status ===
                'uploaded' && (
                <div className="launch-zone">
                  <div className="radar-static">
                    <div className="radar-circle circle-a" />
                    <div className="radar-circle circle-b" />
                    <div className="radar-circle circle-c" />

                    <div className="radar-cross horizontal" />
                    <div className="radar-cross vertical" />

                    <div className="radar-core">
                      <span>AI</span>
                    </div>
                  </div>

                  <button
                    type="button"
                    className="launch-button"
                    onClick={
                      executeJob
                    }
                    disabled={
                      executing
                    }
                  >
                    <span>
                      {executing
                        ? 'INITIALIZING'
                        : 'START DETECTION'}
                    </span>

                    <strong>
                      ↗
                    </strong>
                  </button>
                </div>
              )}

            {isProcessing && (
              <div className="scanner-stage">
                <div className="scanner-grid">
                  <div className="scanner-horizontal" />
                  <div className="scanner-vertical" />

                  <div className="scan-corner corner-tl" />
                  <div className="scan-corner corner-tr" />
                  <div className="scan-corner corner-bl" />
                  <div className="scan-corner corner-br" />

                  <div className="scanner-object fire-object">
                    <span>FIRE</span>
                  </div>

                  <div className="scanner-object smoke-object">
                    <span>SMOKE</span>
                  </div>

                  <div className="scanner-progress">
                    <div className="scanner-progress-heading">
                      <span>
                        ANALYSIS PROGRESS
                      </span>

                      <strong>
                        {detectionProgress}%
                      </strong>
                    </div>

                    <div className="scanner-progress-track">
                      <div
                        className="scanner-progress-fill"
                        style={{
                          width: `${detectionProgress}%`,
                        }}
                      />
                    </div>

                    <div className="scanner-progress-meta">
                      <span>
                        FRAME{' '}
                        {processedFrames.toLocaleString()}
                        {' / '}
                        {totalFrames > 0
                          ? totalFrames.toLocaleString()
                          : '—'}
                      </span>

                      <span>
                        {detectionProgress < 100
                          ? 'PROCESSING'
                          : 'COMPLETE'}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="scanner-readout">
                  <span className="live-dot" />
                  ANALYZING FRAMES
                </div>

                <div className="processing-copy">
                  <strong>
                    VISION ENGINE ACTIVE
                  </strong>

                  <span>
                    DETECTING PATTERNS,
                    MOVEMENT AND
                    CONFIDENCE SIGNALS...
                  </span>
                </div>
              </div>
            )}

            {job?.status ===
              'completed' && (
              <div className="complete-transition">
                <div className="completion-ring">
                  <span>✓</span>
                </div>

                <strong>
                  ANALYSIS COMPLETE
                </strong>

                <span>
                  PREPARING YOUR RESULTS...
                </span>
              </div>
            )}

            {job?.status === 'failed' && (
              <div className="failure-panel">
                <strong>
                  DETECTION INTERRUPTED
                </strong>

                <span>
                  {job.error ||
                    'Video processing failed.'}
                </span>
              </div>
            )}

            {job && (
              <div className="job-chip">
                <span>JOB</span>

                <code>
                  {job.job_id}
                </code>
              </div>
            )}
          </div>
        </section>
      )}

      {page === 'results' && (
        <section className="workflow-page page-enter results-page">
          <WorkflowHeader
            current={3}
            onBack={() =>
              setPage('detect')
            }
          />

          <div className="results-content">
            <div className="results-heading">
              <div>
                <h2>
                  INTELLIGENCE
                  <br />
                  <span>
                    REVEALED.
                  </span>
                </h2>
              </div>

              <div className="success-orb">
                <span>✓</span>
              </div>
            </div>

            {statistics && (
              <div className="metrics-row">
                <MetricCard
                  type="fire"
                  label="FIRE"
                  value={
                    statistics
                      .per_class
                      .fire
                      .detections
                  }
                  confidence={
                    statistics
                      .per_class
                      .fire
                      .average_confidence
                  }
                />

                <MetricCard
                  type="smoke"
                  label="SMOKE"
                  value={
                    statistics
                      .per_class
                      .smoke
                      .detections
                  }
                  confidence={
                    statistics
                      .per_class
                      .smoke
                      .average_confidence
                  }
                />

                <MetricCard
                  type="frames"
                  label="FRAMES"
                  value={
                    statistics
                      .processed_frames
                  }
                  secondary={
                    `OF ${statistics.total_frames.toLocaleString()}`
                  }
                />
              </div>
            )}

            <div className="video-panel">
              <div className="video-panel-header">
                <div>
                  <span className="live-dot" />
                  PROCESSED OUTPUT
                </div>

                <span>
                  AI ANNOTATED VIDEO
                </span>
              </div>

              <div className="video-frame">
                <div className="video-glow" />

                <video
                  className="output-video"
                  controls
                  preload="metadata"
                  src={
                    outputVideoUrl
                  }
                >
                  Your browser does not
                  support video playback.
                </video>
              </div>

              <div className="video-footer">
                <span>
                  FIRE
                  <i className="legend-fire" />
                </span>

                <span>
                  SMOKE
                  <i className="legend-smoke" />
                </span>

                <span>
                  YOLO DETECTION
                </span>
              </div>
            </div>

            <div className="result-actions">
              <button
                type="button"
                className="secondary-action"
                onClick={
                  resetDashboard
                }
              >
                ANALYZE ANOTHER VIDEO
              </button>

              <div className="result-status">
                <span className="live-dot" />

                ANALYSIS VERIFIED
              </div>
            </div>
          </div>
        </section>
      )}

      {error && (
        <div className="floating-error">
          <div className="error-icon">
            !
          </div>

          <div>
            <strong>
              SOMETHING NEEDS ATTENTION
            </strong>

            <span>
              {error}
            </span>
          </div>

          <button
            type="button"
            onClick={() =>
              setError('')
            }
          >
            ×
          </button>
        </div>
      )}
    </main>
  )
}

function WorkflowHeader({
  current,
  onBack,
}) {
  return (
    <header className="workflow-header">
      <button
        type="button"
        className="mini-brand"
        onClick={onBack}
      >
        <span className="mini-brand-icon">
          ✦
        </span>

        <span>
          AGNIDRISHTI
        </span>
      </button>

      <div className="workflow-progress">
        <WorkflowStep
          number="01"
          label="CAPTURE"
          active={
            current === 1
          }
          complete={
            current > 1
          }
        />

        <div
          className={`progress-connector ${
            current > 1
              ? 'complete'
              : ''
          }`}
        />

        <WorkflowStep
          number="02"
          label="DETECT"
          active={
            current === 2
          }
          complete={
            current > 2
          }
        />

        <div
          className={`progress-connector ${
            current > 2
              ? 'complete'
              : ''
          }`}
        />

        <WorkflowStep
          number="03"
          label="REVEAL"
          active={
            current === 3
          }
          complete={false}
        />
      </div>

      <div className="header-status">
        <span className="live-dot" />
        SYSTEM ONLINE
      </div>
    </header>
  )
}

function WorkflowStep({
  number,
  label,
  active,
  complete,
}) {
  return (
    <div
      className={`workflow-step ${
        active
          ? 'active'
          : ''
      } ${
        complete
          ? 'complete'
          : ''
      }`}
    >
      <span>
        {complete
          ? '✓'
          : number}
      </span>

      <small>
        {label}
      </small>
    </div>
  )
}

function MetricCard({
  type,
  label,
  value,
  confidence,
  secondary,
}) {
  return (
    <div
      className={`metric-card metric-${type}`}
    >
      <div className="metric-top">
        <span>
          {label}
        </span>

        <div className="metric-icon">
          {type === 'fire' &&
            '🔥'}

          {type === 'smoke' &&
            '◌'}

          {type === 'frames' &&
            '◈'}
        </div>
      </div>

      <strong>
        {typeof value ===
        'number'
          ? value.toLocaleString()
          : value}
      </strong>

      {confidence !==
        undefined && (
        <small>
          AVG. CONFIDENCE{' '}
          {(
            confidence * 100
          ).toFixed(2)}
          %
        </small>
      )}

      {secondary && (
        <small>
          {secondary}
        </small>
      )}

      <div className="metric-line" />
    </div>
  )
}

export default App