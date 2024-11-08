# routes/api_routes.py
from fastapi import APIRouter, HTTPException, Header
from models.schemas import RepoInfo, PackageName, DependenciesModel, UpdatesModel, DiffRequest, CommitInfo, PullRequestInfo
from services.github_service import (
    fetch_requirements_from_github,
    commit_changes,
    create_pull_request,
    generate_random_branch_name
)
from services.dependency_service import (
    parse_requirements,
    check_for_updates,
    get_latest_version,
    generate_updated_requirements
)
import cf_aiproxy
import config
import logging
import os
from github import Github, Auth

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GitHub authentication
auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
github_client = Github(config.GITHUB_TOKEN)

@router.get("/repos")
async def list_repos():
    if not auth.token:
        raise HTTPException(status_code=500, detail="GitHub token is not loaded. Please check your .env file.")
    try:
        repos = [repo.name for repo in github_client.get_user().get_repos()]
        return {"repositories": repos}
    except Exception as e:
        logger.error(f"Error listing repositories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parse_requirements")
def api_parse_requirements(req: RepoInfo):
    try:
        requirements_text = fetch_requirements_from_github(req.owner, req.repo_name, req.file_path)
        dependencies = parse_requirements(requirements_text)
        return {"dependencies": dependencies}
    except Exception as e:
        logger.error(f"Error parsing requirements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get_latest_version")
def api_get_latest_version(pkg: PackageName):
    try:
        latest_version = get_latest_version(pkg.package_name)
        if latest_version:
            return {"package_name": pkg.package_name, "latest_version": latest_version}
        else:
            raise HTTPException(status_code=404, detail="Package not found")
    except Exception as e:
        logger.error(f"Error fetching latest version: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_for_updates")
def api_check_for_updates(deps: DependenciesModel):
    try:
        updates = check_for_updates(deps.dependencies)
        return {"updates": updates}
    except Exception as e:
        logger.error(f"Error checking for updates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate_updated_requirements")
def api_generate_updated_requirements(data: UpdatesModel):
    try:
        updated_requirements = generate_updated_requirements(data.dependencies, data.updates)
        return {"updated_requirements": updated_requirements}
    except Exception as e:
        logger.error(f"Error generating updated requirements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/commit_changes")
def api_commit_changes(info: CommitInfo, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    try:
        token = authorization.split(" ")[1]
        g = Github(token)
        repo = g.get_repo(f"{info.owner}/{info.repo_name}")
        commit_changes(repo, info.branch_name, info.file_path, info.updated_content, info.original_sha)
        return {"message": "Changes committed successfully"}
    except Exception as e:
        logger.error(f"Error committing changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create_pull_request")
def api_create_pull_request(pr_info: PullRequestInfo, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    try:
        token = authorization.split(" ")[1]
        g = Github(token)
        repo = g.get_repo(f"{pr_info.owner}/{pr_info.repo_name}")
        pr = create_pull_request(repo, pr_info.branch_name)
        return {"message": "Pull request created", "pull_request_url": pr.html_url}
    except Exception as e:
        logger.error(f"Error creating pull request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run_all")
def run_all_actions(repo_info: RepoInfo):
    try:
        user = github_client.get_user()
        repos = [repo.name for repo in user.get_repos()]

        requirements_text = fetch_requirements_from_github(repo_info.owner, repo_info.repo_name)
        dependencies = parse_requirements(requirements_text)

        updates = check_for_updates(dependencies)
        updated_content = generate_updated_requirements(dependencies, updates)

        repo = github_client.get_repo(f"{repo_info.owner}/{repo_info.repo_name}")
        branch_name = generate_random_branch_name()
        
        create_or_get_branch(repo, branch_name)

        file = repo.get_contents("requirements.txt", ref="main")
        repo.update_file("requirements.txt", "Update dependencies", updated_content, file.sha, branch=branch_name)

        pr = repo.create_pull(title="Update dependencies", body="Automated update of dependencies", head=branch_name, base="main")

        diff_summary = get_diff_summary(DiffRequest(original_requirements=requirements_text, updated_requirements=updated_content)).get("summary", "No summary available.")

        return {
            "repositories": repos,
            "parsed_dependencies": dependencies,
            "updates": updates,
            "updated_requirements": updated_content,
            "diff_summary": diff_summary,
            "pr_link": pr.html_url
        }
    except Exception as e:
        logger.error(f"Error running all actions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def create_or_get_branch(repo, branch_name):
    try:
        repo.get_branch(branch_name)
    except Exception:
        source_branch = repo.get_branch("main")
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
        logger.info(f"Created new branch {branch_name}")

@router.post("/diff_summary")
def get_diff_summary(diff_request: DiffRequest):
    try:
        system_message = "You are a software developer reviewing changes to a project's dependencies."
        prompt = f"""
        Compare the following two sets of requirements and provide a summary of the differences:

        Original Requirements:
        {diff_request.original_requirements}

        Updated Requirements:
        {diff_request.updated_requirements}

        Summary:
        """
        
        openai_summary = cf_aiproxy.send_ai_proxy_request(config.config_openai, system_message, prompt)
        groq_summary = cf_aiproxy.send_ai_proxy_request(config.config_groq, system_message, prompt)
        
        combined_summary = f"### OpenAI Summary:\n{openai_summary}\n\n### Groq Summary:\n{groq_summary}"
        return {"summary": combined_summary}
    except Exception as e:
        logger.error(f"Failed to generate diff summary: {e}")
        return {"summary": "Failed to generate summary due to an error."}
