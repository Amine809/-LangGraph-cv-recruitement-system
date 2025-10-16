"""
Advanced agent implementations for recruitment system
"""
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from prompts.agent_prompts import (
    CV_PARSER_PROMPT,
    SKILLS_ANALYZER_PROMPT,
    EXPERIENCE_EVALUATOR_PROMPT,
    CULTURAL_FIT_PROMPT,
    SCORING_AGENT_PROMPT,
    RECOMMENDATION_AGENT_PROMPT
)
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Helpers
def _normalize_parsed_cv(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure parsed CV data exposes the keys expected by the UI with sensible defaults.
    Tries to map common alternative key names returned by the model.
    """
    if not isinstance(parsed, dict):
        return {
            "personal_information": {},
            "work_experience": {},
            "education": {},
            "skills": {}
        }

    def first_present(d: Dict[str, Any], keys):
        for k in keys:
            if k in d and d[k] not in (None, ""):
                return d[k]
        return {}

    normalized = dict(parsed)

    normalized["personal_information"] = first_present(parsed, [
        "personal_information", "personal_info", "personal", "contact_information", "profile"
    ]) or {}

    normalized["work_experience"] = first_present(parsed, [
        "work_experience", "experience", "professional_experience", "employment_history", "work_history"
    ]) or {}

    normalized["education"] = first_present(parsed, [
        "education", "educational_background", "academics"
    ]) or {}

    normalized["skills"] = first_present(parsed, [
        "skills", "skillset", "technical_skills"
    ]) or {}

    return normalized

# Initialize LLM with advanced configuration
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.1,  # Low temperature for consistent, factual output
    max_tokens=4000,
    model_kwargs={
        "response_format": {"type": "json_object"}
    }
)

# LLM for non-JSON outputs
llm_text = ChatOpenAI(
    model="gpt-4o",
    temperature=0.3,
    max_tokens=3000
)

def cv_parser_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 1: Parse CV and extract structured information
    """
    print("🔍 CV Parser Agent: Analyzing resume...")
    
    prompt = CV_PARSER_PROMPT.format(cv_text=state['cv_text'])
    
    messages = [
        SystemMessage(content="You are an expert CV parser. Always respond with valid JSON."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        parsed_data = json.loads(response.content)
        parsed_data = _normalize_parsed_cv(parsed_data)
        
        return {
            **state,
            "parsed_cv": parsed_data,
            "current_agent": "cv_parser",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"CV Parser Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "parsed_cv": {"error": error_msg}
        }

def skills_analyzer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 2: Deep skills analysis
    """
    print("💡 Skills Analyzer Agent: Evaluating competencies...")
    
    prompt = SKILLS_ANALYZER_PROMPT.format(
        job_requirements=state['job_requirements'],
        parsed_data=json.dumps(state['parsed_cv'], indent=2)
    )
    
    messages = [
        SystemMessage(content="You are an expert skills assessor. Always respond with valid JSON."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        analysis = json.loads(response.content)
        
        return {
            **state,
            "skills_analysis": analysis,
            "current_agent": "skills_analyzer",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"Skills Analyzer Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "skills_analysis": {"error": error_msg}
        }

def experience_evaluator_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 3: Evaluate work experience and career trajectory
    """
    print("📊 Experience Evaluator Agent: Assessing career history...")
    
    prompt = EXPERIENCE_EVALUATOR_PROMPT.format(
        job_requirements=state['job_requirements'],
        parsed_data=json.dumps(state['parsed_cv'], indent=2)
    )
    
    messages = [
        SystemMessage(content="You are an expert career evaluator. Always respond with valid JSON."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        evaluation = json.loads(response.content)
        
        return {
            **state,
            "experience_evaluation": evaluation,
            "current_agent": "experience_evaluator",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"Experience Evaluator Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "experience_evaluation": {"error": error_msg}
        }

def cultural_fit_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 4: Assess cultural fit
    """
    print("🎯 Cultural Fit Agent: Analyzing alignment...")
    
    prompt = CULTURAL_FIT_PROMPT.format(
        company_culture=state['company_culture'],
        parsed_data=json.dumps(state['parsed_cv'], indent=2)
    )
    
    messages = [
        SystemMessage(content="You are an expert in organizational culture assessment. Always respond with valid JSON."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        assessment = json.loads(response.content)
        
        return {
            **state,
            "cultural_fit_assessment": assessment,
            "current_agent": "cultural_fit",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"Cultural Fit Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "cultural_fit_assessment": {"error": error_msg}
        }

def scoring_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 5: Aggregate scoring and risk assessment
    """
    print("⚖️ Scoring Agent: Calculating final scores...")
    
    prompt = SCORING_AGENT_PROMPT.format(
        skills_analysis=json.dumps(state['skills_analysis'], indent=2),
        experience_evaluation=json.dumps(state['experience_evaluation'], indent=2),
        cultural_fit=json.dumps(state['cultural_fit_assessment'], indent=2)
    )
    
    messages = [
        SystemMessage(content="You are an expert recruitment scorer. Always respond with valid JSON."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm.invoke(messages)
        scores = json.loads(response.content)
        
        return {
            **state,
            "aggregate_score": scores,
            "current_agent": "scoring_agent",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"Scoring Agent Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "aggregate_score": {"error": error_msg}
        }

def recommendation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent 6: Final hiring recommendation
    """
    print("✅ Recommendation Agent: Generating final decision...")
    
    prompt = RECOMMENDATION_AGENT_PROMPT.format(
        aggregate_assessment=json.dumps(state['aggregate_score'], indent=2),
        job_requirements=state['job_requirements']
    )
    
    messages = [
        SystemMessage(content="You are an expert hiring advisor. Provide clear recommendations."),
        HumanMessage(content=prompt)
    ]
    
    try:
        response = llm_text.invoke(messages)
        
        # Try to parse as JSON, fallback to text
        try:
            recommendation = json.loads(response.content)
        except:
            recommendation = {"recommendation": response.content}
        
        return {
            **state,
            "final_recommendation": recommendation,
            "current_agent": "recommendation_agent",
            "workflow_status": "completed",
            "messages": state.get("messages", []) + [response]
        }
    except Exception as e:
        error_msg = f"Recommendation Agent Error: {str(e)}"
        return {
            **state,
            "errors": state.get("errors", []) + [error_msg],
            "final_recommendation": {"error": error_msg},
            "workflow_status": "failed"
        }