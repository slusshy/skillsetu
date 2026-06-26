# SkillSetu AI - Project Introduction

## 🎯 The Problem

Millions of informal workers across the globe—daily wage laborers, gig workers, artisans, and skilled professionals without formal education—struggle to present their capabilities in a professional manner. They possess valuable skills and years of hands-on experience, but lack the tools to:

- Create structured professional profiles
- Generate ATS-friendly resumes
- Articulate their skills in corporate language
- Match their capabilities with suitable job opportunities

This skills gap prevents talented individuals from accessing better employment opportunities.

---

## 💡 Our Solution

**SkillSetu AI** is an AI-powered full-stack application designed to democratize professional identity creation for informal workers. Our platform transforms unstructured life experiences into structured, professional employment documents using cutting-edge artificial intelligence.

### Core Approach
1. **User Input** → Worker enters basic information and work history in plain language
2. **AI Processing** → Local LLM (qwen2.5:3b via Ollama) extracts skills, competencies, and generates professional summaries
3. **Output Generation** → System produces polished resumes and job-match analytics
4. **Opportunity Matching** → Algorithm compares extracted skills with real job listings and provides match percentages

---

## ⭐ Key Features

### 1. **Intelligent Profile Builder**
- Natural language input for work history
- AI-driven skill extraction and categorization
- Automatic generation of professional summaries
- No prior resume-writing experience required

### 2. **ATS-Friendly Resume Generator**
- One-click PDF generation using ReportLab
- Professionally formatted templates
- Optimized for Applicant Tracking Systems
- Download and share instantly

### 3. **Smart Job Matching Engine**
- Real-time skill-to-job comparison
- Percentage-based match scoring
- Curated job listings database
- Actionable insights for skill gaps

### 4. **Modern, Accessible UI**
- Responsive card-based design
- Clean, intuitive interface
- Built with React + Tailwind CSS + Shadcn
- Mobile-friendly experience

---

## 🛠️ Technical Architecture

### Frontend
- **React 18** - Component-based UI
- **Vite** - Fast build tooling
- **Tailwind CSS** - Utility-first styling
- **Shadcn/ui** - Accessible component library

### Backend
- **FastAPI** - High-performance Python API framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight, embedded database

### AI & Intelligence
- **Ollama** - Local LLM runtime (privacy-first)
- **Qwen 2.5:3B** - Lightweight yet powerful language model
- **Google Gemini** - Optional cloud fallback for enhanced accuracy

### Infrastructure
- **Docker & Docker Compose** - Containerized deployment
- **Nginx** - Reverse proxy and static file serving
- **ReportLab** - PDF generation engine

---

## 🎬 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  1. Worker enters work history and skills in plain text     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  2. AI Model Process (Ollama + Qwen)                        │
│     • Extracts structured skills                            │
│     • Generates professional summary                        │
│     • Categorizes competencies                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Output Generation                                        │
│     • PDF Resume (ReportLab)                                │
│     • Skill Analytics                                       │
│     • Job Match Recommendations                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🌍 Social Impact

- **Accessibility**: No technical skills required to create a professional profile
- **Cost-Effective**: Free, open-source solution for underserved communities
- **Privacy-First**: Local AI processing ensures data security
- **Scalable**: Docker-based deployment allows easy scaling to serve millions

---

## 🚀 Current Status

- ✅ Full-stack application functional
- ✅ AI integration working (Ollama + Gemini fallback)
- ✅ PDF generation implemented
- ✅ Job matching algorithm active
- ✅ Docker deployment ready
- ✅ Responsive UI complete

---

## 📊 Tech Stack Summary

| Layer | Technology |
|-------|-----------|
| **Frontend** | React + Vite + Tailwind CSS |
| **Backend** | FastAPI + Python |
| **Database** | SQLite + SQLAlchemy |
| **AI Engine** | Ollama (qwen2.5:3b) / Google Gemini |
| **PDF Generation** | ReportLab |
| **Deployment** | Docker + Docker Compose + Nginx |

---

## 🙌 Conclusion

SkillSetu AI bridges the gap between informal talent and formal employment opportunities. By leveraging artificial intelligence, we transform raw life experiences into professional credentials—empowering workers to present their true value to the world.

**"Every skill deserves recognition. Every worker deserves a chance."**