from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.schemas import RepoDiscoveryRequest, RepoDiscoveryResponse, AnalysisRequest, AnalysisReport, ChatRequest, ChatResponse
from backend.services.github import GitHubService
from backend.agents.graph import research_graph
from backend.agents.nodes import get_llm
from langchain_core.messages import HumanMessage
import uvicorn
import os

app = FastAPI(title="GitHub Research Agent")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_service = GitHubService()

# In-memory cache for reports (per session/request)
# In production, this would be Redis or a database
REPORTS_CACHE = {}

@app.get("/health")
async def health():
    return {"status": "online", "message": "GitHub Research Agent API"}

@app.post("/search", response_model=RepoDiscoveryResponse)
async def search(request: RepoDiscoveryRequest):
    try:
        repos = await github_service.search_repositories(
            query=request.query,
            language=request.language,
            min_stars=request.min_stars
        )
        return {"repositories": repos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    try:
        initial_state = {
            "repo_full_name": request.repo_full_name,
            "structure_analysis": {},
            "content_summaries": [],
            "issue_intelligence": [],
            "trend_analysis": {},
            "community_health": {},
            "synthesis_report": {},
            "status": "Starting research..."
        }
        
        result = await research_graph.ainvoke(initial_state)
        
        # Cache the full analysis result
        REPORTS_CACHE[request.repo_full_name] = result
        
        return result.get("synthesis_report", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{owner}/{repo}")
async def get_report(owner: str, repo: str):
    full_name = f"{owner}/{repo}"
    if full_name not in REPORTS_CACHE:
        raise HTTPException(status_code=404, detail="Report not found. Please run /analyze first.")
    return REPORTS_CACHE[full_name]

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from langgraph.prebuilt import create_react_agent
from backend.agents.tools import read_github_file, get_repo_issues_intelligence, get_repo_trends_and_risks, get_repo_community_health

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    analysis_data = REPORTS_CACHE.get(request.repo_full_name)
    if not analysis_data:
        raise HTTPException(status_code=404, detail="No research data found for this repository.")
    
    llm = get_llm()
    tools = [read_github_file, get_repo_issues_intelligence, get_repo_trends_and_risks, get_repo_community_health]
    
    # Create a ReAct agent that can use tools to fetch live data if the user asks for something not in the snapshot
    agent = create_react_agent(llm, tools)
    
    import json
    context = json.dumps({
        "structure": analysis_data.get("structure_analysis"),
        "key_file_summaries": analysis_data.get("content_summaries"),
        "issue_intelligence": analysis_data.get("issue_intelligence"),
        "trends": analysis_data.get("trend_analysis"),
        "final_report": analysis_data.get("synthesis_report")
    }, indent=2)
    
    system_message = f"""You are an expert GitHub Repository Analyst and Senior Systems Engineer. 
    You are currently investigating: {request.repo_full_name}
    
    CAPABILITIES:
    1. You have a STATIC RESEARCH SNAPSHOT for quick context.
    2. You have LIVE TOOLS (like `read_github_file`) to fetch completion code for ANY file you see in the file tree.
    
    STATIC RESEARCH SNAPSHOT:
    {context}
    
    GUIDELINES:
    - If the snapshot has the answer, reply immediately.
    - If the user asks about a specific file, class, or logic not in the snapshot, YOU MUST use the `read_github_file` tool.
    - Be extremely technical. If you read a file, explain the logic line-by-line if relevant.
    - If the user asks for a code walkthrough, fetch the file first.
    - You have visibility into up to 1000 file paths in the repo structure. If you don't see a file in the 'tree_summary', you can still try to read it if the user mentions it."""
    
    messages = [
        SystemMessage(content=system_message)
    ]
    
    # Add history
    for msg in request.history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
            
    # Add current query
    messages.append(HumanMessage(content=request.query))
    
    # Invoke the agent
    result = await agent.ainvoke({"messages": messages})
    
    # The last message in the result is the answer
    final_answer = result["messages"][-1].content
    
    return {"answer": final_answer}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
