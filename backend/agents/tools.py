from langchain_core.tools import tool
from backend.services.github import GitHubService
import asyncio

github = GitHubService()

@tool
async def search_repos(query: str, language: str = None, min_stars: int = 0):
    """Search for public GitHub repositories based on query, language, and minimum stars."""
    return await github.search_repositories(query, language, min_stars)

@tool
async def analyze_repo_structure(repo_full_name: str):
    """Fetch the full file tree of a repository to understand its complete structure and architecture."""
    tree = await github.get_file_tree(repo_full_name)
    # Filter for interesting structural files
    priority_files = [item["path"] for item in tree if any(p in item["path"].lower() for p in ["readme", "package.json", "requirements.txt", "main.py", "app.py", "index.ts", "cargo.toml", "dockerfile", "docker-compose.yml", "go.mod"])]
    
    # We return up to 1000 paths so the LLM knows the full file system exists and can choose what to read
    return {
        "tree_summary": [item["path"] for item in tree[:1000]], 
        "key_files": priority_files[:20],
        "total_files": len(tree)
    }

@tool
async def read_github_file(repo_full_name: str, path: str):
    """Read the content of a specific file from a GitHub repository."""
    return await github.fetch_file_content(repo_full_name, path)

@tool
async def get_repo_issues_intelligence(repo_full_name: str):
    """Fetch recent issues and PRs to analyze maintenance quality and community demand."""
    items = await github.get_issues_and_prs(repo_full_name)
    summary = []
    for item in items[:15]:
        summary.append({
            "title": item.get("title"),
            "state": item.get("state"),
            "is_pr": "pull_request" in item,
            "created_at": item.get("created_at")
        })
    return summary

@tool
async def get_repo_community_health(repo_full_name: str):
    """Fetch community health metrics like license, contributing guidelines, and health percentage."""
    profile = await github.get_community_profile(repo_full_name)
    languages = await github.get_languages(repo_full_name)
    
    return {
        "health_percentage": profile.get("health_percentage", 0),
        "has_contributing": "contributing" in profile.get("files", {}),
        "has_license": "license" in profile.get("files", {}),
        "has_code_of_conduct": "code_of_conduct" in profile.get("files", {}),
        "languages": languages
    }

@tool
async def get_repo_trends_and_risks(repo_full_name: str):
    """Fetch commit history and metadata to assess repository health, activity, and risks."""
    commits = await github.get_commits(repo_full_name)
    repo = await github.get_repo_details(repo_full_name)
    
    return {
        "recent_commits_count": len(commits),
        "last_commit_date": commits[0]["commit"]["committer"]["date"] if commits else "N/A",
        "stars": repo.get("stargazers_count"),
        "open_issues": repo.get("open_issues_count"),
        "license": repo.get("license", {}).get("name") if repo.get("license") else "None"
    }
