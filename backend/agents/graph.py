from langgraph.graph import StateGraph, END
from backend.agents.nodes import AgentState, code_analysis_node, intelligence_node, trend_node, community_node, synthesis_node

def create_research_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("code_analysis", code_analysis_node)
    workflow.add_node("intelligence", intelligence_node)
    workflow.add_node("trend", trend_node)
    workflow.add_node("community", community_node)
    workflow.add_node("synthesis", synthesis_node)

    # Define Edges
    workflow.set_entry_point("code_analysis")
    workflow.add_edge("code_analysis", "intelligence")
    workflow.add_edge("intelligence", "trend")
    workflow.add_edge("trend", "community")
    workflow.add_edge("community", "synthesis")
    workflow.add_edge("synthesis", END)

    return workflow.compile()

# For a more "parallel" feel, we could use a custom router, 
# but a linear flow here ensures we don't hit GitHub rate limits too hard simultaneously.
research_graph = create_research_graph()
