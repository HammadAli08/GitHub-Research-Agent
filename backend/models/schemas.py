from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class RepoDiscoveryRequest(BaseModel):
    query: str
    language: Optional[str] = None
    min_stars: Optional[int] = 0

class RepoMetadata(BaseModel):
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    language: Optional[str]
    updated_at: str

class RepoDiscoveryResponse(BaseModel):
    repositories: List[RepoMetadata]

class AnalysisRequest(BaseModel):
    repo_full_name: str

class AnalysisReport(BaseModel):
    repo_name: str
    executive_summary: str
    technical_assessment: str
    risk_score: int # 1-100
    architecture_patterns: List[str]
    tech_stack: List[str]
    maintenance_quality: str
    recent_activity_summary: str
    key_findings: List[str]

class ChatRequest(BaseModel):
    repo_full_name: str
    query: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    answer: str
