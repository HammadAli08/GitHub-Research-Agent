import os
import httpx
import base64
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            # Fine-grained PATs work well with Bearer token
            self.headers["Authorization"] = f"Bearer {self.token}"
        else:
            print("Warning: GITHUB_TOKEN not found in .env. API rate limits will be severely restricted.")
        
        # Increased timeout for complex research tasks
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def search_repositories(self, query: str, language: Optional[str] = None, min_stars: int = 0) -> List[Dict[str, Any]]:
        # 1. Detection: Check if query is a GitHub URL or owner/repo pattern
        candidate_name = None
        query_stripped = query.strip().rstrip("/")
        
        if "github.com/" in query_stripped:
            # Extract owner/repo from URL (e.g., https://github.com/langchain-ai/langchain)
            parts = query_stripped.split("github.com/")[1].split("/")
            if len(parts) >= 2:
                candidate_name = f"{parts[0]}/{parts[1]}"
        elif "/" in query_stripped and " " not in query_stripped:
             # Pattern: owner/repo
             candidate_name = query_stripped

        if candidate_name:
            try:
                details = await self.get_repo_details(candidate_name)
                if details and "full_name" in details:
                    return [{
                        "full_name": details["full_name"],
                        "description": details.get("description"),
                        "url": details["html_url"],
                        "stars": details["stargazers_count"],
                        "forks": details["forks_count"],
                        "language": details["language"],
                        "updated_at": details["updated_at"]
                    }]
            except Exception:
                pass # Fall back to search if direct fetch fails

        # 2. Traditional Search Logic
        full_query = query
        if language:
            full_query += f" language:{language}"
        if min_stars > 0:
            full_query += f" stars:>={min_stars}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search/repositories",
                params={"q": full_query, "sort": "stars", "order": "desc", "per_page": 10},
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            items = response.json().get("items", [])
            return [
                {
                    "full_name": item["full_name"],
                    "description": item["description"],
                    "url": item["html_url"],
                    "stars": item["stargazers_count"],
                    "forks": item["forks_count"],
                    "language": item["language"],
                    "updated_at": item["updated_at"]
                }
                for item in items
            ]

    async def get_repo_details(self, repo_full_name: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}", 
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 404:
                return {}
            response.raise_for_status()
            return response.json()

    async def get_languages(self, repo_full_name: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/languages", 
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            return {}

    async def get_community_profile(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch community health metrics (license, readme, contributing, etc.)"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/community/profile",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.json()
            return {}

    async def get_file_tree(self, repo_full_name: str, recursive: bool = True) -> List[Dict[str, Any]]:
        # Get the default branch first
        repo = await self.get_repo_details(repo_full_name)
        branch = repo.get("default_branch", "main")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/git/trees/{branch}",
                params={"recursive": 1 if recursive else 0},
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("tree", [])

    async def fetch_file_content(self, repo_full_name: str, path: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/contents/{path}",
                headers=self.headers,
                timeout=self.timeout
            )
            if response.status_code == 404:
                return ""
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and "content" in data:
                return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
            return ""

    async def get_issues_and_prs(self, repo_full_name: str, state: str = "all", per_page: int = 30) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/issues",
                params={"state": state, "per_page": per_page, "sort": "updated", "direction": "desc"},
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    async def get_commits(self, repo_full_name: str, per_page: int = 30) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{repo_full_name}/commits",
                params={"per_page": per_page},
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
