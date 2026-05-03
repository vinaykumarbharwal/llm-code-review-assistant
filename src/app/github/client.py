from github import Github

def get_github_client(token: str):
	return Github(token)
