# SkillSetu AI - Voice Assistant Training Guide

## Application Overview
SkillSetu AI is a professional identity builder designed for informal workers. It helps users create professional profiles, generate ATS-friendly PDF resumes, and find matching jobs using AI.

**URL:** http://localhost:5173
**Backend API:** http://127.0.0.1:8000

---

## Core Features

### 1. Profile Builder
**Purpose:** Create a professional employment profile from basic information.

**User Inputs:**
- Full Name (required)
- Age (required)
- Location (required)
- Work Experience & Skills Description (required, free text)

**AI Processing:**
- Extracts skills automatically from the description
- Generates a professional summary
- Recommends a job category based on skills
- Creates a structured worker profile

**Success Response:**
- Profile created with ID
- Extracted skills list
- Recommended job category
- Professional summary

**Example User Statement:**
"I have been a construction worker for 5 years. I know how to read blueprints, operate power tools, follow safety protocols, and work well in teams. I'm good at physical labor and can handle heavy materials."

**Example Profile Output:**
- Name: [User's name]
- Age: [User's age]
- Location: [User's city/state]
- Skills: [Extracted: physical labor, blueprint reading, power tools, safety protocols, teamwork]
- Recommended Job Category: Construction Worker
- Summary: "Dedicated construction worker with 5 years of experience in blueprint reading, tool operation, and team collaboration..."

---

### 2. Resume Generator
**Purpose:** Generate ATS-friendly PDF resumes from created profiles.

**User Actions:**
1. Select a profile from dropdown
2. Click "Generate PDF Resume"
3. Download the generated PDF

**Technical Details:**
- Uses ReportLab for PDF generation
- Formats resume with professional layout
- Includes: name, contact, skills, experience summary
- File saved as: `resume_{profile_id}_{hash}.pdf`
- Accessible at: `/static/resume_{profile_id}_{hash}.pdf`

**Supported Languages:**
- English
- Hindi (Devanagari script)

---

### 3. Job Matching
**Purpose:** Match user skills with real job listings from Adzuna API.

**How It Works:**
1. User selects a profile
2. System fetches live jobs from Adzuna API based on profile skills
3. Calculates match percentage for each job
4. Shows missing skills to develop
5. Provides direct application links

**Match Calculation:**
- Exact skill matches: 100% base
- Partial/similar skill matches: proportional percentage
- Soft skill bonuses: +5% for terms like "team", "safety", "communication", "organization"
- Maximum: 100%

**Job Data Fields:**
- Title
- Company name
- Location
- Salary range (min/max)
- Description
- Redirect URL (direct apply link)
- Match percentage
- Missing skills list

**Example Output:**
```
Construction Worker | Tata Electronics | Mumbai | ₹15,000 - ₹25,000 | 70% Match
Missing skills: masonry, painting
```

**API Endpoint:** `POST /api/match-jobs`
**Request Body:** `{ "skills": ["physical labor", "safety protocols", "teamwork"] }`

---

### 4. Voice Assistant (VAPI)
**Purpose:** Provide voice-guided assistance and live voice chat.

**Capabilities:**
- Page help narration (browser speech synthesis)
- Live voice conversation using VAPI
- Real-time transcription
- Multi-language support (English/Hindi)

**Activation:**
- Click the voice assistant button (bottom-right)
- Select "Start Voice Assistant" for live chat
- Use microphone for speech-to-text

**VAPI Configuration:**
- Provider: Deepgram (transcription), Google Gemini (AI), PlayHT (voice)
- Model: gemini-2.0-flash
- First message: "Hello! I am your career assistant. I can help you build profiles, generate resumes, and find jobs."

---

## Navigation Structure

**Tabs:**
1. Profile Builder (👤)
2. Resume Generator (📄)
3. Job Matching (💼)

**Header:**
- Logo: "S" (SkillSetu)
- Title: "SkillSetu AI - Professional Identity Builder"
- Profile count indicator
- Language selector (English/Hindi)

**Footer:**
- "Built with React, FastAPI, Ollama & SQLite"
- "Designed for informal workers. No paid APIs. Fully local."

---

## User Flows and Voice Commands

### Flow 1: Create Profile
**User Steps:**
1. Navigate to Profile Builder tab
2. Fill in: Full Name, Age, Location
3. Enter work experience and skills in description
4. Click "Generate Professional Profile"
5. AI extracts skills and creates profile

**Voice Assistant Should Understand:**
- "Create a profile"
- "Build my profile"
- "I want to add my work experience"
- "Make a new worker profile"

**Voice Assistant Response:**
"Please fill in your full name, age, location, and describe your work experience in the text area. The AI will automatically extract your skills and create a professional profile for you."

---

### Flow 2: Generate Resume
**User Steps:**
1. Go to Resume Generator tab
2. Select a profile from dropdown
3. Click "Generate PDF Resume"
4. Wait for PDF generation
5. Download or view resume

**Voice Assistant Should Understand:**
- "Generate my resume"
- "Create a PDF resume"
- "Make a CV"
- "Download my resume"

**Voice Assistant Response:**
"Select your profile from the dropdown and click Generate PDF Resume. Your ATS-friendly resume will be ready to download."

---

### Flow 3: Find Jobs
**User Steps:**
1. Go to Job Matching tab
2. Select a profile
3. Click "Find Jobs"
4. Review matches with percentages
5. Identify missing skills
6. Click "Apply" for interested jobs

**Voice Assistant Should Understand:**
- "Find jobs for me"
- "Show job matches"
- "What jobs are available?"
- "Search for construction jobs"

**Voice Assistant Response:**
"Select a profile to discover jobs that match your skills. You'll see match percentages, missing skills to develop, and career tips. Use the Apply button to visit job listings."

---

## API Endpoints Reference

### Profiles
- `GET /api/profiles` - List all profiles
- `POST /api/profile` - Create new profile
- `POST /api/profile/{id}/extract-skills` - AI skill extraction
- `POST /api/profile/{id}/summary` - Generate summary
- `PUT /api/profile/{id}` - Update profile
- `DELETE /api/profile/{id}` - Delete profile

### Jobs
- `POST /api/match-jobs` - Match jobs by skills
- `GET /api/profile/{id}/matches` - Get matches for profile
- `GET /api/search` - Search jobs with query
- `POST /api/save/{adzuna_id}` - Save job
- `DELETE /api/save/{adzuna_id}` - Unsave job
- `GET /api/saved` - Get saved jobs
- `POST /api/alerts` - Create job alert
- `GET /api/alerts` - List alerts

### Chat
- `POST /api/chat` - Chat with AI assistant
- `POST /api/speech-to-text` - Transcribe audio

### Utilities
- `GET /health` - API health check
- `GET /api/vapi/config` - VAPI configuration

---

## Key Terminology for Voice Assistant

**Job Categories:**
- Construction Worker
- Delivery Driver
- Domestic Helper
- Electrician
- Gardener
- Mason
- Painter
- Plumber
- Security Guard
- Tailor

**Common Skills:**
- Hard skills: physical labor, electrical wiring, plumbing, painting, sewing, masonry, tool operation, blueprint reading, driving, childcare, cooking, cleaning
- Soft skills: teamwork, safety protocols, time management, communication, organization, leadership, problem-solving

**Job Search Terms:**
- "construction jobs"
- "driver jobs"
- "electrician work"
- "plumbing jobs"
- "security guard positions"

---

## Voice Assistant Training Prompts

### Help & Guidance
**User:** "What can you do?"
**Assistant:** "I'm your AI career assistant. I can help you build profiles, generate resumes, find jobs, and suggest skill improvements. Just ask me anything about using the SkillSetu app."

**User:** "How do I create a profile?"
**Assistant:** "Go to the Profile Builder tab. Fill in your full name, age, and location. Then describe your work experience and skills in the text area. Click 'Generate Professional Profile' and the AI will create it for you."

**User:** "How do I get a job?"
**Assistant:** "First, create a profile to list your skills. Then go to Job Matching, select your profile, and click Find Jobs. I'll show you jobs that match your skills with match percentages."

### Navigation
**User:** "Take me to resume generator"
**Assistant:** "Opening Resume Generator tab... Select a profile from the dropdown and click Generate PDF Resume."

**User:** "Show me job matches"
**Assistant:** "Going to Job Matching tab... Select a profile and click Find Jobs to see matching opportunities."

**User:** "Change language to Hindi"
**Assistant:** "Switching to Hindi... अब आप हिंदी में प्रोफ़ाइल बिल्डर, रिज्यूमे जनरेटर और जॉब मैचिंग का उपयोग कर सकते हैं।"

---

## Technical Notes for Voice Training

**Database Model (WorkerProfile):**
- id: integer (primary key)
- name: string
- age: integer
- location: string
- skills: JSON/text (comma-separated)
- summary: text
- recommended_job_category: string
- created_at: datetime

**Job Matching Algorithm:**
- Normalizes skills to lowercase
- Calculates exact matches
- Adds soft skill bonuses
- Returns top 10 results sorted by match percentage

**Adzuna API Integration:**
- Country: India (IN)
- Query: Combines top 5 user skills
- Fallback: Local jobs.json if API fails
- Retry logic: Simplifies query if no results

**VAPI Assistant Settings:**
- Name: Career Assistant
- First message context: Help users build professional identities for informal sector work
- Capabilities to mention: profile building, resume generation, job matching, skill development advice

---

## Error Handling & Fallbacks

**No Profiles:**
"If no profiles yet: Create a profile first to find matching jobs. Go to Profile Builder and enter your work experience."

**No API Key:**
"Voice assistant unavailable. Please configure your API keys in the backend .env file."

**No Jobs Found:**
"No matching jobs found for your skills. Try adding more skills to your profile or check back later as new jobs are added regularly."

**Microphone Denied:**
"Please allow microphone access to use voice input. Check your browser settings."

---

## Sample Training Conversations

**Conversation 1: Profile Creation**
User: "I'm a construction worker with 5 years experience"
Assistant: "Great! Please go to the Profile Builder and tell me more. What's your name, age, and location? Also list your specific skills like blueprint reading, tool operation, safety protocols, etc."

**Conversation 2: Job Search**
User: "Find me a job"
Assistant: "I can help with that. First, do you have a profile created? If yes, I'll use your skills to find matching jobs. If not, let's create one first."

**Conversation 3: Skill Development**
User: "What skills should I learn?"
Assistant: "Based on your profile, I notice you're missing masonry and painting skills. Consider taking online courses or certifications in these areas. Also, many job listings value teamwork and safety protocols."

---

## Multilingual Support

**English (en):**
- All primary content
- Default language

**Hindi (hi):**
- Devanagari script support
- Translated UI labels
- Voice assistant can respond in Hindi

**Switching:**
- Use dropdown in header
- Voice command: "Switch to Hindi" / "हिंदी में बदलें"

---

## Accessibility Notes

- Screen reader compatible HTML structure
- Keyboard navigation support
- High contrast text (neutral-900 on white)
- Large touch targets for buttons
- Voice input/output support

---

## Performance Tips

- Frontend: Vite dev server on port 5173
- Backend: Uvicorn with reload on port 8000
- Static files served from `/backend/static/`
- Resume PDFs cached in static directory
- Adzuna API timeout: 20 seconds
- Job matching returns max 10 results

---

## Common User Questions

**Q: Is this free?**
A: "Yes! SkillSetu AI is designed for informal workers. No paid APIs. Fully local."

**Q: Where does job data come from?**
A: "We use the Adzuna API to fetch real job listings. If the API is unavailable, we use a local fallback database."

**Q: Can I download my resume?**
A: "Yes, generate your resume and you'll get a PDF file that you can download and share with employers."

**Q: How accurate is job matching?**
A: "We match your skills against job requirements and show you a match percentage. You'll also see which skills you need to develop for better matches."

**Q: Can I save jobs?**
A: "Yes, click the save button on any job listing. You can view all saved jobs in your profile."

---

## Voice Assistant Scope

**DO:**
- Guide users through features
- Explain how to use the app
- Help with navigation
- Provide career advice
- Answer questions about profiles, resumes, and jobs

**DON'T:**
- Make direct profile modifications without user action
- Generate resumes without explicit request
- Apply to jobs on behalf of users
- Store sensitive data beyond session

---

## Emergency Keywords

If user mentions:
- "Emergency" / "Help me" → Provide immediate guidance to create a basic profile
- "I'm confused" → Offer step-by-step walkthrough
- "Not working" → Troubleshoot: check API keys, refresh page, verify profile created
- "Language" → Offer English/Hindi switch

---

## Testing Checklist for Voice Assistant

- [ ] Can guide user to create profile
- [ ] Can explain resume generation
- [ ] Can describe job matching
- [ ] Understands Hindi commands
- [ ] Handles microphone permissions
- [ ] Falls back gracefully when VAPI unavailable
- [ ] Correctly interprets skill-related queries
- [ ] Provides accurate navigation instructions
- [ ] Responds to "help" and "what can you do"
- [ ] Maintains conversation context across tabs

---

## VAPI Assistant Configuration Reference

```javascript
{
  assistantId: "d64fdb17-4eb4-402f-b821-a64ed451e55b",
  apiKey: "cdc52eb6-2fae-4b05-a119-1747a186a9d2",
  position: "bottom-right",
  firstMessage: "Hello! I am your career assistant...",
  model: "gemini-2.0-flash",
  transcriber: "deepgram/nova-2",
  voice: "playht"
}
```

---

## Document Metadata
- **Version:** 1.0
- **Created:** 2025-06-24
- **Purpose:** Voice assistant training and knowledge base
- **Audience:** AI trainers, voice assistant developers