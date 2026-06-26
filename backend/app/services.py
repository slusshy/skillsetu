import os
import json
import requests
from sqlalchemy.orm import Session
from app.database import WorkerProfile

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def _parse_extraction_text(text: str) -> dict:
    raw = text.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        if len(parts) >= 3:
            raw = parts[1]
            if raw.startswith("json"):
                raw = raw[4:]
    raw = raw.strip()
    try:
        data = json.loads(raw)
    except Exception as e:
        print(f"JSON parse failed: {e}; source={text!r}")
        return {
            "skills": [],
            "experience_summary": "Unable to analyze experience at this time.",
            "recommended_job_category": "General",
        }
    skills = data.get("skills") or []
    summary = data.get("experience_summary") or ""
    category = data.get("recommended_job_category") or ""
    if not skills and not summary and not category:
        print(f"Empty extracted fields; source={text!r}")
    return {
        "skills": skills,
        "experience_summary": summary,
        "recommended_job_category": category,
    }


def _build_prompt(work_experience: str, language: str) -> str:
    lang = "English" if language != "hi" else "Hindi (Devanagari script)"
    return (
        "You are a professional resume coach.\n"
        f"User's raw experience: {work_experience}\n\n"
        "Do NOT copy-paste the input. Expand it into a polished professional profile.\n\n"
        "Return ONLY a JSON object. No markdown. No extra text.\n\n"
        "Required JSON:\n"
        '{"skills":["..."],"experience_summary":"...","recommended_job_category":"..."}\n\n'
        f"Rules:\n- Use {lang} in the value fields\n- skills: infer 6-15 relevant hard and soft skills from the text and likely role context\n"
        "- experience_summary: 3-5 sentences, professionally worded, include scope, tools/equipment, safety/quality, and teamwork/leadership if implied\n"
        "- recommended_job_category: choose the closest standard role/category"
    )


def extract_profile_with_ollama(work_experience: str, language: str = "en") -> dict:
    prompt = _build_prompt(work_experience, language)
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 1024},
            },
            timeout=120,
        )
        response.raise_for_status()
        text = response.json().get("response", "")
        return _parse_extraction_text(text)
    except Exception as e:
        print(f"Ollama error: {e}")
        raise


def extract_profile_with_gemini(work_experience: str, language: str = "en") -> dict:
    try:
        import google.generativeai as genai

        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = _build_prompt(work_experience, language)
        response = model.generate_content(prompt)
        text = getattr(response, "text", "") or ""
        if not text.strip():
            print("Gemini returned empty text")
            raise ValueError("empty gemini text")
        return _parse_extraction_text(text)
    except Exception as e:
        print(f"Gemini error: {e}")
        raise


def _fallback_extraction(work_experience: str) -> dict:
    text = (work_experience or "").strip()
    lower = text.lower()
    skills = []
    seen = set()
    mapping = {
        "electrical": ["electrical wiring", "circuit troubleshooting", "safety standards", "panel installation", "fault diagnosis"],
        "wiring": ["electrical wiring", "circuit reading"],
        "circuit": ["circuit troubleshooting", "control circuits"],
        "panel": ["panel installation", "maintenance"],
        "maintenance": ["preventive maintenance", "repair"],
        "troubleshooting": ["fault diagnosis", "problem solving"],
        "plumbing": ["pipe installation", "leak repair", "drain cleaning"],
        "pipe": ["pipe fitting", "piping systems"],
        "fitting": ["switchboard fitting", "fixture installation"],
        "welding": ["arc welding", "fabrication"],
        "fabrication": ["metal fabrication", "assembly"],
        "construction": ["site safety", "material handling", "supervision"],
        "driving": ["vehicle operation", "route management"],
        "delivery": ["time management", "customer service"],
        "security": ["surveillance", "patrolling", "emergency response"],
        "tailoring": ["sewing", "measurement", "fabric cutting"],
        "sewing": ["stitching", "finishing"],
        "measuring": ["precision measurement", "quality checking"],
        "computer": ["basic computing", "data entry"],
        "typing": ["documentation", "data entry"],
        "team": ["teamwork", "collaboration"],
        "safety": ["safety standards", "PPE compliance"],
        "freelance": ["client management", "project scheduling"],
        "supervision": ["team supervision", "site coordination"],
        "blueprint": ["drawing interpretation", "layout reading"],
        "tool": ["hand tools", "power tools"],
        "machine": ["machine operation", "equipment handling"]
    }
    for key, values in mapping.items():
        if key in lower and key not in seen:
            skills.extend(values)
            seen.add(key)
    skills = sorted(set(skills))[:15]

    category = "General"
    if any(k in lower for k in ["electrical", "electrician", "wiring", "circuit", "panel"]):
        category = "Electrician"
    elif any(k in lower for k in ["plumb", "pipe", "fitting"]):
        category = "Plumber"
    elif any(k in lower for k in ["weld", "fabricat", "construct"]):
        category = "Fabricator / Construction"
    elif any(k in lower for k in ["drive", "delivery", "vehicle"]):
        category = "Delivery / Driver"
    elif any(k in lower for k in ["secur", "guard", "patrol"]):
        category = "Security"
    elif any(k in lower for k in ["sew", "tailor", "cloth", "fabric"]):
        category = "Tailor"

    sentences = [s.strip() for s in text.split(".") if s.strip()]
    summary = ".".join(sentences[:4])
    if not summary:
        summary = text
    return {
        "skills": skills,
        "experience_summary": summary,
        "recommended_job_category": category,
    }


def extract_profile(work_experience: str, language: str = "en") -> dict:
    gemini_ok = False
    if GEMINI_API_KEY:
        try:
            result = extract_profile_with_gemini(work_experience, language=language)
            if result and any(v for v in (result.get("skills") or [], result.get("experience_summary") or "", result.get("recommended_job_category") or "")):
                gemini_ok = True
            else:
                print("Gemini returned no usable fields; using fallback")
        except Exception as e:
            print(f"Gemini failed: {e}")
    if not gemini_ok:
        try:
            result = extract_profile_with_ollama(work_experience, language=language)
            if result and any(v for v in (result.get("skills") or [], result.get("experience_summary") or "", result.get("recommended_job_category") or "")):
                return result
        except Exception as e:
            print(f"Ollama failed: {e}")
        return _fallback_extraction(work_experience)
    return result if 'result' in locals() else _fallback_extraction(work_experience)
