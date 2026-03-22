"""
North Star Unified Shell - State Persistence Engine
Save and load full workspace state to/from JSON files
"""
import streamlit as st
import json
from datetime import datetime
from typing import Dict, Any, Optional


# Version for state file format
STATE_VERSION = "1.0"

# Required keys for valid state file
REQUIRED_KEYS = ["version"]

# State keys to persist (comprehensive list)
PERSISTABLE_STATE_KEYS = [
    # Core financial data
    "core_financials",
    
    # Module-specific data
    "idea_context",
    "idea_screener_results",
    "project_evaluation",
    "project_evaluator_results",
    "valuation_range",
    "loc_recommendation",
    
    # App state
    "active_module",
    "app_mode",
    "active_client",
    "insights_visible",
    
    # Additional module states
    "financial_modeler_inputs",
    "scenario_data"
]


def export_project_state() -> Dict[str, Any]:
    """
    Export current project state to a dictionary
    
    Returns:
        dict: Complete project state with metadata
    """
    state_data = {
        "version": STATE_VERSION,
        "metadata": {
            "saved_at": datetime.now().isoformat(),
            "app_version": "1.0.0 Lite",
            "state_keys_count": 0
        }
    }
    
    # Export all persistable state keys
    for key in PERSISTABLE_STATE_KEYS:
        if key in st.session_state:
            state_data[key] = st.session_state[key]
    
    # Update metadata count
    state_data["metadata"]["state_keys_count"] = len([k for k in PERSISTABLE_STATE_KEYS if k in state_data])
    
    return state_data


def validate_project_state(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate project state data before loading
    
    Args:
        data: State data dictionary to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check if data is a dictionary
    if not isinstance(data, dict):
        return False, "Invalid file format: not a valid JSON object"
    
    # Check for required keys
    for key in REQUIRED_KEYS:
        if key not in data:
            return False, f"Invalid project file: missing required field '{key}'"
    
    # Check version compatibility
    file_version = data.get("version")
    if file_version != STATE_VERSION:
        # For now, just warn but allow loading
        # In future versions, might need migration logic
        pass
    
    # Check if file has any actual data
    has_data = any(key in data for key in PERSISTABLE_STATE_KEYS)
    if not has_data:
        return False, "Invalid project file: no data found"
    
    return True, None


def load_project_state(data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Load project state from dictionary into session state
    
    Args:
        data: State data dictionary
    
    Returns:
        tuple: (success, error_message)
    """
    # Validate first
    is_valid, error_msg = validate_project_state(data)
    if not is_valid:
        return False, error_msg
    
    # Load each state key
    loaded_count = 0
    for key in PERSISTABLE_STATE_KEYS:
        if key in data:
            st.session_state[key] = data[key]
            loaded_count += 1
    
    # Special handling: ensure idea_screener_results is boolean if present
    if "idea_screener_results" in st.session_state:
        if not isinstance(st.session_state["idea_screener_results"], bool):
            st.session_state["idea_screener_results"] = True
    
    # Special handling: ensure project_evaluator_results is boolean if present
    if "project_evaluator_results" in st.session_state:
        if not isinstance(st.session_state["project_evaluator_results"], bool):
            st.session_state["project_evaluator_results"] = True
    
    return True, f"Successfully loaded {loaded_count} state items"


def get_state_summary() -> Dict[str, Any]:
    """
    Get summary of current state for display
    
    Returns:
        dict: Summary information about current state
    """
    summary = {
        "has_financial_data": "core_financials" in st.session_state,
        "has_idea_context": "idea_context" in st.session_state,
        "has_project_evaluation": "project_evaluation" in st.session_state,
        "has_valuation": "valuation_range" in st.session_state,
        "active_module": st.session_state.get("active_module", "None"),
        "total_state_items": len([k for k in PERSISTABLE_STATE_KEYS if k in st.session_state])
    }
    
    return summary


def clear_project_state():
    """
    Clear all project-specific state (reset workspace)
    Keeps app-level settings like active_module
    """
    keys_to_clear = [
        "core_financials",
        "idea_context",
        "idea_screener_results",
        "project_evaluation",
        "project_evaluator_results",
        "valuation_range",
        "loc_recommendation",
        "financial_modeler_inputs",
        "scenario_data"
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def generate_project_filename() -> str:
    """
    Generate a default filename for project save
    
    Returns:
        str: Filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Try to include project/idea name if available
    if "idea_context" in st.session_state:
        idea_title = st.session_state["idea_context"].get("idea_title", "")
        if idea_title:
            # Sanitize title for filename
            safe_title = "".join(c for c in idea_title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:30]  # Limit length
            return f"ns_project_{safe_title}_{timestamp}.json"
    
    if "project_evaluation" in st.session_state:
        project_name = st.session_state["project_evaluation"].get("project_name", "")
        if project_name:
            safe_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')[:30]
            return f"ns_project_{safe_name}_{timestamp}.json"
    
    return f"ns_project_{timestamp}.json"


def get_state_file_info(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract information from a state file for display
    
    Args:
        data: State data dictionary
    
    Returns:
        dict: File information
    """
    info = {
        "version": data.get("version", "Unknown"),
        "saved_at": data.get("metadata", {}).get("saved_at", "Unknown"),
        "state_keys_count": data.get("metadata", {}).get("state_keys_count", 0),
        "has_idea": "idea_context" in data,
        "has_project": "project_evaluation" in data,
        "has_financials": "core_financials" in data,
        "has_valuation": "valuation_range" in data
    }
    
    # Extract names if available
    if info["has_idea"] and isinstance(data.get("idea_context"), dict):
        info["idea_title"] = data["idea_context"].get("idea_title", "Untitled")
    
    if info["has_project"] and isinstance(data.get("project_evaluation"), dict):
        info["project_name"] = data["project_evaluation"].get("project_name", "Untitled")
    
    return info
