import os
from typing import Dict, TypedDict, List, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from backend.agents.tools import analyze_repo_structure, read_github_file, get_repo_issues_intelligence, get_repo_trends_and_risks, get_repo_community_health
from dotenv import load_dotenv
import json

load_dotenv()

class AgentState(TypedDict):
    repo_full_name: str
    structure_analysis: Dict[str, Any]
    content_summaries: List[str]
    issue_intelligence: List[Dict[str, Any]]
    trend_analysis: Dict[str, Any]
    community_health: Dict[str, Any]
    synthesis_report: Dict[str, Any]
    status: str

def get_llm():
    # Use llama-3.3-70b-versatile as it is highly stable on Groq
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

async def code_analysis_node(state: AgentState):
    try:
        llm = get_llm()
        repo = state["repo_full_name"]
        
        # 1. Analyze structure
        struct = await analyze_repo_structure.ainvoke({"repo_full_name": repo})
        
        # 2. Read key files (README and one or two core files)
        contents = []
        for file_path in struct.get("key_files", [])[:3]:
            try:
                content = await read_github_file.ainvoke({"repo_full_name": repo, "path": file_path})
                if content:
                    prompt = f"Summarize the technical purpose of this file: {file_path}\n\nContent:\n{content[:4000]}"
                    res = await llm.ainvoke([HumanMessage(content=prompt)])
                    contents.append(f"File: {file_path}\nSummary: {res.content}")
            except Exception as e:
                print(f"Error reading/summarizing {file_path}: {e}")
                continue
                
        return {
            "structure_analysis": struct,
            "content_summaries": contents,
            "status": "Code analysis complete."
        }
    except Exception as e:
        return {
            "structure_analysis": {"tree_summary": [], "key_files": []},
            "content_summaries": [f"Error during code analysis: {str(e)}"],
            "status": f"Code analysis failed: {str(e)}"
        }

async def intelligence_node(state: AgentState):
    try:
        repo = state["repo_full_name"]
        intelligence = await get_repo_issues_intelligence.ainvoke({"repo_full_name": repo})
        return {
            "issue_intelligence": intelligence,
            "status": "Issue & PR intelligence gathering complete."
        }
    except Exception as e:
        return {
            "issue_intelligence": [],
            "status": f"Issue intelligence gathering failed: {str(e)}"
        }

async def trend_node(state: AgentState):
    try:
        repo = state["repo_full_name"]
        trends = await get_repo_trends_and_risks.ainvoke({"repo_full_name": repo})
        return {
            "trend_analysis": trends,
            "status": "Trend and risk analysis complete."
        }
    except Exception as e:
        return {
            "trend_analysis": {},
            "status": f"Trend analysis failed: {str(e)}"
        }

async def community_node(state: AgentState):
    try:
        repo = state["repo_full_name"]
        health = await get_repo_community_health.ainvoke({"repo_full_name": repo})
        return {
            "community_health": health,
            "status": "Community health assessment complete."
        }
    except Exception as e:
        return {
            "community_health": {},
            "status": f"Community health assessment failed: {str(e)}"
        }

async def synthesis_node(state: AgentState):
    llm = get_llm()
    
    # Construct a high-density prompt for synthesis
    context = f"""
    Repository: {state['repo_full_name']}
    
    Structure: {json.dumps(state['structure_analysis'])}
    
    Key File Summaries:
    {chr(10).join(state['content_summaries'])}
    
    Issue & PR Intelligence:
    {json.dumps(state['issue_intelligence'])}
    
    Trend & Risk Data:
    {json.dumps(state['trend_analysis'])}
    
    Community Health & Ecosystem:
    {json.dumps(state['community_health'])}
    """
    
    prompt = f"""
    You are a Senior AI Systems Engineer. Synthesize the provided research data into a production-grade Technical Research Report.
    
    REPORT REQUIREMENTS:
    - Executive summary: High-level purpose and value proposition.
    - Technical assessment: Detailed look at architecture, stack, and patterns.
    - Risk score: 1-100 (where 100 is critical risk).
    - Maintenance: Assessment of update frequency and community health.
    - Findings: 3-5 distinct, high-impact bullet points.
    
    OUTPUT FORMAT: You MUST output ONLY a valid JSON object. No other text.
    JSON KEYS: executive_summary, technical_assessment, risk_score (int), architecture_patterns (list), tech_stack (list), maintenance_quality, recent_activity_summary, key_findings (list)
    
    DATA PROVIDED:
    {context}
    """
    
    response = await llm.ainvoke([
        SystemMessage(content="You are a JSON-only response engine. You never include conversational filler or markdown code blocks unless requested. Your output must be parseable by json.loads()."),
        HumanMessage(content=prompt)
    ])
    
    try:
        content = response.content.strip()
        # Handle potential markdown wrapping
        if content.startswith("```"):
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                content = match.group(0)
        
        report = json.loads(content)
        
        # Ensure all required keys exist (basic validation)
        required_keys = ["executive_summary", "technical_assessment", "risk_score", "architecture_patterns", "tech_stack", "maintenance_quality", "recent_activity_summary", "key_findings"]
        for key in required_keys:
            if key not in report:
                report[key] = "N/A" if "list" not in key else []
        
        return {
            "synthesis_report": report,
            "status": "Synthesis report generated successfully."
        }
    except Exception as e:
        return {
            "synthesis_report": {
                "executive_summary": "Failed to generate synthesis report.",
                "technical_assessment": f"Parsing Error: {str(e)}",
                "risk_score": 0,
                "architecture_patterns": [],
                "tech_stack": [],
                "maintenance_quality": "Unknown",
                "recent_activity_summary": "Unknown",
                "key_findings": ["Error: The LLM response could not be parsed as valid JSON.", f"Raw response start: {response.content[:100]}..."]
            },
            "status": "Synthesis failed due to parsing error."
        }
