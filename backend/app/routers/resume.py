from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.database import SessionLocal, WorkerProfile
import os

router = APIRouter()

class ResumeRequest(BaseModel):
    profile_id: int

FONT_REGISTERED = False

def ensure_font():
    global FONT_REGISTERED
    if FONT_REGISTERED:
        return
    try:
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\NotoSans-Regular.ttf",
        ]
        for path in font_paths:
            if os.path.exists(path):
                pdfmetrics.registerFont(TTFont('BaseFont', path))
                FONT_REGISTERED = True
                return
    except Exception:
        pass


def generate_pdf(profile: WorkerProfile, output_path: str):
    ensure_font()
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    base_name = 'BaseFont' if FONT_REGISTERED else styles['Normal'].fontName
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=base_name,
        fontSize=24,
        spaceAfter=20,
        textColor='#1a1a1a'
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=base_name,
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor='#2563eb',
        borderWidth=0,
        borderColor='#2563eb',
        borderPadding=5
    )
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=base_name,
        fontSize=10,
        leading=14
    )
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=20,
        textColor='#1a1a1a'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=12,
        textColor='#2563eb',
        borderWidth=0,
        borderColor='#2563eb',
        borderPadding=5
    )
    
    content = []
    
    # Header
    content.append(Paragraph(f"{profile.name}", title_style))
    if profile.location:
        content.append(Paragraph(f"Location: {profile.location}", body_style))
    if profile.age:
        content.append(Paragraph(f"Age: {profile.age}", body_style))
    content.append(Spacer(1, 0.2*inch))

    # Skills
    content.append(Paragraph("Skills", heading_style))
    if profile.skills:
        skills_list = profile.skills.split(", ")
        for skill in skills_list:
            content.append(Paragraph(f"• {skill}", body_style))
    else:
        content.append(Paragraph("No skills extracted yet.", body_style))
    content.append(Spacer(1, 0.1*inch))

    # Experience Summary
    content.append(Paragraph("Professional Summary", heading_style))
    if profile.experience_summary:
        content.append(Paragraph(profile.experience_summary, body_style))
    else:
        content.append(Paragraph("No summary available.", body_style))
    content.append(Spacer(1, 0.1*inch))

    # Work Experience
    content.append(Paragraph("Work Experience", heading_style))
    content.append(Paragraph(profile.work_experience, body_style))
    content.append(Spacer(1, 0.1*inch))

    # Recommended Category
    if profile.recommended_job_category:
        content.append(Paragraph("Recommended Job Category", heading_style))
        content.append(Paragraph(profile.recommended_job_category, body_style))
    
    doc.build(content)

@router.post("/resume/{profile_id}")
def generate_resume(profile_id: int):
    db = SessionLocal()
    try:
        profile = db.query(WorkerProfile).filter(WorkerProfile.id == profile_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        filename = f"resume_{profile_id}_{uuid.uuid4().hex[:8]}.pdf"
        output_dir = os.path.join("backend", "static")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        
        generate_pdf(profile, output_path)
        
        return {"download_url": f"/static/{filename}"}
    finally:
        db.close()

@router.get("/resume/download/{filename}")
def download_resume(filename: str):
    file_path = os.path.join("backend", "static", filename)
    if not os.path.exists(file_path):
        alt_path = os.path.join("static", filename)
        if os.path.exists(alt_path):
            file_path = alt_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='application/pdf', filename=filename)