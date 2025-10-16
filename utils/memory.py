"""
Memory and persistence utilities for the recruitment system
"""
import json
import os
from datetime import datetime
from utils.serialization import to_json_safe
from typing import Dict, Any, List
from pathlib import Path

class RecruitmentMemory:
    """
    Manages persistence and retrieval of candidate assessments
    """
    
    def __init__(self, storage_dir: str = "data/assessments"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_assessment(self, candidate_name: str, assessment_data: Dict[str, Any]) -> str:
        """
        Save candidate assessment to disk
        
        Args:
            candidate_name: Name of the candidate
            assessment_data: Complete assessment results
        
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{candidate_name.replace(' ', '_')}_{timestamp}.json"
        filepath = self.storage_dir / filename
        
        # Add metadata
        assessment_data['metadata'] = {
            'candidate_name': candidate_name,
            'timestamp': timestamp,
            'date': datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(to_json_safe(assessment_data), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def load_assessment(self, filename: str) -> Dict[str, Any]:
        """Load assessment from disk"""
        filepath = self.storage_dir / filename
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_assessments(self) -> List[Dict[str, str]]:
        """List all saved assessments"""
        assessments = []
        
        for file in self.storage_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    metadata = data.get('metadata', {})
                    assessments.append({
                        'filename': file.name,
                        'candidate_name': metadata.get('candidate_name', 'Unknown'),
                        'date': metadata.get('date', 'Unknown'),
                        'score': data.get('aggregate_score', {}).get('overall_score', 0)
                    })
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        return sorted(assessments, key=lambda x: x['date'], reverse=True)
    
    def compare_candidates(self, filenames: List[str]) -> Dict[str, Any]:
        """
        Compare multiple candidates
        
        Args:
            filenames: List of assessment filenames to compare
        
        Returns:
            Comparison data
        """
        candidates = []
        
        for filename in filenames:
            try:
                data = self.load_assessment(filename)
                candidates.append({
                    'name': data.get('metadata', {}).get('candidate_name', 'Unknown'),
                    'overall_score': data.get('aggregate_score', {}).get('overall_score', 0),
                    'skills_score': data.get('skills_analysis', {}).get('skills_match', 0) * 10,
                    'experience_score': data.get('experience_evaluation', {}).get('experience_relevance', 0) * 10,
                    'cultural_fit_score': data.get('cultural_fit_assessment', {}).get('work_style_fit', 0) * 10,
                    'recommendation': data.get('aggregate_score', {}).get('recommendation', 'N/A')
                })
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        return {
            'candidates': candidates,
            'comparison_date': datetime.now().isoformat()
        }
    
    def export_to_csv(self, output_file: str = "assessments_export.csv"):
        """Export all assessments to CSV"""
        import csv
        
        assessments = self.list_assessments()
        
        if not assessments:
            return None
        
        output_path = self.storage_dir / output_file
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['filename', 'candidate_name', 'date', 'score'])
            writer.writeheader()
            writer.writerows(assessments)
        
        return str(output_path)

class ConversationMemory:
    """
    Manages conversation history for context-aware interactions
    """
    
    def __init__(self):
        self.conversations = {}
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add message to conversation history"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_conversation(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieve conversation history"""
        return self.conversations.get(session_id, [])
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history"""
        if session_id in self.conversations:
            del self.conversations[session_id]