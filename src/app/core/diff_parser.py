from unidiff import PatchSet

def parse_diff(diff_text: str):
	"""Parse a unified diff string into a PatchSet object."""
	return PatchSet(diff_text)
