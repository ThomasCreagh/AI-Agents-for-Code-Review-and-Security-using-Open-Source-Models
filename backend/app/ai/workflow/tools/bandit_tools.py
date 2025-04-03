from typing import Dict, Any, List
from app.ai.workflow.utils import log_debug, LOG_LEVEL_INFO, LOG_LEVEL_DEBUG

def add_bandit_to_security_response(context: Dict[str, Any], response_content: str) -> str:
    """
    Adds Bandit analysis results to the security response if available.
    
    Args:
        context: The workflow context containing analysis results
        response_content: The original response content
        
    Returns:
        Modified response content with Bandit results
    """
    # Check if Bandit analysis exists in context
    bandit_analysis = context.get("bandit_analysis", {})
    if not bandit_analysis:
        log_debug("No Bandit analysis found in context, skipping integration", level=LOG_LEVEL_DEBUG)
        return response_content
    
    log_debug("Adding Bandit results to security response", level=LOG_LEVEL_INFO)
    
    # Get Bandit results
    results = bandit_analysis.get("results", [])
    metrics = bandit_analysis.get("metrics", {})
    
    # Create Bandit section
    bandit_section = "\n## Bandit Static Analysis Results\n\n"
    
    if not results:
        bandit_section += "Bandit scan completed with no security issues identified.\n"
    else:
        # Add summary information
        total_issues = len(results)
        bandit_section += f"Bandit identified **{total_issues}** potential security issues:\n\n"
        
        # Count issues by severity
        high = sum(1 for r in results if r.get("issue_severity", "").lower() == "high")
        medium = sum(1 for r in results if r.get("issue_severity", "").lower() == "medium")
        low = sum(1 for r in results if r.get("issue_severity", "").lower() == "low")
        
        bandit_section += f"- **{high}** high severity issues\n"
        bandit_section += f"- **{medium}** medium severity issues\n"
        bandit_section += f"- **{low}** low severity issues\n\n"
        
        # Add detailed information for high and medium issues
        if high > 0 or medium > 0:
            bandit_section += "### Critical Security Issues\n\n"
            
            for issue in results:
                severity = issue.get("issue_severity", "").lower()
                if severity in ["high", "medium"]:
                    test_id = issue.get("test_id", "")
                    test_name = issue.get("test_name", "")
                    issue_text = issue.get("issue_text", "")
                    filename = issue.get("filename", "")
                    line = issue.get("line_number", 0)
                    
                    bandit_section += f"**{severity.upper()} Severity** ({test_id}: {test_name})\n"
                    bandit_section += f"- Issue: {issue_text}\n"
                    bandit_section += f"- Location: {filename}, line {line}\n\n"
    
    # Check if there's a "Recommended Fixes" section in the response
    if "## Recommended Fixes" in response_content:
        # Insert Bandit section before Recommended Fixes
        parts = response_content.split("## Recommended Fixes", 1)
        return parts[0] + bandit_section + "\n## Recommended Fixes" + parts[1]
    else:
        # Just append Bandit section at the end
        return response_content + "\n" + bandit_section
    
def format_bandit_results_summary(bandit_results: Dict[str, Any]) -> str:
    """
    Creates a concise summary of Bandit results for inclusion in responses.
    
    Args:
        bandit_results: The raw Bandit results dictionary
        
    Returns:
        A formatted string summary
    """
    if not bandit_results:
        return "No Bandit analysis results available."
    
    results = bandit_results.get("results", [])
    
    if not results:
        return "Bandit scan completed with no security issues identified."
    
    # Count issues by severity
    total = len(results)
    high = sum(1 for r in results if r.get("issue_severity", "").lower() == "high")
    medium = sum(1 for r in results if r.get("issue_severity", "").lower() == "medium")
    low = sum(1 for r in results if r.get("issue_severity", "").lower() == "low")
    
    summary = f"Bandit scan identified {total} potential security issues: "
    summary += f"{high} high, {medium} medium, and {low} low severity."
    
    # Add one or two examples of high severity issues if they exist
    if high > 0:
        high_issues = [r for r in results if r.get("issue_severity", "").lower() == "high"]
        summary += " Examples include: "
        
        for i, issue in enumerate(high_issues[:2]):
            if i > 0:
                summary += "; "
            test_id = issue.get("test_id", "")
            issue_text = issue.get("issue_text", "")
            summary += f"{test_id}: {issue_text}"
    
    return summary