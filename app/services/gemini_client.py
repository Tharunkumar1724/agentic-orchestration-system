"""
Gemini API Client for Knowledge-Aided Generation (KAG)
Handles fact extraction, reasoning, and summarization
"""
import os
import re
import json
import requests
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"


class GeminiRequest(BaseModel):
    """Request model for Gemini API"""
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 2048


class GeminiResponse(BaseModel):
    """Response model from Gemini API"""
    summary: str = Field(description="Concise summary of the workflow output")
    facts: List[str] = Field(description="List of key facts extracted from the output")
    reasoning: str = Field(description="Analysis and insights about the output")
    raw_response: Optional[str] = None


class GeminiClient:
    """Client for interacting with Gemini 1.5 Flash API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
    
    def generate(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate content using Gemini 1.5 Flash
        
        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            
        Returns:
            Dict containing the response
        """
        url = f"{GEMINI_API_URL}?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": temperature,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract text from Gemini response structure
            if "candidates" in data and len(data["candidates"]) > 0:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    text = candidate["content"]["parts"][0].get("text", "")
                    return {
                        "text": text,
                        "raw": data
                    }
            
            return {
                "text": "",
                "raw": data,
                "error": "No valid response generated"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "text": "",
                "error": str(e),
                "raw": None
            }
    
    def extract_facts(self, workflow_output: str, context: str = "") -> GeminiResponse:
        """
        Extract key facts and insights from workflow output
        
        Args:
            workflow_output: The output from a workflow execution
            context: Optional context about the workflow
            
        Returns:
            GeminiResponse with summary, facts, and reasoning
        """
        prompt = f"""Analyze the following workflow output and extract key information.

Context: {context if context else "General workflow analysis"}

Workflow Output:
{workflow_output}

Please provide:
1. A concise summary (2-3 sentences)
2. Key facts extracted (list 3-5 important facts)
3. Reasoning and insights (brief analysis)

Format your response as JSON with these exact keys:
{{
  "summary": "...",
  "facts": ["fact1", "fact2", ...],
  "reasoning": "..."
}}
"""
        
        result = self.generate(prompt, temperature=0.3)
        
        if "error" in result:
            return GeminiResponse(
                summary="Error extracting facts",
                facts=[],
                reasoning=f"Error: {result['error']}",
                raw_response=str(result.get("raw"))
            )
        
        try:
            # Try to parse JSON from response
            text = result["text"].strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in text:
                json_start = text.find("```json") + 7
                json_end = text.find("```", json_start)
                text = text[json_start:json_end].strip()
            elif "```" in text:
                json_start = text.find("```") + 3
                json_end = text.find("```", json_start)
                text = text[json_start:json_end].strip()
            
            parsed = json.loads(text)
            
            return GeminiResponse(
                summary=parsed.get("summary", ""),
                facts=parsed.get("facts", []),
                reasoning=parsed.get("reasoning", ""),
                raw_response=result["text"]
            )
            
        except json.JSONDecodeError:
            # Fallback: parse text manually
            lines = result["text"].split("\n")
            summary = ""
            facts = []
            reasoning = ""
            
            current_section = None
            for line in lines:
                line = line.strip()
                if "summary" in line.lower() and ":" in line:
                    current_section = "summary"
                    summary = line.split(":", 1)[1].strip()
                elif "fact" in line.lower() and (":" in line or "-" in line):
                    current_section = "facts"
                    fact = line.split(":", 1)[-1].strip() if ":" in line else line.lstrip("- ").strip()
                    if fact and not "fact" in fact.lower():
                        facts.append(fact)
                elif "reasoning" in line.lower() and ":" in line:
                    current_section = "reasoning"
                    reasoning = line.split(":", 1)[1].strip()
                elif current_section == "summary" and line:
                    summary += " " + line
                elif current_section == "facts" and (line.startswith("-") or line.startswith("•")):
                    facts.append(line.lstrip("-•").strip())
                elif current_section == "reasoning" and line:
                    reasoning += " " + line
            
            return GeminiResponse(
                summary=summary or "Analysis completed",
                facts=facts or ["No specific facts extracted"],
                reasoning=reasoning or "No detailed reasoning available",
                raw_response=result["text"]
            )
    
    def summarize_conversation(self, messages: List[Dict[str, str]], workflow_context: str = "") -> str:
        """
        Create a conversation summary from workflow interactions
        
        Args:
            messages: List of messages with 'role' and 'content'
            workflow_context: Context about the workflow
            
        Returns:
            Summary string
        """
        conversation_text = "\n".join([
            f"{msg.get('role', 'system')}: {msg.get('content', '')}"
            for msg in messages
        ])
        
        prompt = f"""Summarize the following workflow conversation into a concise memory that captures the key information and decisions.

Workflow Context: {workflow_context}

Conversation:
{conversation_text}

Provide a brief summary (3-6 sentences) that could be used as context for subsequent workflows."""
        
        result = self.generate(prompt, temperature=0.5)
        return result.get("text", "No summary available")
    
    def reason_about_handoff(self, 
                            source_workflow_summary: str,
                            source_facts: List[str],
                            target_workflow_description: str) -> Dict[str, Any]:
        """
        Generate reasoning about how to hand off information between workflows
        
        Args:
            source_workflow_summary: Summary from source workflow
            source_facts: Key facts from source workflow
            target_workflow_description: Description of target workflow
            
        Returns:
            Dict with handoff instructions and context
        """
        facts_text = "\n".join([f"- {fact}" for fact in source_facts])
        
        prompt = f"""You are orchestrating communication between two workflows.

Source Workflow Summary:
{source_workflow_summary}

Key Facts from Source:
{facts_text}

Target Workflow Description:
{target_workflow_description}

Based on the source workflow's output, provide:
1. What information should be passed to the target workflow
2. How this information relates to the target workflow's task
3. Any important context or constraints

Respond with valid JSON in this exact format:
{{
    "handoff_data": "Information to pass to the target workflow",
    "relevance": "How this information relates to the target task",
    "context": "Important context or constraints"
}}"""
        
        result = self.generate(prompt, temperature=0.7)
        text = result.get("text", "{}")
        
        # Try to extract JSON from the response
        try:
            # First try direct JSON parsing
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON in markdown code blocks
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Fallback
            return {
                "handoff_data": source_workflow_summary,
                "relevance": "General context from previous workflow",
                "context": f"Error generating detailed handoff: {text[:200]}"
            }


# Global instance
_gemini_client = None

def get_gemini_client() -> GeminiClient:
    """Get or create the global Gemini client instance"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
