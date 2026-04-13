# Telemetry Replay Studio Plan

## Product Positioning

Build a polished replay and debrief tool that feels relevant to validation teams, autonomy software teams, edge-device platforms, and observability-heavy internal engineering groups.

## Core User Story

An engineer or technical lead needs to review a run and answer four questions quickly:

1. What changed over the course of the session?
2. Where did behavior drift away from baseline?
3. Which anomalies deserve follow-up right now?
4. How can the result be handed off without forcing the next engineer to dig through raw logs?

## Why This Is The Right Next Project

`edge-lab-console` already shows lab operations and live run management. This project complements it by focusing on analysis and debrief:

- replay instead of queue management
- comparison instead of run intake
- scoring and debrief instead of operator notes alone
- a more visual, data-heavy interaction model

Together, the two projects tell a stronger story than either one alone.

## MVP Scope

- session catalog with filters
- replay timeline with event clusters
- comparison view for selected runs
- anomaly summary and artifact list
- debrief export API

## Stretch Scope

- playback speed controls
- scrubber-linked charts
- baseline profile selection
- operator note templates
- generated executive summary draft

## Definition Of Done

- clean GitHub repo with screenshots
- backend endpoints with tests
- responsive frontend with polished visual identity
- seeded demo data that feels believable
- one-paragraph case study ready for the portfolio site
