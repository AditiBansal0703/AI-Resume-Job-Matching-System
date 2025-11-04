import os, re, json
from pathlib import Path
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
from dateutil import parser as dateparser

def _extract_text_from_pdf(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text()
                if txt:
                    text += "\n" + txt
    except Exception:
        text = ""
    return text.strip()

def _extract_text_from_docx(path):
    doc = Document(path)
    texts = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(texts)

def _extract_text_from_image(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def parse_resume_file(path):
    p = Path(path)
    ext = p.suffix.lower().lstrip('.')
    raw_text = ""
    if ext == "pdf":
        raw_text = _extract_text_from_pdf(path)
        if not raw_text:
            pass
    elif ext in ["docx"]:
        raw_text = _extract_text_from_docx(path)
    elif ext in ["txt"]:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            raw_text = f.read()
    elif ext in ["png","jpg","jpeg"]:
        raw_text = _extract_text_from_image(path)
    else:
        raw_text = ""
    structured = simple_information_extraction(raw_text)
    return {"raw_text": raw_text, "structured": structured}


def simple_information_extraction(text):
    if not text or not text.strip():
        return {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    joined = "\n".join(lines[:400])
 
    name = lines[0] if lines else ""

    email_match = re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    email = email_match.group(0) if email_match else None
    phone_match = re.search(r'\+?\d[\d\-\s()]{7,}\d', text)
    phone = phone_match.group(0) if phone_match else None

    skills = []
    for i,l in enumerate(lines):
        if l.lower().startswith("skills") or l.lower().startswith("technical skills"):
            for j in range(i+1, min(i+8, len(lines))):
                parts = re.split(r'[,:;\|•\-]', lines[j])
                for p in parts:
                    if p and len(p.strip())>1:
                        skills.append(p.strip())
            break

    experiences = []
    for l in lines:
        if re.search(r'\b(19|20)\d{2}\b', l):
            experiences.append(l)

    education = []
    for l in lines:
        if any(x in l.lower() for x in ['university','institute','college','bachelor','master','phd','bs ','b.sc','m.sc']):
            education.append(l)

    return {
        "name_guess": name,
        "email": email,
        "phone": phone,
        "skills_raw": skills,
        "experience_snippets": experiences[:5],
        "education_snippets": education[:5]
    }
