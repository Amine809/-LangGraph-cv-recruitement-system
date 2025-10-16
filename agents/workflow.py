"""
Advanced LangGraph workflow for recruitment system
Following official LangGraph patterns and best practices
"""
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from agents.recruitment_agents import (
    cv_parser_agent,
    skills_analyzer_agent,
    experience_evaluator_agent,
    cultural_fit_agent,
    scoring_agent,
    recommendation_agent
)

def create_recruitment_workflow():
    """
    Creates the LangGraph workflow for CV recruitment analysis
    
    Workflow: CV Parser → Skills Analyzer → Experience Evaluator → 
              Cultural Fit → Scoring Agent → Recommendation Agent
    """
    
    # Initialize StateGraph
    workflow = StateGraph(dict)
    
    # Add nodes (agents)
    workflow.add_node("cv_parser", cv_parser_agent)
    workflow.add_node("skills_analyzer", skills_analyzer_agent)
    workflow.add_node("experience_evaluator", experience_evaluator_agent)
    workflow.add_node("cultural_fit", cultural_fit_agent)
    workflow.add_node("scoring_agent", scoring_agent)
    workflow.add_node("recommendation", recommendation_agent)
    
    # Define edges (workflow sequence)
    workflow.set_entry_point("cv_parser")
    
    workflow.add_edge("cv_parser", "skills_analyzer")
    workflow.add_edge("skills_analyzer", "experience_evaluator")
    workflow.add_edge("experience_evaluator", "cultural_fit")
    workflow.add_edge("cultural_fit", "scoring_agent")
    workflow.add_edge("scoring_agent", "recommendation")
    workflow.add_edge("recommendation", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

def create_parallel_workflow():
    """
    Alternative workflow with parallel agent execution
    Skills, Experience, and Cultural Fit run in parallel
    """
    
    workflow = StateGraph(dict)
    
    # Add all nodes
    workflow.add_node("cv_parser", cv_parser_agent)
    workflow.add_node("skills_analyzer", skills_analyzer_agent)
    workflow.add_node("experience_evaluator", experience_evaluator_agent)
    workflow.add_node("cultural_fit", cultural_fit_agent)
    workflow.add_node("scoring_agent", scoring_agent)
    workflow.add_node("recommendation", recommendation_agent)
    
    # CV Parser runs first
    workflow.set_entry_point("cv_parser")
    
    # After CV parsing, three agents run in parallel
    workflow.add_edge("cv_parser", "skills_analyzer")
    workflow.add_edge("cv_parser", "experience_evaluator")
    workflow.add_edge("cv_parser", "cultural_fit")
    
    # All three feed into scoring agent
    workflow.add_edge("skills_analyzer", "scoring_agent")
    workflow.add_edge("experience_evaluator", "scoring_agent")
    workflow.add_edge("cultural_fit", "scoring_agent")
    
    # Final recommendation
    workflow.add_edge("scoring_agent", "recommendation")
    workflow.add_edge("recommendation", END)
    
    app = workflow.compile()
    
    return app

def create_conditional_workflow():
    """
    Advanced workflow with conditional routing based on scores
    """
    
    def should_continue_evaluation(state: Dict[str, Any]) -> str:
        """
        Decides if full evaluation should continue based on initial skills assessment
        """
        skills_analysis = state.get('skills_analysis', {})
        
        # Check if skills match score exists and is above threshold
        if 'skills_match' in skills_analysis:
            skills_score = skills_analysis.get('skills_match', 0)
            if skills_score < 4:  # Below 4/10 threshold
                return "early_reject"
        
        return "continue_evaluation"
    
    workflow = StateGraph(dict)
    
    # Add nodes
    workflow.add_node("cv_parser", cv_parser_agent)
    workflow.add_node("skills_analyzer", skills_analyzer_agent)
    workflow.add_node("experience_evaluator", experience_evaluator_agent)
    workflow.add_node("cultural_fit", cultural_fit_agent)
    workflow.add_node("scoring_agent", scoring_agent)
    workflow.add_node("recommendation", recommendation_agent)
    
    # Early rejection node
    def early_rejection(state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            **state,
            "final_recommendation": {
                "decision": "Rejected - Insufficient Skills Match",
                "reason": "Candidate does not meet minimum skill requirements"
            },
            "workflow_status": "completed"
        }
    
    workflow.add_node("early_reject", early_rejection)
    
    # Define workflow
    workflow.set_entry_point("cv_parser")
    workflow.add_edge("cv_parser", "skills_analyzer")
    
    # Conditional routing after skills analysis
    workflow.add_conditional_edges(
        "skills_analyzer",
        should_continue_evaluation,
        {
            "continue_evaluation": "experience_evaluator",
            "early_reject": "early_reject"
        }
    )
    
    # Continue normal flow
    workflow.add_edge("experience_evaluator", "cultural_fit")
    workflow.add_edge("cultural_fit", "scoring_agent")
    workflow.add_edge("scoring_agent", "recommendation")
    
    # End points
    workflow.add_edge("recommendation", END)
    workflow.add_edge("early_reject", END)
    
    app = workflow.compile()
    
    return app

# Export default workflow
def get_workflow(workflow_type: str = "sequential"):
    """
    Get compiled workflow based on type
    
    Args:
        workflow_type: 'sequential', 'parallel', or 'conditional'
    
    Returns:
        Compiled LangGraph application
    """
    workflows = {
        "sequential": create_recruitment_workflow,
        "parallel": create_parallel_workflow,
        "conditional": create_conditional_workflow
    }
    
    creator = workflows.get(workflow_type, create_recruitment_workflow)
    return creator()