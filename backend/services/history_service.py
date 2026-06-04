"""History & Caching Service - Store and retrieve analysis and generation results."""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path


class HistoryService:
    """Manage history of analyses and generated code."""

    def __init__(self, base_path: str = "data/history"):
        """Initialize history service.
        
        Args:
            base_path: Directory to store history files
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.analyses_file = self.base_path / "analyses.jsonl"
        self.generations_file = self.base_path / "generations.jsonl"

    def save_analysis(self, source_url: str, analysis: Dict[str, Any]) -> str:
        """Save analysis result to history.
        
        Args:
            source_url: URL or file name that was analyzed
            analysis: Analysis result containing endpoints, auth, format, security
            
        Returns:
            Analysis ID
        """
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = {
            "id": analysis_id,
            "timestamp": datetime.now().isoformat(),
            "source": source_url,
            "endpoints_count": len(analysis.get("endpoints", [])),
            "auth_method": analysis.get("auth_method"),
            "response_format": analysis.get("response_format"),
            "analysis": analysis
        }
        
        with open(self.analyses_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        return analysis_id

    def save_generation(self, analysis_id: str, language: str, code: str, api_name: str = "API") -> str:
        """Save generated code to history.
        
        Args:
            analysis_id: ID of the analysis this code was generated from
            language: Programming language
            code: Generated SDK code
            api_name: Name of the API
            
        Returns:
            Generation ID
        """
        generation_id = f"gen_{language}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        record = {
            "id": generation_id,
            "timestamp": datetime.now().isoformat(),
            "analysis_id": analysis_id,
            "language": language,
            "api_name": api_name,
            "code_length": len(code),
            "code": code
        }
        
        with open(self.generations_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
        
        return generation_id

    def get_analysis_history(self, limit: int = 20) -> List[Dict]:
        """Get recent analysis history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of analysis records
        """
        if not self.analyses_file.exists():
            return []
        
        records = []
        with open(self.analyses_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                if line.strip():
                    records.append(json.loads(line))
        
        return list(reversed(records))  # Newest first

    def get_generation_history(self, limit: int = 20) -> List[Dict]:
        """Get recent generation history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of generation records (code removed for list view)
        """
        if not self.generations_file.exists():
            return []
        
        records = []
        with open(self.generations_file, 'r') as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                if line.strip():
                    record = json.loads(line)
                    # Remove full code from list view
                    record['code'] = record['code'][:200] + '...' if len(record['code']) > 200 else record['code']
                    records.append(record)
        
        return list(reversed(records))  # Newest first

    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict]:
        """Get specific analysis by ID.
        
        Args:
            analysis_id: Analysis ID to retrieve
            
        Returns:
            Analysis record or None
        """
        if not self.analyses_file.exists():
            return None
        
        with open(self.analyses_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['id'] == analysis_id:
                    return record
        
        return None

    def get_generation_by_id(self, generation_id: str) -> Optional[Dict]:
        """Get specific generation by ID.
        
        Args:
            generation_id: Generation ID to retrieve
            
        Returns:
            Generation record or None
        """
        if not self.generations_file.exists():
            return None
        
        with open(self.generations_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['id'] == generation_id:
                    return record
        
        return None

    def get_related_generations(self, analysis_id: str) -> List[Dict]:
        """Get all generations related to an analysis.
        
        Args:
            analysis_id: Analysis ID to find generations for
            
        Returns:
            List of generation records
        """
        if not self.generations_file.exists():
            return []
        
        records = []
        with open(self.generations_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['analysis_id'] == analysis_id:
                    # Remove full code from list view
                    record['code'] = record['code'][:200] + '...' if len(record['code']) > 200 else record['code']
                    records.append(record)
        
        return list(reversed(records))  # Newest first

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about history.
        
        Returns:
            Dictionary with statistics
        """
        analyses = self.get_analysis_history(limit=1000)
        generations = self.get_generation_history(limit=1000)
        
        language_counts = {}
        for gen in generations:
            lang = gen['language']
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        auth_methods = {}
        for analysis in analyses:
            auth = analysis.get('auth_method', 'None')
            auth_methods[auth] = auth_methods.get(auth, 0) + 1
        
        return {
            "total_analyses": len(analyses),
            "total_generations": len(generations),
            "languages_used": language_counts,
            "auth_methods_detected": auth_methods,
            "avg_endpoints_per_analysis": sum(a['endpoints_count'] for a in analyses) / len(analyses) if analyses else 0,
        }

    def clear_history(self) -> bool:
        """Clear all history (use with caution).
        
        Returns:
            True if cleared successfully
        """
        try:
            if self.analyses_file.exists():
                self.analyses_file.unlink()
            if self.generations_file.exists():
                self.generations_file.unlink()
            return True
        except Exception:
            return False
