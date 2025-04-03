from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.models import AgentState
import time
import json

from app.ai.dependencies import AIDependencies
from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG
)
from app.ai.workflow.tools.security_tools import create_final_response_prompt
from app.ai.workflow.tools.message_tools import create_prompt_message, format_llm_response
# We don't need to import the bandit_tools module - we'll implement directly here

def generate_response(state: AgentState, deps: AIDependencies):
    """
    Generates the final structured response based on all previous analysis.
    """
    # Log agent start
    log_agent_start("RESPONSE GENERATION", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    # Apply throttling delay if enabled
    if deps.enable_throttling:
        delay = deps.throttling_delay
        log_debug(f"Applying throttling delay: {delay}s", level=LOG_LEVEL_DEBUG)
        time.sleep(delay)

    # Get code summary for structured response
    code_summary = context.get("code_summary", None)
    
    # Get full code for reference
    full_code = context.get("full_code", [])
    
    # Get document sources
    doc_sources = context.get("doc_sources", [])
    
    # Check if there are any document sources
    has_sources = len(doc_sources) > 0
    
    # Log the sources
    if has_sources:
        source_names = [src.get('source', 'unknown') for src in doc_sources if isinstance(src, dict)]
        log_debug(f"Security standards used in response: {', '.join(source_names)}", level=LOG_LEVEL_INFO)
    else:
        log_debug("No security standards available for response", level=LOG_LEVEL_INFO)
    
    # Check for Bandit results
    bandit_analysis = context.get("bandit_analysis", {})
    has_bandit_results = bool(bandit_analysis)
    if has_bandit_results:
        log_debug("Bandit analysis results available for response integration", level=LOG_LEVEL_INFO)
        
        # Log detailed Bandit findings for debugging
        results = bandit_analysis.get("results", [])
        log_debug(f"Bandit found {len(results)} potential issues", level=LOG_LEVEL_DEBUG)
        
        # Prepare Bandit information for inclusion in prompt
        bandit_summary = "## Bandit Static Analysis Results\n\n"
        
        if results:
            # Count issues by severity
            high = sum(1 for r in results if r.get("issue_severity", "").lower() == "high")
            medium = sum(1 for r in results if r.get("issue_severity", "").lower() == "medium")
            low = sum(1 for r in results if r.get("issue_severity", "").lower() == "low")
            
            bandit_summary += f"Bandit identified {len(results)} potential security issues:\n"
            bandit_summary += f"- HIGH severity: {high}\n"
            bandit_summary += f"- MEDIUM severity: {medium}\n"
            bandit_summary += f"- LOW severity: {low}\n\n"
            
            # Add examples of high and medium issues
            high_medium_issues = [r for r in results if r.get("issue_severity", "").lower() in ["high", "medium"]]
            if high_medium_issues:
                bandit_summary += "Notable issues:\n"
                for issue in high_medium_issues[:3]:  # Limit to top 3
                    bandit_summary += f"- {issue.get('test_id', '')}: {issue.get('issue_text', '')}\n"
        else:
            bandit_summary += "No security issues identified by Bandit scan.\n"
    else:
        bandit_summary = None
    
    # Create final response prompt
    response_prompt_content = create_final_response_prompt()
    log_debug(
        "Created final response prompt", 
        level=LOG_LEVEL_DEBUG,
        data=response_prompt_content[:100] + "..." if len(response_prompt_content) > 100 else response_prompt_content
    )
    
    # Add Bandit summary to prompt if available
    if bandit_summary:
        response_prompt_content += f"\n\nInclude the following Bandit static analysis results in your response:\n{bandit_summary}"
        log_debug("Added Bandit results to prompt", level=LOG_LEVEL_INFO)
    
    # Create function list to help with structured output if available
    if code_summary:
        function_list = "Functions to reference in analysis:\n"
        for func_name in code_summary.get('functions', []):
            function_list += f"- {func_name}\n"
        
        # Add the function list to the prompt content
        response_prompt_content += f"\n\n{function_list}"
    
    # Add explicit sources instruction
    if has_sources:
        sources_list = "SOURCES TO REFERENCE (MUST CITE THESE EXACT SOURCES):\n"
        for src in doc_sources:
            if isinstance(src, dict):
                page_info = f", page {src.get('page', '')}" if src.get('page', '') else ""
                sources_list += f"{src.get('id', '')} {src.get('source', 'unknown')}{page_info}\n"
        
        response_prompt_content += f"\n\n{sources_list}\n\nIMPORTANT: You MUST list these exact sources in your Sources section. Do not reference any other security standards."
        log_debug("Added explicit sources list to prompt", level=LOG_LEVEL_INFO)
    else:
        response_prompt_content += "\n\nNo specific security standards were provided. State this in your Sources section."
    
    response_prompt = create_prompt_message(response_prompt_content)
    
    # Create a message with the complete original code if available
    if full_code:
        original_code = "\n".join(full_code)
        full_code_message = SystemMessage(content=f"Complete code for analysis:\n```python\n{original_code}\n```")
        log_debug("Added complete original code to final response", level=LOG_LEVEL_INFO)
    else:
        full_code_message = None
    
    # Modify query message to also emphasize sources
    if has_sources:
        source_names = [src.get('source', 'unknown') for src in doc_sources if isinstance(src, dict)]
        formatted_sources = ", ".join(source_names)
        query_message = HumanMessage(content=f"""
        User question: {query}
        
        IMPORTANT: Base your analysis on these security standards: {formatted_sources}
        Your final response MUST include these exact sources in the Sources section.
        """)
    else:
        query_message = HumanMessage(content=f"User question: {query}")

    # Create agent messages for LLM
    agent_messages = [response_prompt]
    
    # Add full code message right after the response prompt
    if full_code_message:
        agent_messages.append(full_code_message)
    
    # Add existing messages
    agent_messages.extend(messages)
    
    # Add query message at the end
    agent_messages.append(query_message)
    
    log_debug(f"Preparing LLM request with {len(agent_messages)} messages", level=LOG_LEVEL_DEBUG)

    # Log final response request
    log_debug("Sending final response request to LLM", level=LOG_LEVEL_INFO)

    # Get response from LLM
    response = deps.llm.invoke(agent_messages)
    
    # Format response
    formatted_response = format_llm_response(response)
    response_content = formatted_response.content
    
    # Ensure Bandit results are in the response
    if has_bandit_results and "## Bandit" not in response_content:
        log_debug("Bandit results not found in response, manually adding them", level=LOG_LEVEL_INFO)
        
        # Find a good place to insert Bandit section
        if "## Recommended Fixes" in response_content:
            parts = response_content.split("## Recommended Fixes", 1)
            response_content = parts[0] + "\n\n## Bandit Static Analysis Results\n" + bandit_summary + "\n## Recommended Fixes" + parts[1]
        else:
            response_content += "\n\n## Bandit Static Analysis Results\n" + bandit_summary
            
        # Create a new message with the modified content
        formatted_response = AIMessage(content=response_content)
        
        log_debug("Manually added Bandit analysis to response", level=LOG_LEVEL_INFO)
    
    # Ensure sources are included if they exist
    if has_sources and "## Sources" not in response_content:
        log_debug("Sources section not found in response, manually adding it", level=LOG_LEVEL_INFO)
        
        # Create a sources section
        sources_section = "\n\n## Sources\n"
        for src in doc_sources:
            if isinstance(src, dict):
                page_info = f", page {src.get('page', '')}" if src.get('page', '') else ""
                sources_section += f"{src.get('id', '')} {src.get('source', 'unknown')}{page_info}\n"
        
        # Add to response content
        response_content += sources_section
        formatted_response = AIMessage(content=response_content)
        
        log_debug("Manually added sources section to response", level=LOG_LEVEL_INFO)
    elif not has_sources and "## Sources" not in response_content:
        log_debug("No sources available and Sources section missing, adding empty sources note", level=LOG_LEVEL_INFO)
        
        # Add empty sources note
        response_content += "\n\n## Sources\nNo specific security standards referenced."
        formatted_response = AIMessage(content=response_content)
    
    # Log response preview
    response_preview = response_content[:100] + "..." if len(response_content) > 100 else response_content
    log_debug(
        "Generated final response:", 
        level=LOG_LEVEL_INFO,
        data=response_preview
    )

    # Create updated state
    new_state = {
        "messages": messages + [formatted_response],
        "latest_user_message": query,
        "context": context  
    }
    
    # Log agent end
    log_agent_end("RESPONSE GENERATION", original_state, new_state)
    
    return new_state