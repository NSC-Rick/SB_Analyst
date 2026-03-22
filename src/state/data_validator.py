"""
North Star Unified Shell - Data Validator
Validation and sanitization functions for cross-module data integrity
"""
from src.state.data_contracts import (
    CORE_FINANCIALS_SCHEMA,
    DEFAULT_CORE_FINANCIALS,
    INTEGRITY_RULES,
    SYSTEM_KEYS,
)


def validate_core_financials(data):
    """
    Validate and sanitize core financial data
    
    Args:
        data: Dict with financial data
    
    Returns:
        dict: Validated and sanitized financial data
    """
    if not isinstance(data, dict):
        return DEFAULT_CORE_FINANCIALS.copy()
    
    validated = {}
    
    # Validate each field
    validated["revenue"] = float(data.get("revenue", 0))
    validated["expenses"] = float(data.get("expenses", 0))
    
    # Calculate profit (enforce integrity rule)
    validated["profit"] = validated["revenue"] - validated["expenses"]
    
    # Validate growth rate (enforce range)
    growth_rate = float(data.get("growth_rate", 0))
    min_growth, max_growth = INTEGRITY_RULES["growth_rate_range"]
    validated["growth_rate"] = max(min_growth, min(max_growth, growth_rate))
    
    # Validate projection months (enforce range)
    projection_months = int(data.get("projection_months", 12))
    min_months, max_months = INTEGRITY_RULES["projection_months_range"]
    validated["projection_months"] = max(min_months, min(max_months, projection_months))
    
    # Optional fields
    validated["cogs"] = float(data.get("cogs", 0))
    validated["operating_expenses"] = float(data.get("operating_expenses", 0))
    validated["cash_on_hand"] = float(data.get("cash_on_hand", 0))
    
    return validated


def validate_valuation(data):
    """
    Validate valuation data
    
    Args:
        data: Valuation data (tuple or dict)
    
    Returns:
        tuple or None: Validated (low, high) or None if invalid
    """
    if isinstance(data, tuple) and len(data) == 2:
        low, high = data
        if low > 0 and high > 0 and high >= low:
            return (float(low), float(high))
    
    if isinstance(data, dict):
        low = data.get("low", 0)
        high = data.get("high", 0)
        if low > 0 and high > 0 and high >= low:
            return (float(low), float(high))
    
    return None


def validate_loc_recommendation(data):
    """
    Validate LOC recommendation data
    
    Args:
        data: Dict with LOC data
    
    Returns:
        dict or None: Validated LOC data or None if invalid
    """
    if not isinstance(data, dict):
        return None
    
    recommended_amount = float(data.get("recommended_amount", 0))
    
    if recommended_amount < 0:
        return None
    
    return {
        "recommended_amount": recommended_amount,
        "utilization_rate": float(data.get("utilization_rate", 0)),
        "monthly_payment": float(data.get("monthly_payment", 0)),
        "purpose": str(data.get("purpose", "")),
        "risk_level": str(data.get("risk_level", "")),
    }


def validate_project_evaluation(data):
    """
    Validate project evaluation data
    
    Args:
        data: Dict with project evaluation data
    
    Returns:
        dict or None: Validated project data or None if invalid
    """
    if not isinstance(data, dict):
        return None
    
    min_score, max_score = INTEGRITY_RULES["score_range"]
    
    overall_score = int(data.get("overall_score", 0))
    if not (min_score <= overall_score <= max_score):
        return None
    
    return {
        "overall_score": overall_score,
        "priority_classification": str(data.get("priority_classification", "Unknown")),
        "market_score": max(min_score, min(max_score, int(data.get("market_score", 0)))),
        "financial_score": max(min_score, min(max_score, int(data.get("financial_score", 0)))),
        "execution_score": max(min_score, min(max_score, int(data.get("execution_score", 0)))),
        "risk_score": max(min_score, min(max_score, int(data.get("risk_score", 0)))),
    }


def validate_idea_context(data):
    """
    Validate idea context data
    
    Args:
        data: Dict with idea context data
    
    Returns:
        dict or None: Validated idea data or None if invalid
    """
    if not isinstance(data, dict):
        return None
    
    if not data.get("idea_title"):
        return None
    
    min_score, max_score = INTEGRITY_RULES["score_range"]
    
    return {
        "idea_title": str(data.get("idea_title", "")),
        "viability_score": max(min_score, min(max_score, int(data.get("viability_score", 0)))),
        "market_rating": max(min_score, min(max_score, int(data.get("market_rating", 0)))),
        "revenue_rating": max(min_score, min(max_score, int(data.get("revenue_rating", 0)))),
        "competition_rating": max(min_score, min(max_score, int(data.get("competition_rating", 0)))),
        "execution_rating": max(min_score, min(max_score, int(data.get("execution_rating", 0)))),
    }


def validate_entity_structure(data):
    """
    Validate entity structure data
    
    Args:
        data: Dict with entity structure data
    
    Returns:
        dict or None: Validated entity data or None if invalid
    """
    if not isinstance(data, dict):
        return None
    
    if not data.get("entity_type"):
        return None
    
    return {
        "entity_type": str(data.get("entity_type", "")),
        "reasoning": str(data.get("reasoning", "")),
        "tax_implications": data.get("tax_implications", {}),
        "next_steps": data.get("next_steps", []),
    }


def validate_capital_stack(data):
    """
    Validate capital stack data
    
    Args:
        data: Dict with capital stack data
    
    Returns:
        dict or None: Validated capital stack or None if invalid
    """
    if not isinstance(data, dict):
        return None
    
    total = float(data.get("total_capital_need", 0))
    if total <= 0:
        return None
    
    return {
        "total_capital_need": total,
        "equity_amount": float(data.get("equity_amount", 0)),
        "debt_amount": float(data.get("debt_amount", 0)),
        "loc_amount": float(data.get("loc_amount", 0)),
        "structure": data.get("structure", {}),
    }


def validate_system_integrity(session_state):
    """
    Check system-wide data integrity
    
    Args:
        session_state: Streamlit session state
    
    Returns:
        dict: Integrity report with missing keys and validation status
    """
    report = {
        "missing_keys": [],
        "invalid_data": [],
        "valid_keys": [],
        "integrity_score": 0,
    }
    
    # Check for missing keys
    for key in SYSTEM_KEYS:
        if key not in session_state:
            report["missing_keys"].append(key)
        else:
            # Validate data if present
            data = session_state[key]
            
            if key == "core_financials":
                validated = validate_core_financials(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "valuation_range":
                validated = validate_valuation(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "loc_recommendation":
                validated = validate_loc_recommendation(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "project_evaluation":
                validated = validate_project_evaluation(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "idea_context":
                validated = validate_idea_context(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "entity_structure":
                validated = validate_entity_structure(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
            
            elif key == "capital_stack":
                validated = validate_capital_stack(data)
                if validated:
                    report["valid_keys"].append(key)
                else:
                    report["invalid_data"].append(key)
    
    # Calculate integrity score
    total_keys = len(SYSTEM_KEYS)
    valid_count = len(report["valid_keys"])
    report["integrity_score"] = int((valid_count / total_keys) * 100) if total_keys > 0 else 0
    
    return report


def get_data_sync_status(session_state, module_name):
    """
    Get sync status for a specific module
    
    Args:
        session_state: Streamlit session state
        module_name: Name of the module
    
    Returns:
        str: Sync status ("synced", "partial", "unsynced")
    """
    from src.state.data_contracts import MODULE_REQUIREMENTS
    
    if module_name not in MODULE_REQUIREMENTS:
        return "unsynced"
    
    requirements = MODULE_REQUIREMENTS[module_name]
    required_reads = requirements.get("reads", [])
    
    if not required_reads:
        return "synced"  # No requirements
    
    missing = 0
    for key in required_reads:
        if key not in session_state or not session_state[key]:
            missing += 1
    
    if missing == 0:
        return "synced"
    elif missing < len(required_reads):
        return "partial"
    else:
        return "unsynced"
