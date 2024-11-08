# services/dependency_service.py
from packaging import version
from typing import Optional, Dict
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_requirements(requirements_text: str) -> Dict[str, Optional[str]]:
    """Parse a requirements.txt format text to extract packages and their versions."""
    dependencies = {}
    for line in requirements_text.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            package, package_version = parse_dependency_line(line)
            dependencies[package] = package_version
    return dependencies

def parse_dependency_line(line: str) -> (str, Optional[str]):
    """Parse an individual line in requirements format and return the package and version."""
    if "==" in line:
        package, package_version = line.split("==")
        return package.strip(), package_version.strip()
    else:
        return line, None

def get_latest_version(package_name: str) -> Optional[str]:
    """Retrieve the latest version of a package from PyPI."""
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    if response.ok:
        return response.json().get("info", {}).get("version")
    logger.error(f"Failed to fetch version for {package_name}")
    return None

def check_for_updates(dependencies: Dict[str, Optional[str]]) -> Dict[str, Dict[str, Optional[str]]]:
    """Check each dependency for updates and return those with newer versions available."""
    updates = {}
    for package, current_version in dependencies.items():
        latest_version = get_latest_version(package)
        if is_update_available(current_version, latest_version):
            updates[package] = {
                "current": current_version,
                "latest": latest_version
            }
    return updates

def is_update_available(current_version: Optional[str], latest_version: Optional[str]) -> bool:
    """Determine if an update is available by comparing current and latest versions."""
    return latest_version and (not current_version or version.parse(latest_version) > version.parse(current_version))

def generate_updated_requirements(dependencies: Dict[str, Optional[str]], updates: Dict[str, Dict[str, Optional[str]]]) -> str:
    """Generate an updated requirements text with available package updates."""
    updated_lines = [
        f"{package}=={updates[package]['latest']}" if package in updates else f"{package}=={current_version}" if current_version else package
        for package, current_version in dependencies.items()
    ]
    return "\n".join(updated_lines)
