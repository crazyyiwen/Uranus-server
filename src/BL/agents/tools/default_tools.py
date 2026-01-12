import os
import uuid, base64
import httpx
from pydantic import BaseModel, Field
from tavily import TavilyClient
from typing_extensions import Annotated, Literal
from markdownify import markdownify

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import InjectedToolArg, InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from BL.agents.states.state import DeepAgentState
from BL.agents.tools.api_generation import dynamic_search
from core.utils.common_functions import get_today_str
from BL.agents.prompts.context_prompts import SUMMARIZE_WEB_SEARCH
from BL.agents.agents_model.model_selection import get_dynamic_model_instance

tavily_client = TavilyClient()

class Summary(BaseModel):
    """Schema for webpage content summarization."""
    filename: str = Field(description="Name of the file to store.")
    summary: str = Field(description="Key learnings from the webpage.")

@tool(parse_docstring=True)
async def search(
    query: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    max_results: Annotated[int, InjectedToolArg] = 1,
) -> Command:
    """
    Call catalog api and saves full content to files for context offloading.

    Args:
        query: Search query to execute
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        max_results: Maximum number of results to return (default: 1)

    Returns:
        Return the API search result in files
    """
    # Execute search
    search_results = await dynamic_search()

    # Process and summarize results
    # processed_results = process_search_results(search_results)
    results = search_results.get('results', [])

    # Save each result to a file and prepare summary
    files = state.get("files", {})
    saved_files = []
    summaries = []

    for i, result in enumerate(results):
        # Use the AI-generated filename from summarization
        filename = result['supplierItemNumber']

        # Create file content with full details
        file_content = f"""# Search Result: {result['shortName']}
                        **Query:** {query}
                        **Date:** {get_today_str()}
                        ## Summary
                        {result['itemDescription']}
                        """

        files[filename] = file_content
        saved_files.append(filename)
        summaries.append(f"- {filename}: {result['itemDescription']}...")

        # Create minimal summary for tool message - focus on what was collected
        summary_text = f"""🔍 Found {len(results)} result(s) for '{query}':

                        {chr(10).join(summaries)}

                        Files: {', '.join(saved_files)}
                        💡 Use read_file() to access full details when needed."""

    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(summary_text, tool_call_id=tool_call_id)
            ],
        }
    )

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on search progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the search workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?
    - How complex is the question: Have I reached the number of search limits?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"