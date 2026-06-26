from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)

from app.database import engine, Base
from app.routers import profiles, jobs, resume, chat

app = FastAPI(title="SkillSetu AI API")
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(profiles.router, prefix="/api", tags=["profiles"])
app.include_router(jobs.router, prefix="/api", tags=["jobs"])
app.include_router(resume.router, prefix="/api", tags=["resume"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/vapi/config")
def vapi_config():
    api_key = os.getenv("VAPI_API_KEY", "")
    return {"api_key": api_key}

@app.get("/debug/gemini")
def debug_gemini():
    try:
        import google.generativeai as genai
        import os
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            return {"gemini_configured": False, "reason": "missing_api_key"}
        genai.configure(api_key=api_key)
        models = genai.list_models()
        model_names = []
        for m in models:
            name = getattr(m, "name", "") or getattr(m, "model_name", "") or ""
            if name:
                model_names.append(name)
        if "models/gemini-1.5-flash-002" in model_names:
            model_name = "gemini-1.5-flash-002"
        elif "models/gemini-1.5-flash" in model_names:
            model_name = "gemini-1.5-flash"
        elif model_names:
            model_name = model_names[0].split("/")[-1]
        else:
            return {"gemini_configured": False, "error": "no_models_found"}
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Reply with exactly: OK")
        text = getattr(response, "text", "") or ""
        return {"gemini_configured": True, "model": model_name, "response": text, "available": model_names[:10]}
    except Exception as e:
        return {"gemini_configured": False, "error": str(e)}
