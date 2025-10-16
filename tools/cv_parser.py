"""
Advanced CV Parser Tool for extracting structured data from resumes
"""
import PyPDF2
import docx
from typing import Dict, Any
from langchain.tools import tool
import re

@tool
def parse_cv_from_text(cv_text: str) -> Dict[str, Any]:
    """
    Parse CV text and extract structured information.
    
    Args:
        cv_text: Raw text content of the CV
    
    Returns:
        Dictionary with extracted CV information
    """
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, cv_text)
    
    # Extract phone numbers
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, cv_text)
    
    # Extract years of experience (rough estimation)
    year_pattern = r'\b(19|20)\d{2}\b'
    years = re.findall(year_pattern, cv_text)
    
    return {
        "raw_text": cv_text,
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "years_mentioned": sorted(set(years), reverse=True),
        "text_length": len(cv_text),
        "word_count": len(cv_text.split())
    }

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from DOCX file"""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

@tool
def extract_skills_keywords(text: str, skill_list: str) -> Dict[str, Any]:
    """
    Extract skills from CV text based on a predefined skill list.
    
    Args:
        text: CV text content
        skill_list: Comma-separated list of skills to search for
    
    Returns:
        Dictionary with found skills and their frequencies
    """
    skills = [s.strip().lower() for s in skill_list.split(',')]
    text_lower = text.lower()
    
    found_skills = {}
    for skill in skills:
        count = text_lower.count(skill)
        if count > 0:
            found_skills[skill] = count
    
    return {
        "found_skills": found_skills,
        "total_skills_found": len(found_skills),
        "skill_density": len(found_skills) / len(skills) if skills else 0
    }