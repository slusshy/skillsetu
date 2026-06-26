from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
from app.services import extract_profile
import os

# Voice features are optional
try:
    from deepgram import DeepgramClient
    from deepgram.rest.types import PrerecordedOptions
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    profile_id: Optional[int] = None
    language: Optional[str] = "en"

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]


class TranscriptionResponse(BaseModel):
    transcript: str
    language: Optional[str] = "en"

@router.post("/speech-to-text", response_model=TranscriptionResponse)
async def speech_to_text(file: UploadFile = File(...), language: Optional[str] = "en"):
    try:
        api_key = os.getenv("DEEPGRAM_API_KEY", "")
        if not api_key:
            raise HTTPException(status_code=500, detail="DEEPGRAM_API_KEY not configured")

        audio_bytes = await file.read()

        deepgram = DeepgramClient(api_key)

        payload = {"buffer": audio_bytes}

        options = PrerecordedOptions(
            model="nova-2",
            language=language,
            smart_format=True,
        )

        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        transcript = (
            response["results"]["channels"][0]["alternatives"][0]["transcript"]
        )

        return TranscriptionResponse(transcript=transcript, language=language)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
def chat(message: ChatMessage):
    try:
        # Use Gemini for intelligent chat responses
        response_text, suggestions = get_gemini_chat_response(message.message, message.language)
        
        return ChatResponse(response=response_text, suggestions=suggestions)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_gemini_chat_response(user_message: str, language: str = "en") -> tuple[str, list]:
    """Use Gemini to generate intelligent chat responses."""
    try:
        import google.generativeai as genai
        import os
        
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            return get_fallback_response(user_message)
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        lang_instruction = "Respond in English." if language != "hi" else "Respond in Hindi (Devanagari script)."
        
        prompt = f"""You are a helpful career assistant for SkillSetu AI, an app that helps informal workers build professional identities.

Your capabilities:
1. Help users build professional profiles from their work experience
2. Generate ATS-friendly PDF resumes
3. Match users' skills with job listings
4. Provide career advice and skill development tips

User message: {user_message}

{lang_instruction}

Provide a helpful, concise response (2-3 sentences max). Then suggest 2-3 relevant actions the user can take from this list:
- Build Profile
- Generate Resume  
- Find Jobs
- View Profiles

Format your response as JSON:
{{"response": "your response here", "suggestions": ["suggestion1", "suggestion2", "suggestion3"]}}

Return ONLY valid JSON, no markdown or extra text."""

        response = model.generate_content(prompt)
        text = getattr(response, "text", "").strip()
        
        # Parse JSON response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        
        import json
        data = json.loads(text)
        return data.get("response", ""), data.get("suggestions", [])
    
    except Exception as e:
        print(f"Gemini chat error: {e}")
        return get_fallback_response(user_message)


def get_fallback_response(user_message: str) -> tuple[str, list]:
    """Fallback responses when Gemini is not available."""
    user_message_lower = user_message.lower()
    
    if any(word in user_message_lower for word in ["resume", "cv"]):
        return "I can help you create a professional resume. Go to the Resume Generator tab and select your profile.", ["Generate Resume", "View Profiles"]
    elif any(word in user_message_lower for word in ["job", "work", "career"]):
        return "I can help you find matching jobs based on your skills. Visit the Job Matching tab.", ["Find Jobs", "Build Profile"]
    elif any(word in user_message_lower for word in ["skill", "learn", "improve"]):
        return "To improve your skills, focus on the missing skills from your job matches. Take online courses or get certified.", ["Find Jobs", "Build Profile"]
    elif any(word in user_message_lower for word in ["help", "what can you do"]):
        return "I'm your AI career assistant. I can help you build profiles, generate resumes, find jobs, and suggest skill improvements.", ["Build Profile", "Find Jobs", "Generate Resume"]
    else:
        return "I'm here to help you build your professional identity. Ask me about profiles, resumes, or jobs.", ["Build Profile", "Find Jobs"]


