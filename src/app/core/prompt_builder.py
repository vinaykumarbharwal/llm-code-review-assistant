def build_review_prompt(diff_chunk: str, guidelines: str = "") -> str:
	"""Builds a prompt for the LLM to review a diff chunk, optionally with guidelines."""
	prompt = "You are an expert code reviewer. Review the following diff and provide structured feedback."
	if guidelines:
		prompt += f"\n\nTeam Guidelines:\n{guidelines}"
	prompt += f"\n\nDiff:\n{diff_chunk}"
	prompt += "\n\nReturn JSON with file, line_start, line_end, severity, category, message, suggested_fix."
	return prompt
