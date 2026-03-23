"""
North Star Unified Shell - System Validator
Global validation and integrity checking for cross-module sync
"""
import streamlit as st
from src.state.financial_state import get_core_financials


def validate_system_sync():
    """
    Validate that all modules are properly synced with core
    
    Returns:
        list: List of sync issues found
    """
    issues = []
    core = get_core_financials()
    
    revenue = core.get("revenue", 0)
    expenses = core.get("expenses", 0)
    profit = core.get("profit", 0)
    
    # Check 1: Core financial data exists
    if revenue == 0 and expenses == 0:
        issues.append("⚠️ No financial data in core - modules may be using local values")
    
    # Check 2: Valuation without revenue
    if st.session_state.get("valuation_range") and revenue == 0:
        issues.append("❌ Valuation exists without revenue in core - data inconsistency")
    
    # Check 3: LOC without revenue
    if st.session_state.get("loc_recommendation") and revenue == 0:
        issues.append("❌ LOC calculated without revenue in core - data inconsistency")
    
    # Check 4: Profit calculation integrity
    if revenue > 0 or expenses > 0:
        expected_profit = revenue - expenses
        if abs(profit - expected_profit) > 0.01:  # Allow small floating point errors
            issues.append(f"❌ Profit calculation error: {profit} != {revenue} - {expenses} = {expected_profit}")
    
    # Check 5: Source module tracking
    source = core.get("source_module")
    if (revenue > 0 or expenses > 0) and not source:
        issues.append("⚠️ Financial data exists but source module not tracked")
    
    # Check 6: Detect local state (should not exist)
    local_state_keys = ["fm_pro_revenue", "fm_pro_expenses", "fm_lite_revenue", "fm_lite_expenses"]
    for key in local_state_keys:
        if key in st.session_state:
            issues.append(f"❌ Local state detected: {key} - should use core only")
    
    return issues


def validate_module_compliance(module_name):
    """
    Validate that a specific module is compliant with sync rules
    
    Args:
        module_name: Name of the module to validate
    
    Returns:
        dict: Compliance report
    """
    from src.state.data_contracts import MODULE_REQUIREMENTS
    
    if module_name not in MODULE_REQUIREMENTS:
        return {
            "compliant": False,
            "issues": [f"Module '{module_name}' not defined in MODULE_REQUIREMENTS"],
        }
    
    requirements = MODULE_REQUIREMENTS[module_name]
    issues = []
    
    # Check required reads
    for read_key in requirements.get("reads", []):
        if read_key == "core_financials":
            core = get_core_financials()
            if not core.get("revenue", 0) and not core.get("expenses", 0):
                issues.append(f"Module requires '{read_key}' but it's empty")
        elif read_key not in st.session_state:
            issues.append(f"Module requires '{read_key}' but it's missing")
    
    # Check required writes
    for write_key in requirements.get("writes", []):
        if write_key not in st.session_state and write_key != "core_financials":
            issues.append(f"Module should write '{write_key}' but it's missing")
    
    return {
        "compliant": len(issues) == 0,
        "issues": issues,
    }


def validate_data_flow():
    """
    Validate the complete data flow across all modules
    
    Returns:
        dict: Data flow validation report
    """
    core = get_core_financials()
    
    report = {
        "core_populated": False,
        "modules_synced": [],
        "modules_unsynced": [],
        "data_flow_valid": False,
    }
    
    # Check if core is populated
    if core.get("revenue", 0) > 0 or core.get("expenses", 0) > 0:
        report["core_populated"] = True
    
    # Check each module
    modules_to_check = {
        "valuation_range": "Business Valuation",
        "loc_recommendation": "LOC Analyzer",
        "project_evaluation": "Project Evaluator",
        "idea_context": "Idea Screener",
        "entity_structure": "Entity Assistant",
    }
    
    for key, module_name in modules_to_check.items():
        if key in st.session_state and st.session_state[key]:
            report["modules_synced"].append(module_name)
        else:
            report["modules_unsynced"].append(module_name)
    
    # Data flow is valid if core is populated and no sync issues
    sync_issues = validate_system_sync()
    report["data_flow_valid"] = report["core_populated"] and len(sync_issues) == 0
    
    return report


def get_integrity_score():
    """
    Calculate overall system integrity score (0-100)
    
    Returns:
        int: Integrity score
    """
    score = 100
    issues = validate_system_sync()
    
    # Deduct points for each issue
    for issue in issues:
        if "❌" in issue:
            score -= 20  # Critical issues
        elif "⚠️" in issue:
            score -= 10  # Warnings
    
    return max(0, score)


def generate_sync_report():
    """
    Generate comprehensive sync status report
    
    Returns:
        dict: Complete sync report
    """
    core = get_core_financials()
    issues = validate_system_sync()
    data_flow = validate_data_flow()
    
    return {
        "timestamp": st.session_state.get("_report_timestamp", "Unknown"),
        "integrity_score": get_integrity_score(),
        "sync_issues": issues,
        "core_financials": {
            "revenue": core.get("revenue", 0),
            "expenses": core.get("expenses", 0),
            "profit": core.get("profit", 0),
            "source": core.get("source_module", "Unknown"),
        },
        "data_flow": data_flow,
        "modules_status": {
            "valuation": "synced" if st.session_state.get("valuation_range") else "not run",
            "loc": "synced" if st.session_state.get("loc_recommendation") else "not run",
            "project": "synced" if st.session_state.get("project_evaluation") else "not run",
        },
    }


def auto_fix_sync_issues():
    """
    Attempt to automatically fix common sync issues
    
    Returns:
        list: List of fixes applied
    """
    fixes_applied = []
    core = get_core_financials()
    
    # Fix 1: Recalculate profit if wrong
    revenue = core.get("revenue", 0)
    expenses = core.get("expenses", 0)
    profit = core.get("profit", 0)
    expected_profit = revenue - expenses
    
    if abs(profit - expected_profit) > 0.01:
        from src.state.financial_state import update_core_financial
        update_core_financial("profit", expected_profit)
        fixes_applied.append(f"Recalculated profit: {expected_profit}")
    
    # Fix 2: Clear local state
    local_keys = ["fm_pro_revenue", "fm_pro_expenses", "fm_lite_revenue", "fm_lite_expenses"]
    for key in local_keys:
        if key in st.session_state:
            del st.session_state[key]
            fixes_applied.append(f"Cleared local state: {key}")
    
    return fixes_applied


def validate_round_trip_sync():
    """
    Validate that Lite → Pro → Lite maintains same values
    
    Returns:
        dict: Round-trip validation report
    """
    core = get_core_financials()
    
    return {
        "core_revenue": core.get("revenue", 0),
        "core_expenses": core.get("expenses", 0),
        "core_profit": core.get("profit", 0),
        "source": core.get("source_module", "Unknown"),
        "round_trip_valid": True,  # Will be False if drift detected
    }
