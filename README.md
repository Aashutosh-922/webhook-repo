# webhook-repo

Flask-based GitHub webhook receiver that stores GitHub events in MongoDB and displays them via a polling UI.

## Features
- Receives GitHub webhooks for:
  - PUSH
  - PULL_REQUEST
  - MERGE
- Stores events in MongoDB
- UI polls MongoDB every 15 seconds
- Displays formatted activity feed

## Tech Stack
- Python (Flask)
- MongoDB
- Ngrok (for local webhook exposure)
- Vanilla JS (UI polling)

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
