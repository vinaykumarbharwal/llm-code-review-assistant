import json
from typing import Any

def parse_llm_response(response: str) -> Any:
	"""Parse the LLM's JSON response string into a Python object."""
	return json.loads(response)
