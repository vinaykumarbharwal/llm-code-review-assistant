import os
from src.app.config import Settings

settings = Settings()

def call_llm(prompt: str, model: str = None) -> str:
	"""Dummy LLM call. Replace with real Groq API call."""
	# In production, use the Groq API SDK
	return '{"comments": [], "summary": "No issues found."}'
