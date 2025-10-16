"""
Test suite for recruitment agents
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.workflow import get_workflow

# Sample CV for testing
SAMPLE_CV = """
JOHN DOE
Senior Software Engineer
Email: john.doe@email.com | Phone: +1-555-0123
LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years in full-stack development. 
Specialized in Python, React, and AWS cloud architecture. Led teams of 5-10 engineers.

WORK EXPERIENCE

Senior Software Engineer | Tech Corp | 2020 - Present
- Led development of microservices architecture serving 10M+ users
- Reduced API response time by 40% through optimization
- Mentored 5 junior developers
- Technologies: Python, Django, React, PostgreSQL, AWS, Docker

Software Engineer | StartupXYZ | 2017 - 2020
- Built RESTful APIs for mobile and web applications
- Implemented CI/CD pipelines reducing deployment time by 60%
- Technologies: Node.js, MongoDB, React, Jenkins

Junior Developer | WebSolutions Inc | 2015 - 2017
- Developed responsive web applications
- Technologies: JavaScript, HTML, CSS, PHP

EDUCATION
Bachelor of Science in Computer Science | State University | 2015
GPA: 3.7/4.0

CERTIFICATIONS
- AWS Certified Solutions Architect
- Certified Scrum Master

SKILLS
Technical: Python, JavaScript, React, Node.js, Django, PostgreSQL, MongoDB, 
AWS, Docker, Kubernetes, Git, REST APIs, Microservices
Soft Skills: Leadership, Team Management, Communication, Problem Solving
"""

SAMPLE_JOB_REQUIREMENTS = """
Senior Backend Engineer
Requirements:
- 5+ years of experience in backend development
- Strong proficiency in Python and Django
- Experience with AWS and microservices architecture
- Database expertise (PostgreSQL/MySQL)
- Leadership experience preferred
- Excellent communication skills
"""

SAMPLE_COMPANY_CULTURE = """
Fast-paced tech company with focus on innovation and continuous learning.
We value collaboration, transparency, and work-life balance.
Remote-first culture with flexible hours.
Strong emphasis on mentorship and professional growth.
"""

def test_sequential_workflow():
    """Test sequential workflow execution"""
    print("=" * 50)
    print("Testing Sequential Workflow")
    print("=" * 50)
    
    try:
        workflow = get_workflow("sequential")
        
        initial_state = {
            "cv_text": SAMPLE_CV,
            "job_requirements": SAMPLE_JOB_REQUIREMENTS,
            "company_culture": SAMPLE_COMPANY_CULTURE,
            "messages": [],
            "current_agent": "",
            "workflow_status": "initiated",
            "errors": []
        }
        
        print("\n🚀 Executing workflow...\n")
        results = workflow.invoke(initial_state)
        
        print("\n✅ Workflow completed successfully!")
        print(f"Status: {results.get('workflow_status')}")
        print(f"Errors: {results.get('errors', [])}")
        
        # Display key results
        if results.get('aggregate_score'):
            score = results['aggregate_score']
            print(f"\n📊 Overall Score: {score.get('overall_score', 'N/A')}")
            print(f"Recommendation: {score.get('recommendation', 'N/A')}")
            print(f"Risk Level: {score.get('risk_level', 'N/A')}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_conditional_workflow():
    """Test conditional workflow with early rejection"""
    print("\n" + "=" * 50)
    print("Testing Conditional Workflow")
    print("=" * 50)
    
    # Create a poor-fit CV
    poor_cv = """
    JANE SMITH
    Marketing Manager
    5 years experience in digital marketing, SEO, and content creation.
    Skills: Social Media, Google Analytics, Copywriting, Photoshop
    """
    
    try:
        workflow = get_workflow("conditional")
        
        initial_state = {
            "cv_text": poor_cv,
            "job_requirements": SAMPLE_JOB_REQUIREMENTS,  # Tech role
            "company_culture": SAMPLE_COMPANY_CULTURE,
            "messages": [],
            "current_agent": "",
            "workflow_status": "initiated",
            "errors": []
        }
        
        print("\n🚀 Executing workflow with poor-fit candidate...\n")
        results = workflow.invoke(initial_state)
        
        print("\n✅ Workflow completed!")
        print(f"Status: {results.get('workflow_status')}")
        
        if results.get('final_recommendation'):
            print(f"Decision: {results['final_recommendation']}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("RECRUITMENT SYSTEM TEST SUITE")
    print("=" * 50)
    
    results = {
        "Sequential Workflow": test_sequential_workflow(),
        "Conditional Workflow": test_conditional_workflow()
    }
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return all(results.values())

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)