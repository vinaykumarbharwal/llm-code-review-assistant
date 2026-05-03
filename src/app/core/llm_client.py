import json
import os
from typing import Optional

import httpx

from src.app.config import Settings

settings = Settings()


def _candidate_models(requested_model: str) -> list[str]:
	# Map older Groq model aliases to currently supported names and keep fallbacks.
	alias_map = {
		"llama3-70b-8192": "llama-3.3-70b-versatile",
		"llama3-8b-8192": "llama-3.1-8b-instant",
	}
	primary = alias_map.get(requested_model, requested_model)
	fallbacks = [
		primary,
		"llama-3.3-70b-versatile",
		"llama-3.1-8b-instant",
	]
	# Deduplicate while preserving order
	seen = set()
	ordered = []
	for model in fallbacks:
		if model not in seen:
			seen.add(model)
			ordered.append(model)
	return ordered


def call_llm(prompt: str, model: Optional[str] = None, max_output_tokens: int = 512) -> str:
	"""Call Groq generative API and return the text output.

	Falls back to a small JSON stub when `GROQ_API_KEY` is not configured.

	Returns:
		str: LLM textual response (usually JSON string the rest of the app will parse).
	"""
	requested_model = model or settings.llm_model

	# Allow forcing a stub via env for offline/dev runs
	force_stub = os.getenv("FORCE_STUB_LLM", "false").lower() in ("1", "true", "yes")
	api_key = settings.groq_api_key
	if force_stub or not api_key:
		# Graceful fallback for local dev when key is not set or stub forced
		return json.dumps({"comments": [], "summary": "Groq call skipped (stubbed response)."})

	# Groq uses an OpenAI-compatible chat completions API.
	url = "https://api.groq.com/openai/v1/chat/completions"
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json",
	}
	base_messages = [
		{
			"role": "system",
			"content": "You are a strict code reviewer. Return concise, useful output.",
		},
		{"role": "user", "content": prompt},
	]

	try:
		with httpx.Client(timeout=30.0) as client:
			last_error: Optional[str] = None
			for candidate_model in _candidate_models(requested_model):
				payload = {
					"model": candidate_model,
					"temperature": 0,
					"max_tokens": max_output_tokens,
					"messages": base_messages,
				}
				resp = client.post(url, headers=headers, json=payload)
				if resp.status_code >= 400:
					# Keep Groq details for diagnostics and continue trying fallback models.
					body = resp.text
					try:
						err_json = resp.json()
						body = json.dumps(err_json)
					except Exception:
						pass
					last_error = f"model={candidate_model}, status={resp.status_code}, body={body}"
					continue

				data = resp.json()

				# Primary shape for OpenAI-compatible responses.
				if isinstance(data, dict):
					choices = data.get("choices")
					if isinstance(choices, list) and choices:
						message = choices[0].get("message", {})
						content = message.get("content")
						if content is not None:
							return str(content)

				# Backward-compatible fallbacks for alternate response shapes.
				if isinstance(data, dict):
					out = None
					if "output" in data and isinstance(data["output"], list) and data["output"]:
						first = data["output"][0]
						out = first.get("content") or first.get("text")
					if out is None:
						out = data.get("generated_text") or data.get("text")

					if out is not None:
						if isinstance(out, (dict, list)):
							return json.dumps(out)
						return str(out)

				# If this model succeeded but shape was unexpected, return raw text.
				return resp.text

			return json.dumps({
				"error": "LLM request failed for all candidate models",
				"detail": last_error or "Unknown error",
			})
	except httpx.HTTPError as e:
		# Surface a helpful error string for debugging
		return json.dumps({"error": f"LLM request failed: {str(e)}"})
