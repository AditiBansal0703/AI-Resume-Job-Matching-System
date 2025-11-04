from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import uuid
import fitz  # PyMuPDF (for PDFs)
import docx
import io

app = FastAPI(title="AI Resume Parser API", version="2.0")

# Enable frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
db = {}


# 🩺 Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Resume upload + parse
@app.post("/api/v1/resumes/upload")
async def upload_resume(file: UploadFile = File(...)):
    resume_id = str(uuid.uuid4())

    # Extract text content based on file type
    file_bytes = await file.read()
    text_content = extract_text(file.filename, file_bytes)

    db[resume_id] = {
        "file_name": file.filename,
        "resume_text": text_content,
    }

    return {"id": resume_id, "message": "Resume uploaded successfully"}


# Match resume with job description
@app.post("/api/v1/resumes/{resume_id}/match")
async def match_resume(resume_id: str, job_description: str = Form(...)):
    if resume_id not in db:
        return {"error": "Resume not found"}

    resume_text = db[resume_id]["resume_text"]

    # Real AI logic — text similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity_score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    score = round(similarity_score * 100, 2)

    # Additional analysis — skill overlap
    skills = extract_skills(resume_text)
    overlap = [s for s in skills if s.lower() in job_description.lower()]

    # Smart suggestion based on score
    if score > 80:
        suggestion = "Excellent Match — Candidate fits the job description well."
    elif score > 60:
        suggestion = "Moderate Match — Some relevant skills present, could improve."
    else:
        suggestion = "Weak Match — Resume and job description mismatch."

    return {
        "file": db[resume_id]["file_name"],
        "match_score": score,
        "skills_found": skills,
        "matching_skills": overlap,
        "suggestion": suggestion,
    }


# Utility: Extract text from resume
def extract_text(filename: str, file_bytes: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = "".join([page.get_text("text") for page in doc])
    elif filename.lower().endswith(".docx"):
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        text = file_bytes.decode(errors="ignore")
    return text


# Utility: Extract skills (simple keyword matcher)
def extract_skills(text: str):
    skill_keywords = [
        "python", "java", "sql", "machine learning", "data analysis",
        "excel", "communication", "leadership", "nlp", "deep learning",
        "django", "flask", "javascript", "html", "css", "react", "power bi",
        "tableau", "statistics", "data visualization"
    ]
    text_lower = text.lower()
    found = [s for s in skill_keywords if s in text_lower]
    return list(set(found))
