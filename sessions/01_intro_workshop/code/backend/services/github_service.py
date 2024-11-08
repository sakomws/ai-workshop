from github import Github, Auth
from fastapi import HTTPException
import config
import logging
import random
import string
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create authentication and GitHub client
auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
github_client = Github(config.GITHUB_TOKEN)

def fetch_requirements_from_github(owner: str, repo_name: str, file_path: str = "requirements.txt"):
    """Fetch the content of a requirements file from a GitHub repository."""
    try:
        repo = github_client.get_repo(f"{owner}/{repo_name}")
        file_content = repo.get_contents(file_path).decoded_content.decode("utf-8")
        return file_content
    except Exception as e:
        handle_github_error(e, file_path)

def handle_github_error(error, file_path):
    """Handle GitHub errors with appropriate logging and HTTP responses."""
    if "404" in str(error):
        logger.error(f"Failed to fetch file from GitHub: {error}. File path '{file_path}' might be incorrect.")
        raise HTTPException(status_code=404, detail="404: Could not find the specified file in the repository. Please check the file path.")
    else:
        logger.error(f"Error accessing GitHub repository: {error}")
        raise HTTPException(status_code=500, detail="Error accessing the repository or fetching file.")

def commit_changes(repo, branch_name, file_path, updated_content, original_sha):
    """Commit changes to a specified file on a new branch in the repository."""
    create_branch(repo, branch_name)
    repo.update_file(
        path=file_path,
        message="Update dependencies",
        content=updated_content,
        sha=original_sha,
        branch=branch_name
    )
    logger.info(f"Committed changes to {file_path} on branch {branch_name}")

def create_branch(repo, branch_name):
    """Create a new branch from the repository's default branch."""
    base = repo.get_branch(repo.default_branch)
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base.commit.sha)
    logger.info(f"Created new branch {branch_name}")

def create_pull_request(repo, branch_name):
    """Create a pull request from a specified branch to the repository's default branch."""
    pr = repo.create_pull(
        title="Update dependencies to latest versions",
        body="This PR updates the dependencies to their latest versions.",
        head=branch_name,
        base=repo.default_branch
    )
    logger.info(f"Created pull request {pr.html_url}")
    return pr

def generate_random_branch_name(prefix="update-dependencies-"):
    """Generate a random branch name with the given prefix."""
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}{random_id}"
