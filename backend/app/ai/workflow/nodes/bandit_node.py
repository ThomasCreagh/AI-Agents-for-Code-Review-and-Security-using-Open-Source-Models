from langchain_core.messages import SystemMessage
from app.models import AgentState
import time
import subprocess
import os
import tempfile
import json

from app.ai.workflow.utils import (
    log_debug, log_agent_start, log_agent_end,
    LOG_LEVEL_INFO, LOG_LEVEL_DEBUG, LOG_LEVEL_ERROR
)

def bandit_analysis_agent(state: AgentState):
    """
    Performs Bandit security analysis on Python code in the context.
    
    This agent:
    1. Takes code from the state context
    2. Runs Bandit analysis on it
    3. Adds the results to the context for the next agent
    """
    # Log agent start
    log_agent_start("BANDIT ANALYSIS", state)
    
    # Store original state for comparison
    original_state = state.copy()
    
    messages = state["messages"]
    query = state["latest_user_message"]
    context = state.get("context", {})

    # Get code from context
    full_code = context.get("full_code", [])
    
    if not full_code:
        log_debug("No code found to analyze with Bandit", level=LOG_LEVEL_ERROR)
        # Return state unchanged if no code to analyze
        log_agent_end("BANDIT ANALYSIS", original_state, state)
        return state
    
    # Create a temporary file to store the code for analysis
    try:
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w') as temp_file:
            # Join multiple code blocks if needed
            code_content = "\n".join(full_code)
            temp_file.write(code_content)
            temp_file_path = temp_file.name
            
        log_debug(f"Created temporary file for Bandit analysis: {temp_file_path}", level=LOG_LEVEL_DEBUG)
        
        # Run Bandit on the temp file with JSON output format
        cmd = ['bandit', '-f', 'json', '-r', temp_file_path]
        log_debug(f"Running Bandit command: {' '.join(cmd)}", level=LOG_LEVEL_INFO)
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # Timeout after 30 seconds
        )
        
        # Remove the temporary file
        try:
            os.unlink(temp_file_path)
        except Exception as e:
            log_debug(f"Error removing temporary file: {str(e)}", level=LOG_LEVEL_DEBUG)
        
        # Process the Bandit output
        bandit_results = {}
        if process.returncode == 0 or process.returncode == 1:  # Bandit returns 1 when issues are found
            log_debug("Bandit analysis completed", level=LOG_LEVEL_INFO)
            
            try:
                # Try to parse the JSON output
                bandit_results = json.loads(process.stdout)
                
                # Create a message with the analysis
                bandit_message_content = create_bandit_summary(bandit_results)
                bandit_message = SystemMessage(content=bandit_message_content)
                
                # Add results to context
                context["bandit_analysis"] = bandit_results
                
                # Create updated state
                new_state = {
                    "messages": messages + [bandit_message],
                    "latest_user_message": query,
                    "context": context
                }
                
                log_debug("Added Bandit analysis to context", level=LOG_LEVEL_INFO)
                
                # Log agent end
                log_agent_end("BANDIT ANALYSIS", original_state, new_state)
                
                return new_state
                
            except json.JSONDecodeError:
                log_debug("Failed to parse Bandit JSON output", level=LOG_LEVEL_ERROR)
                log_debug(f"Raw Bandit output: {process.stdout[:200]}...", level=LOG_LEVEL_DEBUG)
                log_debug(f"Stderr: {process.stderr[:200]}...", level=LOG_LEVEL_DEBUG)
        else:
            # Handle Bandit execution errors
            log_debug(f"Bandit analysis failed with return code {process.returncode}", level=LOG_LEVEL_ERROR)
            log_debug(f"Error output: {process.stderr[:200]}...", level=LOG_LEVEL_DEBUG)
    
    except Exception as e:
        log_debug(f"Error during Bandit analysis: {str(e)}", level=LOG_LEVEL_ERROR)
    
    # If we get here, something went wrong
    # Add error message to context
    error_message = SystemMessage(content="Bandit security scan attempted but encountered an error.")
    
    # Return state with error message
    new_state = {
        "messages": messages + [error_message],
        "latest_user_message": query,
        "context": context
    }
    
    log_agent_end("BANDIT ANALYSIS", original_state, new_state)
    return new_state

def create_bandit_summary(bandit_results):
    """
    Create a human-readable summary from Bandit results.
    """
    content = "Bandit Security Analysis Results:\n\n"
    
    # Add metrics
    metrics = bandit_results.get("metrics", {})
    if metrics:
        content += "Files scanned: {}\n".format(metrics.get("_totals", {}).get("loc", 0))
        content += "Lines of code: {}\n".format(metrics.get("_totals", {}).get("loc", 0))
    
    # Add results summary
    results = bandit_results.get("results", [])
    if results:
        content += "Total security issues found: {}\n\n".format(len(results))
        
        # Count issues by severity
        high = sum(1 for r in results if r.get("issue_severity", "").lower() == "high")
        medium = sum(1 for r in results if r.get("issue_severity", "").lower() == "medium")
        low = sum(1 for r in results if r.get("issue_severity", "").lower() == "low")
        
        content += "Severity breakdown:\n"
        content += "- HIGH: {}\n".format(high)
        content += "- MEDIUM: {}\n".format(medium)
        content += "- LOW: {}\n\n".format(low)
        
        # List high and medium severity issues
        if high or medium:
            content += "Notable security issues:\n"
            for issue in results:
                severity = issue.get("issue_severity", "").lower()
                if severity in ["high", "medium"]:
                    content += "- [{}] {}: {}\n".format(
                        issue.get("issue_severity", ""),
                        issue.get("test_id", ""),
                        issue.get("issue_text", "")
                    )
    else:
        content += "No security issues identified.\n"
    
    return content