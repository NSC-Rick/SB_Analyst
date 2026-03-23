"""
North Star Unified Shell - Sync Engine
Enforces single source of truth for financial data across all modules
"""
import streamlit as st
from datetime import datetime


def enforce_core_defaults(local_value, core_value):
    """
    Enforce core financial value as default if it exists
    
    Args:
        local_value: Local/default value to use if core is empty
        core_value: Value from core financials
    
    Returns:
        Core value if valid, otherwise local value
    """
    if core_value is not None and core_value > 0:
        return core_value
    return local_value


def push_to_core(data, source_module=None):
    """
    Push financial data to core state with validation
    
    Args:
        data: Dictionary of financial data to push
        source_module: Name of module pushing the data
    """
    from src.state.financial_state import update_core_financials
    
    # Add metadata
    if source_module:
        data["_last_updated_by"] = source_module
        data["_last_updated_at"] = datetime.now().isoformat()
    
    # Push to core with validation
    update_core_financials(data, source=source_module)
    
    # Track in session state for debugging
    if "sync_history" not in st.session_state:
        st.session_state.sync_history = []
    
    st.session_state.sync_history.append({
        "timestamp": datetime.now().isoformat(),
        "source": source_module,
        "keys": list(data.keys()),
    })
    
    # Keep only last 10 sync events
    if len(st.session_state.sync_history) > 10:
        st.session_state.sync_history = st.session_state.sync_history[-10:]


def pull_from_core(key, default=0):
    """
    Pull a single value from core financials
    
    Args:
        key: Key to retrieve from core financials
        default: Default value if key not found
    
    Returns:
        Value from core or default
    """
    from src.state.financial_state import get_core_financials
    
    core = get_core_financials()
    return core.get(key, default)


def sync_status():
    """
    Get current sync status information
    
    Returns:
        dict: Sync status with source and timestamp
    """
    from src.state.financial_state import get_core_financials
    
    core = get_core_financials()
    
    return {
        "has_data": core.get("revenue", 0) > 0 or core.get("expenses", 0) > 0,
        "last_updated_by": core.get("_last_updated_by", "Unknown"),
        "last_updated_at": core.get("_last_updated_at", "Never"),
        "source_module": core.get("source_module", "Unknown"),
    }


def enforce_read_only(module_name):
    """
    Mark a module as read-only (should not write to core)
    
    Args:
        module_name: Name of the module
    
    Returns:
        bool: True if module should only read
    """
    READ_ONLY_MODULES = [
        "Business Valuation",
        "LOC Analyzer",
        "Project Evaluator",
        "Insights Engine",
        "Command Center",
    ]
    
    return module_name in READ_ONLY_MODULES


def validate_write_permission(module_name):
    """
    Check if module has permission to write to core
    
    Args:
        module_name: Name of the module
    
    Returns:
        tuple: (allowed, message)
    """
    if enforce_read_only(module_name):
        return False, f"{module_name} is read-only and should not write to core financials"
    
    WRITE_ALLOWED_MODULES = [
        "Financial Modeler Lite",
        "Financial Modeler Pro",
    ]
    
    if module_name in WRITE_ALLOWED_MODULES:
        return True, "Write permission granted"
    
    return False, f"{module_name} does not have write permission"


def get_sync_history():
    """
    Get recent sync history
    
    Returns:
        list: Recent sync events
    """
    return st.session_state.get("sync_history", [])


def clear_sync_history():
    """Clear sync history"""
    if "sync_history" in st.session_state:
        st.session_state.sync_history = []


def detect_drift():
    """
    Detect if any modules have drifted from core
    
    Returns:
        dict: Drift detection report
    """
    from src.state.financial_state import get_core_financials
    
    core = get_core_financials()
    core_revenue = core.get("revenue", 0)
    
    drift_report = {
        "has_drift": False,
        "issues": [],
    }
    
    # Check if valuation exists without revenue
    if st.session_state.get("valuation_range") and core_revenue == 0:
        drift_report["has_drift"] = True
        drift_report["issues"].append("Valuation exists but core revenue is 0")
    
    # Check if LOC exists without revenue
    if st.session_state.get("loc_recommendation") and core_revenue == 0:
        drift_report["has_drift"] = True
        drift_report["issues"].append("LOC recommendation exists but core revenue is 0")
    
    # Check for local financial state (should not exist)
    if "fm_pro_revenue" in st.session_state and st.session_state["fm_pro_revenue"] != core_revenue:
        drift_report["has_drift"] = True
        drift_report["issues"].append(f"Pro has local revenue ({st.session_state['fm_pro_revenue']}) != core ({core_revenue})")
    
    return drift_report


def force_sync_all():
    """
    Force all modules to re-sync with core
    This clears any local state and forces reads from core
    """
    # Clear any local financial state
    keys_to_clear = [
        "fm_pro_revenue",
        "fm_pro_expenses",
        "fm_lite_revenue",
        "fm_lite_expenses",
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Clear sync history
    clear_sync_history()
    
    return "All modules forced to re-sync with core"
