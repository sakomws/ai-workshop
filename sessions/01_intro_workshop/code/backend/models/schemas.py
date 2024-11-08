from pydantic import BaseModel
from typing import Optional, Dict

# Define the Pydantic model for the request body
class RepoInfo(BaseModel):
    owner: str
    repo_name: str
    file_path: Optional[str] = "requirements.txt"

# Pydantic models for request bodies
class RequirementsText(BaseModel):
    requirements_text: str

class PackageName(BaseModel):
    package_name: str

class DependenciesModel(BaseModel):
    dependencies: dict

class UpdatesModel(BaseModel):
    dependencies: dict
    updates: dict

class CommitInfo(BaseModel):
    owner: str
    repo_name: str
    branch_name: str
    file_path: str
    updated_content: str
    original_sha: str

class PullRequestInfo(BaseModel):
    owner: str
    repo_name: str
    branch_name: str

class DiffRequest(BaseModel):
    original_requirements: str
    updated_requirements: str
