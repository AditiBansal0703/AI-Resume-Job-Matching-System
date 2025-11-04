import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resumes.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(String, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False)
    file_hash = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    processing_status = Column(String, default="processing")
    raw_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True)
    ai_enhancements = Column(JSON, nullable=True)
    extra_metadata = Column(JSON, nullable=True)
    processing_time = Column(Float, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def create_session():
    return SessionLocal()

def save_raw_and_structured(session, resume_id, file_path, structured, processing_time):
    r = session.query(Resume).filter_by(id=resume_id).first()
    if not r:
        return
    r.raw_text = structured.get("raw_text")
    r.structured_data = structured.get("structured")
    r.processed_at = datetime.utcnow()
    r.processing_time = processing_time
    r.processing_status = "done"
    session.add(r)
    session.commit()
