import os
import asyncio
from typing import List, Dict

GROQ_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4.5")

# LangChain integration
try:
    from langchain_groq import ChatGroq
    from langchain_anthropic import ChatAnthropic
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

class LLMClient:
    def __init__(self, provider: str = None, api_key: str = None, model: str = None):
        self.provider = (provider or LLM_PROVIDER).lower()
        self.api_key = api_key
        self.model = model
        self.context_window: List[Dict[str, str]] = []
        self.max_context_messages = 20

    def get_chat_model(self):
        """Get LangChain-compatible chat model for agent execution"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not installed. Run: pip install langchain-groq langchain-anthropic")
        
        provider = self.provider
        if provider == "groq":
            key = self.api_key or GROQ_KEY
            model = self.model or GROQ_MODEL
            return ChatGroq(api_key=key, model=model, temperature=0.7)
        elif provider in ["anthropic", "claude"]:
            key = self.api_key or ANTHROPIC_KEY
            model = self.model or ANTHROPIC_MODEL
            return ChatAnthropic(api_key=key, model=model, temperature=0.7)
        else:
            # Fallback to Groq
            key = GROQ_KEY
            model = GROQ_MODEL
            return ChatGroq(api_key=key, model=model, temperature=0.7)

    def add_to_context(self, role: str, content: str):
        self.context_window.append({"role": role, "content": content})
        if len(self.context_window) > self.max_context_messages:
            self.context_window = self.context_window[-self.max_context_messages:]

    def get_context(self) -> List[Dict[str, str]]:
        return self.context_window.copy()

    def clear_context(self):
        self.context_window = []

    async def generate(self, prompt: str, add_to_context: bool = True) -> str:
        if add_to_context:
            self.add_to_context("user", prompt)
        provider = self.provider
        response_text = ""
        if provider == "groq":
            key = self.api_key or GROQ_KEY
            model = self.model or GROQ_MODEL
            if key:
                import httpx
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                messages = self.context_window.copy() if self.context_window else []
                if not messages or messages[-1]["content"] != prompt:
                    messages.append({"role": "user", "content": prompt})
                
                # Truncate messages to prevent 413 Payload Too Large
                max_chars_per_message = 3000  # Limit each message to 3000 chars
                truncated_messages = []
                for msg in messages:
                    content = msg.get("content", "")
                    if len(content) > max_chars_per_message:
                        content = content[:max_chars_per_message] + "\n\n[... content truncated due to size ...]"
                    truncated_messages.append({"role": msg["role"], "content": content})
                
                # Keep only last 10 messages to reduce payload size
                if len(truncated_messages) > 10:
                    truncated_messages = truncated_messages[-10:]
                
                payload = {"model": model, "messages": truncated_messages, "max_tokens": 800, "temperature": 0.7}
                try:
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        r = await client.post(url, json=payload, headers=headers)
                        r.raise_for_status()
                        j = r.json()
                        response_text = j.get("choices", [{}])[0].get("message", {}).get("content", "")
                        if not response_text:
                            response_text = "[groq-empty-response]"
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 413:
                        # Payload too large - try with even smaller context
                        truncated_messages = truncated_messages[-3:]  # Keep only last 3 messages
                        for i, msg in enumerate(truncated_messages):
                            truncated_messages[i]["content"] = msg["content"][:1500]
                        payload["messages"] = truncated_messages
                        payload["max_tokens"] = 500
                        try:
                            async with httpx.AsyncClient(timeout=60.0) as client:
                                r = await client.post(url, json=payload, headers=headers)
                                r.raise_for_status()
                                j = r.json()
                                response_text = j.get("choices", [{}])[0].get("message", {}).get("content", "")
                        except Exception:
                            response_text = f"Analysis: Based on the available information, I'll provide a summary. {prompt[:500]}"
                    else:
                        response_text = f"AI service returned error {e.response.status_code}. Using simplified response."
                except httpx.ConnectError as e:
                    response_text = f"I'm having trouble connecting to the AI service. Using fallback response: I understand you said '{prompt[:100]}'. However, I'm currently unable to connect to my AI backend. Please check your internet connection or API configuration."
                except Exception as e:
                    response_text = f"Error connecting to AI: {str(e)[:100]}. I can still help with basic responses, but advanced AI features are temporarily unavailable."
            else:
                await asyncio.sleep(0.01)
                response_text = f"[mock-groq] response for: {prompt[:200]}"
        elif provider == "anthropic" or provider.startswith("claude"):
            key = self.api_key or ANTHROPIC_KEY
            model = self.model or ANTHROPIC_MODEL
            if key:
                import httpx
                url = "https://api.anthropic.com/v1/messages"
                headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
                messages = []
                for msg in self.context_window:
                    if msg["role"] in ["user", "assistant"]:
                        messages.append(msg)
                if not messages or messages[-1]["content"] != prompt:
                    messages.append({"role": "user", "content": prompt})
                payload = {"model": model, "messages": messages, "max_tokens": 1024}
                try:
                    async with httpx.AsyncClient(timeout=60.0) as client:
                        r = await client.post(url, json=payload, headers=headers)
                        r.raise_for_status()
                        j = r.json()
                        response_text = j.get("content", [{}])[0].get("text", "")
                        if not response_text:
                            response_text = "[anthropic-empty-response]"
                except Exception as e:
                    response_text = f"[anthropic-error: {str(e)[:100]}]"
            else:
                await asyncio.sleep(0.01)
                response_text = f"[mock-anthropic] response for: {prompt[:200]}"
        else:
            await asyncio.sleep(0.01)
            response_text = f"[mock-llm-{provider}] response for: {prompt[:200]}"
        if add_to_context and response_text:
            self.add_to_context("assistant", response_text)
        return response_text
