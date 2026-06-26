# SkillSetu AI - Professional Identity Builder

A full-stack AI-powered application that helps informal workers create professional employment identities.

## Features

- **Worker Profile Builder** - Enter basic info and work experience, AI extracts skills and creates a professional summary
- **Resume Generator** - Generate ATS-friendly PDF resumes
- **Job Matching** - Match extracted skills against job listings with match percentages
- **Dashboard** - Modern, clean UI with card-based responsive design

## Tech Stack

- **Frontend**: React + Vite + Tailwind CSS + Shadcn
- **Backend**: FastAPI + SQLAlchemy
- **Database**: SQLite
- **AI**: Ollama (local LLM) with qwen2.5:3b or Google Gemini as fallback
- **PDF**: ReportLab

## Quick Start

### Prerequisites

- Ollama (if running locally)

### Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd skillsetu
```

2. Start the backend:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

3. Start the frontend (in a new terminal):
```bash
cd frontend
npm install
npm run dev
```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

- `OLLAMA_URL` - Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model to use (default: qwen2.5:3b)
- `GEMINI_API_KEY` - Optional Google Gemini API key for fallback AI

## Project Structure

```
skillsetu/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── services.py
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── profiles.py
│   │       ├── jobs.py
│   │       └── resume.py
│   ├── main.py
│   ├── requirements.txt
│   ├── jobs.json
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProfileBuilder.jsx
│   │   │   ├── ResumeGenerator.jsx
│   │   │   └── JobMatcher.jsx
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
```

## Architecture

```
┌─────────────┐                            ┌──────────────────────────────┐
│  Browser    │                            │  FastAPI Backend             │
│             │       ┌──────────────────►│  (Port 8000)                  │
│  :5173      ├───────┤                   │  - Profile management         │
│  Frontend   │       │                   │  - Ollama AI integration      │
│  (Vite)     │       │                   │  - ReportLab PDF generation   │
└─────────────┘       │                   │  - Job matching logic         │
                       │                   └──────────┬───────────────────┘
                       │                              │
                       │                   ┌──────────▼───────────────────┐
                       │                   │  SQLite                       │
                       │                   │  - Worker profiles             │
                       │                   └──────────────────────────────┘
                       │                              │
                       │                   ┌──────────▼───────────────────┐
                       │                   │  Ollama (Local LLM)           │
                       │                   │  (Port 11434)                  │
                       │                   │  - qwen2.5:3b                  │
                       │                   │  - Profile extraction          │
                       │                   └──────────────────────────────┘
                       │
          API calls    │
           /api/* ─────┘
```

## Contributing

This project is designed for informal workers. Contributions are welcome!

## License

MIT