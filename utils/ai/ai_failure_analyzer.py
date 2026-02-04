"""
AI-Powered Test Failure Analyzer using Ollama
Analyzes test failures and provides intelligent root cause analysis
"""
import json
import requests
from datetime import datetime
from typing import Dict, Optional
import traceback


class AIFailureAnalyzer:
    """Analyzes test failures using local Ollama AI"""
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        """
        Initialize AI analyzer
        
        Args:
            ollama_host: Ollama API endpoint (default: local)
        """
        self.ollama_host = ollama_host
        self.model = "tinyllama"
        
    def analyze_failure(
        self,
        test_name: str,
        error_message: str,
        error_type: str,
        traceback_text: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Analyze a test failure and provide intelligent insights
        
        Args:
            test_name: Name of the failed test
            error_message: Error message from the failure
            error_type: Type of exception
            traceback_text: Full traceback (optional)
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Build analysis prompt
            prompt = self._build_analysis_prompt(
                test_name, error_message, error_type, traceback_text
            )
            
            # Call Ollama API
            analysis = self._call_ollama(prompt)
            
            return {
                "status": "success",
                "test_name": test_name,
                "error_type": error_type,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "analyzer": "Ollama AI (tinyllama)"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "test_name": test_name,
                "error_type": error_type,
                "analysis": f"AI analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "analyzer": "Ollama AI (error)"
            }
    
    def _build_analysis_prompt(
        self,
        test_name: str,
        error_message: str,
        error_type: str,
        traceback_text: Optional[str]
    ) -> str:
        """Build prompt for AI analysis"""
        prompt = f"""Analyze this test automation failure and provide:
1. Root cause (most likely reason for failure)
2. Suggested fix (specific action to resolve)
3. Confidence level (high/medium/low)

Test: {test_name}
Error Type: {error_type}
Error Message: {error_message}"""
        
        if traceback_text:
            # Include only last 3 lines of traceback to keep prompt short
            tb_lines = traceback_text.strip().split('\n')
            relevant_tb = '\n'.join(tb_lines[-3:])
            prompt += f"\nTraceback (last 3 lines):\n{relevant_tb}"
        
        prompt += "\n\nProvide analysis in this format:\nRoot Cause: <cause>\nSuggested Fix: <fix>\nConfidence: <level>"
        
        return prompt
    
    def _call_ollama(self, prompt: str, timeout: int = 30) -> str:
        """
        Call Ollama API for analysis
        
        Args:
            prompt: Analysis prompt
            timeout: Request timeout in seconds
            
        Returns:
            AI analysis text
        """
        url = f"{self.ollama_host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more focused analysis
                "num_predict": 300   # Limit response length
            }
        }
        
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "No analysis generated")
    
    def format_analysis_for_report(self, analysis_result: Dict[str, str]) -> str:
        """
        Format analysis result for HTML report
        
        Args:
            analysis_result: Analysis dictionary
            
        Returns:
            Formatted HTML string
        """
        if analysis_result["status"] == "error":
            return f"""
            <div class="ai-analysis-error">
                <h4>🤖 AI Analysis Failed</h4>
                <p>{analysis_result["analysis"]}</p>
            </div>
            """
        
        return f"""
        <div class="ai-analysis">
            <h4>🤖 AI-Powered Failure Analysis</h4>
            <p><strong>Test:</strong> {analysis_result["test_name"]}</p>
            <p><strong>Error Type:</strong> {analysis_result["error_type"]}</p>
            <div class="analysis-content">
                {self._format_analysis_text(analysis_result["analysis"])}
            </div>
            <p class="analysis-meta">
                <em>Analyzed by {analysis_result["analyzer"]} at {analysis_result["timestamp"]}</em>
            </p>
        </div>
        """
    
    def _format_analysis_text(self, analysis: str) -> str:
        """Format analysis text with proper HTML"""
        lines = analysis.strip().split('\n')
        formatted = []
        
        for line in lines:
            if line.startswith("Root Cause:"):
                formatted.append(f"<p><strong>🔍 {line}</strong></p>")
            elif line.startswith("Suggested Fix:"):
                formatted.append(f"<p><strong>🔧 {line}</strong></p>")
            elif line.startswith("Confidence:"):
                formatted.append(f"<p><strong>📊 {line}</strong></p>")
            elif line.strip():
                formatted.append(f"<p>{line}</p>")
        
        return '\n'.join(formatted)


# Convenience function for quick analysis
def analyze_test_failure(
    test_name: str,
    error_message: str,
    error_type: str = "Exception",
    traceback_text: Optional[str] = None,
    ollama_host: str = "http://localhost:11434"
) -> Dict[str, str]:
    """
    Quick function to analyze a test failure
    
    Args:
        test_name: Name of failed test
        error_message: Error message
        error_type: Type of exception
        traceback_text: Full traceback (optional)
        ollama_host: Ollama API endpoint
        
    Returns:
        Analysis results dictionary
    """
    analyzer = AIFailureAnalyzer(ollama_host=ollama_host)
    return analyzer.analyze_failure(test_name, error_message, error_type, traceback_text)
