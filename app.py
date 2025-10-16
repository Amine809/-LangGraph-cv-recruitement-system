"""
Advanced Streamlit UI for CV Recruitment Multi-Agent System
"""
import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from agents.workflow import get_workflow
from utils.serialization import to_json_safe
from tools.cv_parser import extract_text_from_pdf, extract_text_from_docx
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Recruitment System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .score-high {
        color: #00cc00;
        font-weight: bold;
    }
    .score-medium {
        color: #ff9900;
        font-weight: bold;
    }
    .score-low {
        color: #ff0000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'workflow_executed' not in st.session_state:
        st.session_state.workflow_executed = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = ""

def create_score_gauge(score, title):
    """Create a gauge chart for scores"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20}},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': '#ffcccc'},
                {'range': [40, 70], 'color': '#ffffcc'},
                {'range': [70, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    return fig

def create_skills_chart(skills_analysis):
    """Create radar chart for skills assessment"""
    if not skills_analysis or 'error' in skills_analysis:
        return None
    
    categories = []
    scores = []
    
    # Extract scores from analysis
    for key, value in skills_analysis.items():
        if isinstance(value, (int, float)) and 0 <= value <= 10:
            categories.append(key.replace('_', ' ').title())
            scores.append(value * 10)  # Convert to 0-100 scale
    
    if not categories:
        return None
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        height=400,
        title="Skills Assessment Breakdown"
    )
    
    return fig

def display_results(results):
    """Display comprehensive results in organized tabs"""
    
    st.success("✅ Analysis Complete!")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "🎯 Detailed Analysis", 
        "💡 Skills Deep Dive",
        "📈 Experience Review",
        "✅ Final Recommendation"
    ])
    
    # TAB 1: Overview
    with tab1:
        st.header("Candidate Assessment Overview")
        
        # Display overall score
        aggregate = results.get('aggregate_score', {})
        
        if 'error' not in aggregate:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                overall_score = aggregate.get('overall_score', 0)
                st.plotly_chart(
                    create_score_gauge(overall_score, "Overall Score"),
                    use_container_width=True
                )
            
            with col2:
                st.metric("Recommendation", aggregate.get('recommendation', 'N/A'))
                st.metric("Risk Level", aggregate.get('risk_level', 'N/A'))
            
            with col3:
                # Category scores
                st.subheader("Category Scores")
                for key, value in aggregate.items():
                    if 'score' in key.lower() and isinstance(value, (int, float)):
                        score_class = "score-high" if value >= 70 else "score-medium" if value >= 40 else "score-low"
                        st.markdown(f"{key.replace('_', ' ').title()}: <span class='{score_class}'>{value}/100</span>", 
                                  unsafe_allow_html=True)
            
            # Strengths and Weaknesses
            st.subheader("Key Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💪 Strengths:**")
                strengths = aggregate.get('strengths', [])
                if isinstance(strengths, list):
                    for strength in strengths:
                        st.markdown(f"- {strength}")
                else:
                    st.info("No strengths data available")
            
            with col2:
                st.markdown("**⚠️ Areas of Concern:**")
                weaknesses = aggregate.get('weaknesses', [])
                if isinstance(weaknesses, list):
                    for weakness in weaknesses:
                        st.markdown(f"- {weakness}")
                else:
                    st.info("No weaknesses data available")
        else:
            st.error(f"Scoring Error: {aggregate.get('error')}")
    
    # TAB 2: Detailed Analysis
    with tab2:
        st.header("Parsed CV Data")
        
        parsed_cv = results.get('parsed_cv', {})
        if 'error' not in parsed_cv:
            # Display in expandable sections
            with st.expander("👤 Personal Information", expanded=True):
                st.json(parsed_cv.get('personal_information', {}))
            
            with st.expander("💼 Work Experience"):
                st.json(parsed_cv.get('work_experience', {}))
            
            with st.expander("🎓 Education"):
                st.json(parsed_cv.get('education', {}))
            
            with st.expander("🛠️ Skills"):
                st.json(parsed_cv.get('skills', {}))
        else:
            st.error(f"Parsing Error: {parsed_cv.get('error')}")
    
    # TAB 3: Skills Deep Dive
    with tab3:
        st.header("Skills Analysis")
        
        skills_analysis = results.get('skills_analysis', {})
        if 'error' not in skills_analysis:
            # Radar chart
            radar_chart = create_skills_chart(skills_analysis)
            if radar_chart:
                st.plotly_chart(radar_chart, use_container_width=True)
            
            # Detailed breakdown
            st.subheader("Detailed Skills Assessment")
            st.json(skills_analysis)
        else:
            st.error(f"Skills Analysis Error: {skills_analysis.get('error')}")
    
    # TAB 4: Experience Review
    with tab4:
        st.header("Experience Evaluation")
        
        experience_eval = results.get('experience_evaluation', {})
        if 'error' not in experience_eval:
            st.json(experience_eval)
            
            # Cultural fit
            st.subheader("Cultural Fit Assessment")
            cultural_fit = results.get('cultural_fit_assessment', {})
            if 'error' not in cultural_fit:
                st.json(cultural_fit)
            else:
                st.error(f"Cultural Fit Error: {cultural_fit.get('error')}")
        else:
            st.error(f"Experience Evaluation Error: {experience_eval.get('error')}")
    
    # TAB 5: Final Recommendation
    with tab5:
        st.header("Hiring Recommendation")
        
        recommendation = results.get('final_recommendation', {})
        if 'error' not in recommendation:
            if isinstance(recommendation, dict):
                for key, value in recommendation.items():
                    st.subheader(key.replace('_', ' ').title())
                    if isinstance(value, list):
                        for item in value:
                            st.markdown(f"- {item}")
                    else:
                        st.write(value)
            else:
                st.write(recommendation)
            
            # Interview focus areas
            if aggregate.get('interview_focus'):
                st.subheader("🎤 Interview Focus Areas")
                for area in aggregate.get('interview_focus', []):
                    st.markdown(f"- {area}")
        else:
            st.error(f"Recommendation Error: {recommendation.get('error')}")
        
        # Export option
        st.divider()
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download JSON Report"):
                json_str = json.dumps(to_json_safe(results), indent=2, ensure_ascii=False)
                st.download_button(
                    label="Download",
                    data=json_str,
                    file_name=f"candidate_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.title("🎯 AI-Powered Recruitment System")
    st.markdown("**Advanced Multi-Agent CV Analysis using LangGraph**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        workflow_type = st.selectbox(
            "Workflow Type",
            ["sequential", "parallel", "conditional"],
            help="Choose the agent execution pattern"
        )
        
        st.divider()
        
        st.header("📄 System Info")
        st.info("""
        **Agents:**
        1. CV Parser
        2. Skills Analyzer
        3. Experience Evaluator
        4. Cultural Fit Assessor
        5. Scoring Agent
        6. Recommendation Agent
        """)
        
        if st.button("🔄 Reset Analysis"):
            st.session_state.workflow_executed = False
            st.session_state.results = None
            st.rerun()
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Upload CV")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose CV file (PDF or DOCX)",
            type=['pdf', 'docx'],
            help="Upload candidate's resume"
        )
        
        # Or paste text
        cv_text_input = st.text_area(
            "Or paste CV text directly",
            height=200,
            placeholder="Paste the candidate's CV here..."
        )
    
    with col2:
        st.header("📝 Job Requirements")
        
        job_requirements = st.text_area(
            "Enter job requirements",
            height=150,
            value="Senior Software Engineer with 5+ years experience in Python, React, AWS. Strong leadership and communication skills required.",
            help="Describe the role requirements"
        )
        
        company_culture = st.text_area(
            "Company Culture",
            height=150,
            value="Fast-paced startup environment. Values innovation, collaboration, and continuous learning. Remote-first culture.",
            help="Describe your company culture"
        )
    
    # Process CV
    if uploaded_file or cv_text_input:
        if uploaded_file:
            # Extract text from file
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Save temporarily
            temp_path = f"temp_cv.{file_extension}"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            if file_extension == 'pdf':
                cv_text = extract_text_from_pdf(temp_path)
            else:
                cv_text = extract_text_from_docx(temp_path)
            
            # Clean up
            os.remove(temp_path)
            
            st.session_state.cv_text = cv_text
        else:
            cv_text = cv_text_input
            st.session_state.cv_text = cv_text
        
        # Display preview
        with st.expander("📄 CV Preview"):
            st.text_area("CV Content", cv_text, height=200, disabled=True)
        
        # Analyze button
        st.divider()
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if not cv_text.strip():
                st.error("Please upload a CV or paste CV text")
            elif not job_requirements.strip():
                st.error("Please enter job requirements")
            else:
                with st.spinner("🔄 Running multi-agent analysis..."):
                    try:
                        # Get workflow
                        workflow = get_workflow(workflow_type)
                        
                        # Prepare initial state
                        initial_state = {
                            "cv_text": cv_text,
                            "job_requirements": job_requirements,
                            "company_culture": company_culture,
                            "messages": [],
                            "current_agent": "",
                            "workflow_status": "initiated",
                            "errors": []
                        }
                        
                        # Execute workflow
                        results = workflow.invoke(initial_state)
                        
                        # Save results
                        st.session_state.results = results
                        st.session_state.workflow_executed = True
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.exception(e)
    
    # Display results if available
    if st.session_state.workflow_executed and st.session_state.results:
        st.divider()
        display_results(st.session_state.results)

if __name__ == "__main__":
    main()