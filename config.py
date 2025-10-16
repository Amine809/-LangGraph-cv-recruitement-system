"""
Configuration settings for the recruitment system
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"
OPENAI_TEMPERATURE = 0.1
MAX_TOKENS = 4000

# Agent Configuration
AGENT_TIMEOUT = 120  # seconds
MAX_RETRIES = 3

# Scoring Weights
SCORING_WEIGHTS = {
    "skills_match": 0.35,
    "experience_quality": 0.30,
    "cultural_fit": 0.20,
    "career_progression": 0.15
}

# Score Thresholds
SCORE_THRESHOLDS = {
    "strong_yes": 90,
    "yes": 75,
    "maybe": 60,
    "no": 40,
    "strong_no": 0
}

# Workflow Configuration
WORKFLOW_TYPES = ["sequential", "parallel", "conditional"]
DEFAULT_WORKFLOW = "sequential"

# File Upload Settings
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Storage Settings
DATA_DIR = "data"
ASSESSMENTS_DIR = os.path.join(DATA_DIR, "assessments")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

# Create directories if they don't exist
os.makedirs(ASSESSMENTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Skills Database (expandable)
TECHNICAL_SKILLS = [
    # Programming Languages
    "python", "javascript", "java", "c++", "c#", "go", "rust", "typescript",
    "ruby", "php", "swift", "kotlin", "scala",
    
    # Frameworks
    "react", "angular", "vue", "django", "flask", "fastapi", "spring boot",
    "node.js", "express", ".net", "laravel",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins",
    "github actions", "gitlab ci", "ansible",
    
    # Databases
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "dynamodb",
    "cassandra", "oracle",
    
    # AI/ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "nlp", "computer vision", "langchain", "llm",
    
    # Others
    "git", "linux", "agile", "scrum", "rest api", "graphql", "microservices"
]

SOFT_SKILLS = [
    "leadership", "communication", "teamwork", "problem-solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "emotional intelligence", "conflict resolution", "decision making",
    "mentoring", "project management"
]

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# UI Configuration
STREAMLIT_THEME = {
    "primaryColor": "#1f77b4",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#262730",
    "font": "sans serif"
}