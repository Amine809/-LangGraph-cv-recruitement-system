"""
State management for the recruitment multi-agent system
"""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class RecruitmentState(TypedDict):
    """
    State schema for the recruitment workflow
    """
    # Input data
    cv_text: str
    job_requirements: str
    company_culture: str
    
    # Agent outputs
    parsed_cv: Dict[str, Any]
    skills_analysis: Dict[str, Any]
    experience_evaluation: Dict[str, Any]
    cultural_fit_assessment: Dict[str, Any]
    aggregate_score: Dict[str, Any]
    final_recommendation: Dict[str, Any]
    
    # Workflow metadata
    messages: Annotated[List[BaseMessage], add_messages]
    current_agent: str
    workflow_status: str
    errors: List[str]

class CandidateProfile(TypedDict):
    """Structured candidate profile"""
    name: str
    email: str
    phone: str
    location: str
    summary: str
    experience_years: int
    education: List[Dict[str, Any]]
    work_history: List[Dict[str, Any]]
    skills: Dict[str, List[str]]
    certifications: List[str]
    projects: List[Dict[str, Any]]

class AssessmentScores(TypedDict):
    """Standardized scoring structure"""
    overall_score: float
    skills_score: float
    experience_score: float
    cultural_fit_score: float
    career_progression_score: float
    risk_level: str
    recommendation: str
    strengths: List[str]
    weaknesses: List[str]
    interview_focus: List[str]