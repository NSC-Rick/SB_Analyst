"""
Core Financial State Sync Layer
Single source of truth for financial values across modules
"""
import streamlit as st


CORE_FINANCIAL_FIELDS = {
    "revenue": 0.0,
    "expenses": 0.0,
    "profit": 0.0,
    "growth_rate": 0.0,
    "payroll": 0.0,
    "starting_cash": 0.0,
    "projection_months": 12,
    "margin_percent": 0.0,
    "fixed_costs": 0.0,
    "variable_costs": 0.0,
    "source_module": None,
    "last_updated": None
}


def initialize_financial_state():
    """Initialize shared financial state if not present"""
    if "core_financials" not in st.session_state:
        st.session_state.core_financials = CORE_FINANCIAL_FIELDS.copy()


def get_core_financials():
    """
    Get the shared financial state object
    
    Returns:
        dict with core financial values
    """
    initialize_financial_state()
    return st.session_state.core_financials


def get_core_financial(key, default=None):
    """
    Get a single financial value from shared state
    
    Args:
        key: Field name to retrieve
        default: Default value if key not found
    
    Returns:
        Value from shared state or default
    """
    initialize_financial_state()
    return st.session_state.core_financials.get(key, default)


def update_core_financial(key, value, source=None):
    """
    Update a single financial value in shared state
    
    Args:
        key: Field name to update
        value: New value
        source: Module name that made the update (optional)
    """
    initialize_financial_state()
    
    st.session_state.core_financials[key] = value
    
    if source:
        st.session_state.core_financials["source_module"] = source
        st.session_state.core_financials["last_updated"] = key
    
    recalculate_derived_financials()


def update_core_financials(data, source=None):
    """
    Update multiple financial values in shared state
    
    Args:
        data: Dictionary of key-value pairs to update
        source: Module name that made the update (optional)
    """
    initialize_financial_state()
    
    for key, value in data.items():
        if key in st.session_state.core_financials:
            st.session_state.core_financials[key] = value
    
    if source:
        st.session_state.core_financials["source_module"] = source
        st.session_state.core_financials["last_updated"] = "bulk_update"
    
    recalculate_derived_financials()


def recalculate_derived_financials():
    """
    Recalculate derived financial values based on core inputs
    Ensures consistency across modules
    """
    initialize_financial_state()
    
    core = st.session_state.core_financials
    
    revenue = core.get("revenue", 0)
    expenses = core.get("expenses", 0)
    
    if revenue > 0 and expenses > 0:
        core["profit"] = revenue - expenses
        core["margin_percent"] = (core["profit"] / revenue * 100) if revenue > 0 else 0
    elif revenue > 0 or expenses > 0:
        core["profit"] = revenue - expenses
        core["margin_percent"] = (core["profit"] / revenue * 100) if revenue > 0 else 0


def sync_from_lite(fm_inputs):
    """
    Sync shared state from Financial Modeler Lite inputs
    
    Args:
        fm_inputs: Dictionary from FM Lite session state
    """
    if not fm_inputs:
        return
    
    monthly_revenue = fm_inputs.get("monthly_revenue", 0)
    cogs_percent = fm_inputs.get("cogs_percent", 0)
    fixed_costs = fm_inputs.get("fixed_costs", 0)
    variable_costs_percent = fm_inputs.get("variable_costs_percent", 0)
    
    cogs = monthly_revenue * cogs_percent
    variable_costs = monthly_revenue * variable_costs_percent
    total_expenses = cogs + fixed_costs + variable_costs
    
    update_data = {
        "revenue": monthly_revenue,
        "expenses": total_expenses,
        "profit": monthly_revenue - total_expenses,
        "growth_rate": fm_inputs.get("revenue_growth", 0),
        "projection_months": fm_inputs.get("projection_months", 12),
        "fixed_costs": fixed_costs,
        "variable_costs": cogs + variable_costs
    }
    
    update_core_financials(update_data, source="financial_modeler_lite")


def sync_from_pro(pro_streams, pro_costs, pro_labor, pro_assumptions):
    """
    Sync shared state from Financial Modeler Pro inputs
    
    Args:
        pro_streams: Revenue streams list
        pro_costs: Cost structure dict
        pro_labor: Labor/payroll dict
        pro_assumptions: Projection assumptions dict
    """
    if not pro_streams:
        return
    
    total_revenue = sum(stream.get("monthly_revenue", 0) for stream in pro_streams)
    
    cogs = total_revenue * pro_costs.get("cogs_percent", 0)
    other_variable = total_revenue * pro_costs.get("other_variable_percent", 0)
    total_variable = cogs + other_variable
    
    total_fixed = pro_costs.get("total_fixed", 0)
    total_payroll = pro_labor.get("total_payroll", 0)
    
    total_expenses = total_variable + total_fixed + total_payroll
    
    avg_growth = sum(stream.get("growth", 0) for stream in pro_streams) / len(pro_streams) if pro_streams else 0
    
    update_data = {
        "revenue": total_revenue,
        "expenses": total_expenses,
        "profit": total_revenue - total_expenses,
        "payroll": total_payroll,
        "growth_rate": avg_growth,
        "projection_months": pro_assumptions.get("projection_months", 12),
        "fixed_costs": total_fixed,
        "variable_costs": total_variable
    }
    
    update_core_financials(update_data, source="financial_modeler_pro")


def get_sync_status():
    """
    Get information about current sync state
    
    Returns:
        dict with sync status information
    """
    initialize_financial_state()
    
    core = st.session_state.core_financials
    
    has_data = core.get("revenue", 0) > 0 or core.get("expenses", 0) > 0
    source = core.get("source_module", None)
    
    return {
        "has_data": has_data,
        "source_module": source,
        "last_updated": core.get("last_updated", None),
        "is_synced": has_data and source is not None
    }


def clear_financial_state():
    """Clear the shared financial state (reset)"""
    if "core_financials" in st.session_state:
        st.session_state.core_financials = CORE_FINANCIAL_FIELDS.copy()


def get_financial_summary():
    """
    Get a formatted summary of current financial state
    
    Returns:
        dict with formatted summary values
    """
    core = get_core_financials()
    
    return {
        "revenue": f"${core['revenue']:,.0f}",
        "expenses": f"${core['expenses']:,.0f}",
        "profit": f"${core['profit']:,.0f}",
        "margin": f"{core['margin_percent']:.1f}%",
        "growth_rate": f"{core['growth_rate']*100:.1f}%",
        "payroll": f"${core['payroll']:,.0f}",
        "starting_cash": f"${core['starting_cash']:,.0f}",
        "projection_months": core['projection_months'],
        "source": core['source_module'] or "Not set"
    }


def validate_financial_state():
    """
    Validate that financial state values are reasonable
    
    Returns:
        tuple (is_valid, list of warnings)
    """
    core = get_core_financials()
    warnings = []
    
    if core["revenue"] < 0:
        warnings.append("Revenue cannot be negative")
    
    if core["expenses"] < 0:
        warnings.append("Expenses cannot be negative")
    
    if core["revenue"] > 0 and core["expenses"] > core["revenue"] * 2:
        warnings.append("Expenses exceed 2x revenue - verify inputs")
    
    if core["payroll"] > core["expenses"]:
        warnings.append("Payroll exceeds total expenses - check cost structure")
    
    if core["growth_rate"] > 0.5:
        warnings.append("Growth rate exceeds 50%/month - verify assumption")
    
    if core["growth_rate"] < -0.5:
        warnings.append("Growth rate below -50%/month - verify assumption")
    
    is_valid = len(warnings) == 0
    
    return is_valid, warnings


def has_financial_data():
    """
    Check if shared financial state has meaningful data
    
    Returns:
        bool indicating if financial data exists
    """
    core = get_core_financials()
    return core.get("revenue", 0) > 0 or core.get("expenses", 0) > 0
