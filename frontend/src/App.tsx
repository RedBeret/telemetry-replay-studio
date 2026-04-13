import { startTransition, useCallback, useDeferredValue, useEffect, useState } from "react";

type Overview = {
    sessions: number;
    flagged: number;
    avgScore: number;
    artifactsReady: number;
};

type SessionSummary = {
    id: string;
    title: string;
    status: string;
    score: number;
    durationSeconds: number;
    environment: string;
    vehicle: string;
    missionProfile: string;
    summary: string;
    anomalies: number;
};

type CompareCandidate = {
    id: string;
    title: string;
    score: number;
};

type DetailMetric = {
    label: string;
    value: string;
    delta: string;
    trend: string;
};

type SignalFrame = {
    time: string;
    accuracy: number;
    latency: number;
    linkQuality: number;
    confidence: number;
    note: string;
};

type TimelineEvent = {
    time: string;
    type: string;
    title: string;
    detail: string;
};

type Anomaly = {
    severity: string;
    window: string;
    title: string;
    owner: string;
};

type Artifact = {
    name: string;
    kind: string;
};

type Note = {
    author: string;
    time: string;
    text: string;
};

type SessionDetail = {
    id: string;
    title: string;
    status: string;
    score: number;
    summary: string;
    verdict: string;
    durationSeconds: number;
    environment: string;
    vehicle: string;
    missionProfile: string;
    compareCandidates: CompareCandidate[];
    defaultBaselineId: string;
    metrics: DetailMetric[];
    signalFrames: SignalFrame[];
    timeline: TimelineEvent[];
    anomalies: Anomaly[];
    artifacts: Artifact[];
    notes: Note[];
};

type ComparisonFocusArea = {
    label: string;
    current: string;
    baseline: string;
    delta: string;
};

type Comparison = {
    sessionId: string;
    baselineId: string;
    baselineTitle: string;
    summary: string;
    scoreDelta: number;
    largestWindow: string;
    recommendation: string;
    focusAreas: ComparisonFocusArea[];
};

type Debrief = {
    sessionId: string;
    sessionTitle: string;
    baselineId: string;
    baselineTitle: string;
    score: number;
    scoreDelta: number;
    verdict: string;
    executiveSummary: string;
    callouts: string[];
    recommendedActions: string[];
    artifactChecklist: string[];
};

type Catalog = {
    overview: Overview;
    sessions: SessionSummary[];
    defaultSessionId: string;
};

const formatDuration = (durationSeconds: number) => {
    const minutes = Math.floor(durationSeconds / 60);
    const seconds = durationSeconds % 60;
    return `${minutes}m ${seconds.toString().padStart(2, "0")}s`;
};

const statusOptions = ["all", "flagged", "review", "passed"];

const App = () => {
    const [catalog, setCatalog] = useState<Catalog | null>(null);
    const [detail, setDetail] = useState<SessionDetail | null>(null);
    const [comparison, setComparison] = useState<Comparison | null>(null);
    const [debrief, setDebrief] = useState<Debrief | null>(null);
    const [selectedSessionId, setSelectedSessionId] = useState("");
    const [selectedBaselineId, setSelectedBaselineId] = useState("");
    const [activeFrameIndex, setActiveFrameIndex] = useState(0);
    const [statusFilter, setStatusFilter] = useState("all");
    const [search, setSearch] = useState("");
    const [error, setError] = useState("");
    const [loadingDetail, setLoadingDetail] = useState(false);
    const [loadingDebrief, setLoadingDebrief] = useState(false);
    const deferredSearch = useDeferredValue(search);

    const stepFrame = useCallback(
        (direction: 1 | -1) => {
            if (!detail) {
                return;
            }

            setActiveFrameIndex((current) =>
                Math.max(0, Math.min(detail.signalFrames.length - 1, current + direction))
            );
        },
        [detail]
    );

    useEffect(() => {
        const handleKey = (event: KeyboardEvent) => {
            if (
                event.target instanceof HTMLInputElement ||
                event.target instanceof HTMLSelectElement ||
                event.target instanceof HTMLTextAreaElement
            ) {
                return;
            }

            if (event.key === "ArrowRight") {
                stepFrame(1);
            } else if (event.key === "ArrowLeft") {
                stepFrame(-1);
            }
        };

        window.addEventListener("keydown", handleKey);
        return () => window.removeEventListener("keydown", handleKey);
    }, [stepFrame]);

    useEffect(() => {
        fetch("/api/replay")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load replay catalog");
                }

                return response.json();
            })
            .then((payload: Catalog) => {
                setCatalog(payload);
                setSelectedSessionId(payload.defaultSessionId);
            })
            .catch(() =>
                setError(
                    "Replay workspace could not be loaded. Start the backend and try again."
                )
            );
    }, []);

    useEffect(() => {
        if (!selectedSessionId) {
            return;
        }

        setLoadingDetail(true);
        fetch(`/api/replay/${selectedSessionId}`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load session detail");
                }

                return response.json();
            })
            .then((payload: SessionDetail) => {
                startTransition(() => {
                    setDetail(payload);
                    setSelectedBaselineId(payload.defaultBaselineId);
                    setActiveFrameIndex(0);
                });
            })
            .catch(() =>
                setError("Session detail could not be loaded. Refresh and try again.")
            )
            .finally(() => setLoadingDetail(false));
    }, [selectedSessionId]);

    useEffect(() => {
        if (!detail || !selectedBaselineId) {
            return;
        }

        setLoadingDebrief(true);
        Promise.all([
            fetch(`/api/replay/${detail.id}/compare/${selectedBaselineId}`).then(
                (response) => {
                    if (!response.ok) {
                        throw new Error("Failed to load comparison");
                    }

                    return response.json();
                }
            ),
            fetch(
                `/api/replay/${detail.id}/debrief?baseline_id=${encodeURIComponent(selectedBaselineId)}`
            ).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load debrief");
                }

                return response.json();
            }),
        ])
            .then(([comparisonPayload, debriefPayload]) => {
                setComparison(comparisonPayload as Comparison);
                setDebrief(debriefPayload as Debrief);
            })
            .catch(() =>
                setError("Comparison or debrief data could not be loaded for this session.")
            )
            .finally(() => setLoadingDebrief(false));
    }, [detail, selectedBaselineId]);

    if (error) {
        return <main className="app-shell status-screen">{error}</main>;
    }

    if (!catalog || !detail) {
        return (
            <main className="app-shell status-screen">
                Loading replay workspace...
            </main>
        );
    }

    const filteredSessions = catalog.sessions.filter((session) => {
        const matchesStatus =
            statusFilter === "all" ? true : session.status === statusFilter;
        const haystack = `${session.title} ${session.id} ${session.environment} ${session.vehicle} ${session.missionProfile}`.toLowerCase();
        const matchesSearch = haystack.includes(deferredSearch.trim().toLowerCase());

        return matchesStatus && matchesSearch;
    });

    const activeFrame =
        detail.signalFrames[Math.min(activeFrameIndex, detail.signalFrames.length - 1)];
    const highlightedTimelineIndex = Math.min(
        activeFrameIndex,
        detail.timeline.length - 1
    );
    const emptySessions = filteredSessions.length === 0;

    const downloadDebrief = () => {
        if (!debrief) {
            return;
        }

        const blob = new Blob([JSON.stringify(debrief, null, 2)], {
            type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${debrief.sessionId.toLowerCase()}-debrief.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

    return (
        <main className="app-shell">
            <section className="hero">
                <div className="hero-copy-block">
                    <p className="eyebrow">Telemetry Replay Studio</p>
                    <h1>Replay runs, compare behavior, and leave a cleaner handoff.</h1>
                    <p className="hero-copy">
                        A full-stack replay and debrief workspace for teams that need
                        to understand what changed, where a run drifted, and what the
                        next engineer should know before promotion.
                    </p>
                    <div className="hero-tags">
                        <span>Replay timeline</span>
                        <span>Baseline compare</span>
                        <span>Debrief export</span>
                        <span>{detail.anomalies.length} review windows</span>
                    </div>
                </div>
                <div className="hero-panel">
                    <span>Selected session</span>
                    <strong>{detail.id}</strong>
                    <p>{detail.verdict}</p>
                    <div className="hero-panel__meta">
                        <span>{detail.environment}</span>
                        <span>{detail.vehicle}</span>
                        <span>{formatDuration(detail.durationSeconds)}</span>
                    </div>
                </div>
            </section>

            <section className="metric-grid">
                <article className="metric-card">
                    <span>Total sessions</span>
                    <strong>{catalog.overview.sessions}</strong>
                </article>
                <article className="metric-card">
                    <span>Flagged</span>
                    <strong>{catalog.overview.flagged}</strong>
                </article>
                <article className="metric-card">
                    <span>Average score</span>
                    <strong>{catalog.overview.avgScore}</strong>
                </article>
                <article className="metric-card">
                    <span>Artifacts ready</span>
                    <strong>{catalog.overview.artifactsReady}</strong>
                </article>
            </section>

            <section className="content-grid">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Session catalog</p>
                        <h2>Recent replays</h2>
                    </div>
                    <div className="catalog-controls">
                        <label className="control">
                            <span>Search</span>
                            <input
                                type="search"
                                placeholder="TRS-3102, sim-west, route-regression..."
                                value={search}
                                onChange={(event) => setSearch(event.target.value)}
                            />
                        </label>
                        <label className="control">
                            <span>Status</span>
                            <select
                                value={statusFilter}
                                onChange={(event) => setStatusFilter(event.target.value)}
                            >
                                {statusOptions.map((option) => (
                                    <option key={option} value={option}>
                                        {option === "all"
                                            ? "All statuses"
                                            : option.charAt(0).toUpperCase() +
                                              option.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </label>
                    </div>
                    {emptySessions ? (
                        <div className="empty-state">
                            No sessions match the current search and status filter.
                        </div>
                    ) : (
                        <div className="session-list">
                            {filteredSessions.map((session) => (
                                <button
                                    key={session.id}
                                    className={`session-card session-card--button${
                                        session.id === detail.id ? " is-active" : ""
                                    }`}
                                    onClick={() => setSelectedSessionId(session.id)}
                                    type="button"
                                >
                                    <div className="session-card__top">
                                        <div>
                                            <strong>{session.title}</strong>
                                            <span>{session.id}</span>
                                        </div>
                                        <span className={`badge badge--${session.status}`}>
                                            {session.status}
                                        </span>
                                    </div>
                                    <p>{session.summary}</p>
                                    <div className="session-meta">
                                        <span>{session.environment}</span>
                                        <span>{session.vehicle}</span>
                                        <span>{session.anomalies} anomalies</span>
                                        <span>score {session.score}</span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}
                </article>

                <article className="panel panel--wide">
                    <div className="panel-heading panel-heading--split">
                        <div>
                            <p className="eyebrow">Replay view</p>
                            <h2>{detail.title}</h2>
                        </div>
                        <div className="session-header-meta">
                            <span>{detail.missionProfile}</span>
                            <span>{detail.status}</span>
                        </div>
                    </div>
                    <div className="frame-scrubber">
                        <div className="frame-scrubber__top">
                            <strong>{activeFrame.time}</strong>
                            <span>{activeFrame.note}</span>
                            <span className="frame-counter">
                                Frame {activeFrameIndex + 1} of {detail.signalFrames.length}
                                <em className="keyboard-hint"> · ← → to step</em>
                            </span>
                        </div>
                        <input
                            type="range"
                            min="0"
                            max={String(Math.max(detail.signalFrames.length - 1, 0))}
                            value={activeFrameIndex}
                            onChange={(event) =>
                                setActiveFrameIndex(Number(event.target.value))
                            }
                        />
                        <div className="signal-grid">
                            <div className="signal-card">
                                <span>Accuracy</span>
                                <strong>{activeFrame.accuracy}%</strong>
                                <div className="signal-bar">
                                    <div style={{ width: `${activeFrame.accuracy}%` }} />
                                </div>
                            </div>
                            <div className="signal-card">
                                <span>Latency</span>
                                <strong>{activeFrame.latency} ms</strong>
                                <div className="signal-bar">
                                    <div style={{ width: `${Math.min(activeFrame.latency / 1.5, 100)}%` }} />
                                </div>
                            </div>
                            <div className="signal-card">
                                <span>Link quality</span>
                                <strong>{activeFrame.linkQuality}%</strong>
                                <div className="signal-bar">
                                    <div style={{ width: `${activeFrame.linkQuality}%` }} />
                                </div>
                            </div>
                            <div className="signal-card">
                                <span>Confidence</span>
                                <strong>{activeFrame.confidence}%</strong>
                                <div className="signal-bar">
                                    <div style={{ width: `${activeFrame.confidence}%` }} />
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="timeline">
                        {detail.timeline.map((event, index) => (
                            <div
                                className={`timeline-event${
                                    index === highlightedTimelineIndex ? " is-active" : ""
                                }`}
                                key={`${event.time}-${event.title}`}
                            >
                                <div className={`timeline-event__dot timeline-event__dot--${event.type}`} />
                                <div className="timeline-event__content">
                                    <span>{event.time}</span>
                                    <strong>{event.title}</strong>
                                    <p>{event.detail}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </article>
            </section>

            <section className="content-grid">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Compare</p>
                        <h2>Baseline review</h2>
                    </div>
                    <label className="control">
                        <span>Comparison target</span>
                        <select
                            value={selectedBaselineId}
                            onChange={(event) => setSelectedBaselineId(event.target.value)}
                        >
                            {detail.compareCandidates.map((candidate) => (
                                <option key={candidate.id} value={candidate.id}>
                                    {candidate.title} ({candidate.id})
                                </option>
                            ))}
                        </select>
                    </label>
                    {comparison ? (
                        <>
                            <div className="comparison-strip">
                                <div className="comparison-card">
                                    <span>Baseline</span>
                                    <strong>{comparison.baselineId}</strong>
                                </div>
                                <div className="comparison-card">
                                    <span>Score delta</span>
                                    <strong>
                                        {comparison.scoreDelta > 0 ? "+" : ""}
                                        {comparison.scoreDelta}
                                    </strong>
                                </div>
                                <div className="comparison-card">
                                    <span>Largest window</span>
                                    <strong>{comparison.largestWindow}</strong>
                                </div>
                            </div>
                            <p className="hint-copy">
                                Recommendation: {comparison.recommendation}
                            </p>
                            <p className="body-copy">{comparison.summary}</p>
                            <div className="focus-grid">
                                {comparison.focusAreas.map((area) => (
                                    <div className="focus-card" key={area.label}>
                                        <span>{area.label}</span>
                                        <strong>{area.current}</strong>
                                        <p>Baseline {area.baseline}</p>
                                        <em>{area.delta}</em>
                                    </div>
                                ))}
                            </div>
                        </>
                    ) : null}
                </article>

                <article className="panel">
                    <div className="panel-heading panel-heading--split">
                        <div>
                            <p className="eyebrow">Debrief</p>
                            <h2>Operator handoff brief</h2>
                        </div>
                        <button
                            className="export-button"
                            onClick={downloadDebrief}
                            type="button"
                        >
                            Export JSON
                        </button>
                    </div>
                    {loadingDebrief ? (
                        <p className="body-copy">Refreshing debrief...</p>
                    ) : null}
                    {debrief ? (
                        <>
                            <p className="body-copy">{debrief.executiveSummary}</p>
                            <div className="debrief-columns">
                                <div>
                                    <h3>Callouts</h3>
                                    <ul className="simple-list simple-list--stacked">
                                        {debrief.callouts.map((callout) => (
                                            <li key={callout}>{callout}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <h3>Recommended actions</h3>
                                    <ul className="simple-list simple-list--stacked">
                                        {debrief.recommendedActions.map((action) => (
                                            <li key={action}>{action}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                            <div className="checklist-block">
                                <h3>Artifact checklist</h3>
                                <ul className="simple-list simple-list--stacked">
                                    {debrief.artifactChecklist.map((item) => (
                                        <li key={item}>{item}</li>
                                    ))}
                                </ul>
                            </div>
                        </>
                    ) : null}
                </article>
            </section>

            <section className="content-grid content-grid--bottom">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Session metrics</p>
                        <h2>What changed from baseline</h2>
                    </div>
                    <div className="metric-list">
                        {detail.metrics.map((metric) => (
                            <div className="metric-row" key={metric.label}>
                                <span>{metric.label}</span>
                                <strong>{metric.value}</strong>
                                <em className={`trend trend--${metric.trend}`}>
                                    {metric.delta}
                                </em>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Anomalies</p>
                        <h2>Windows worth review</h2>
                    </div>
                    <div className="note-list">
                        {detail.anomalies.map((anomaly) => (
                            <div className="anomaly-card" key={`${anomaly.window}-${anomaly.title}`}>
                                <div className="session-card__top">
                                    <strong>{anomaly.title}</strong>
                                    <span className={`badge badge--${anomaly.severity}`}>
                                        {anomaly.severity}
                                    </span>
                                </div>
                                <p>{anomaly.window}</p>
                                <span>{anomaly.owner}</span>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Artifacts and notes</p>
                        <h2>Debrief package</h2>
                    </div>
                    <ul className="simple-list simple-list--stacked">
                        {detail.artifacts.map((artifact) => (
                            <li key={artifact.name}>
                                <strong>{artifact.name}</strong>
                                <span>{artifact.kind}</span>
                            </li>
                        ))}
                    </ul>
                    <div className="note-list note-list--compact">
                        {detail.notes.map((note) => (
                            <div className="note-card" key={`${note.author}-${note.time}`}>
                                <strong>{note.author}</strong>
                                <span>{note.time}</span>
                                <p>{note.text}</p>
                            </div>
                        ))}
                    </div>
                </article>
            </section>

            <section className="footer-strip">
                <span>{filteredSessions.length} sessions visible</span>
                <span>{loadingDetail ? "Refreshing session..." : "Session ready"}</span>
                <span>{comparison ? comparison.recommendation : "Comparison loading..."}</span>
            </section>
        </main>
    );
};

export default App;
