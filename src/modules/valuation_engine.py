"""
North Star Unified Shell - Business Valuation Engine
Standalone intelligence module with multi-method valuation
"""
import streamlit as st
from src.state.financial_state import (
    get_core_financials,
    has_financial_data,
    get_sync_status
)
from src.modules.valuation_logic import (
    calculate_valuation_completeness,
    is_method_available,
    calculate_primary_valuation,
    calculate_revenue_multiple_valuation,
    calculate_earnings_multiple_valuation,
    calculate_weighted_valuation,
    calculate_scenario_valuation,
    generate_valuation_insights,
    get_value_drivers,
    get_method_status
)


def render_business_valuation():
    """Main render function for Business Valuation Engine"""
    
    st.markdown("## 💎 Business Valuation Engine")
    st.markdown("*Multi-method valuation using shared financial intelligence*")
    st.divider()
    
    if not has_financial_data():
        render_no_data_state()
        return
    
    core = get_core_financials()
    sync_status = get_sync_status()
    
    if sync_status["has_data"]:
        source = sync_status["source_module"].replace("_", " ").title()
        st.caption(f"📊 *Using financial data from {source}*")
    
    completeness = calculate_valuation_completeness(core)
    
    render_completeness_section(completeness)
    
    st.divider()
    
    render_primary_valuation_section(core)
    
    st.divider()
    
    render_method_breakdown_panel(core)
    
    st.divider()
    
    render_scenario_section(core)
    
    st.divider()
    
    render_value_drivers_section()
    
    st.divider()
    
    render_insights_section(core)
    
    st.divider()
    
    render_integration_hook(core)


def render_no_data_state():
    """Render state when no financial data is available"""
    
    st.info("👈 **Get Started:** Complete a Financial Modeler (Lite or Pro) to calculate your business valuation")
    
    st.markdown("### 🎯 What You'll Get")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Valuation Methods:**
        - Revenue Multiple (1.5x - 4.0x)
        - Earnings Multiple (3x - 6x)
        - Weighted combined analysis
        """)
    
    with col2:
        st.markdown("""
        **Insights:**
        - Value range estimates
        - Margin impact analysis
        - Growth opportunity identification
        - Value driver recommendations
        """)
    
    st.divider()
    
    st.markdown("### 📚 Understanding Business Valuation")
    
    with st.expander("💰 Revenue Multiple Method"):
        st.markdown("""
        **What it is:** Values your business as a multiple of annual revenue
        
        **When to use:** Early-stage businesses, high-growth companies
        
        **Typical range:** 1.5x - 4.0x annual revenue
        
        **Best for:** Businesses with strong revenue but developing profitability
        """)
    
    with st.expander("📊 Earnings Multiple Method"):
        st.markdown("""
        **What it is:** Values your business as a multiple of annual profit/earnings
        
        **When to use:** Profitable businesses with stable margins
        
        **Typical range:** 3x - 6x annual profit
        
        **Best for:** Established businesses with consistent profitability
        """)


def render_completeness_section(completeness):
    """Render valuation completeness progress"""
    
    st.markdown("### 📊 Valuation Completeness")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.progress(completeness / 100)
    
    with col2:
        st.metric("Score", f"{completeness}%")
    
    if completeness < 100:
        st.caption("💡 Complete more financial data to unlock additional valuation methods")
    else:
        st.caption("✅ All inputs complete - full valuation methods available")


def render_primary_valuation_section(core):
    """Render the primary valuation estimate"""
    
    st.markdown("### 💰 Estimated Business Value")
    
    low, high, method = calculate_primary_valuation(core)
    
    if low == 0 and high == 0:
        st.warning("⚠️ Insufficient data for valuation. Complete Financial Modeler inputs.")
        return
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.metric("Low Estimate", f"${low:,.0f}")
    
    with col2:
        st.metric("High Estimate", f"${high:,.0f}")
    
    with col3:
        midpoint = (low + high) / 2
        st.metric("Midpoint", f"${midpoint:,.0f}")
    
    st.success(f"**Primary Method:** {method}")
    
    st.caption("⚠️ *These are estimated ranges, not certified valuations. Actual value depends on market conditions, growth potential, and buyer perspective.*")
    
    # Store for downstream use
    st.session_state["valuation_range"] = (low, high)


def render_method_breakdown_panel(core):
    """Render method availability breakdown"""
    
    st.markdown("### � Valuation Method Status")
    
    method_status = get_method_status(core)
    
    for method_name, (available, icon, description) in method_status.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if available:
                st.markdown(f"**{method_name}**")
            else:
                st.markdown(f"{method_name}")
            st.caption(description)
        
        with col2:
            if available:
                st.success(f"{icon} Available")
            elif method_name in ["DCF", "Industry Comps"]:
                st.info(f"{icon} Future")
            else:
                st.warning(f"{icon} Locked")
        
        st.markdown("")


def render_scenario_section(core):
    """Render scenario valuation with improved margins"""
    
    st.markdown("### 📈 Scenario Valuation")
    
    scenario_result = calculate_scenario_valuation(core)
    
    if scenario_result is None:
        st.info("� Scenario analysis available when business is profitable")
        return
    
    scenario_low, scenario_high = scenario_result
    current_low, current_high, _ = calculate_primary_valuation(core)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Value Range", f"${current_low:,.0f} - ${current_high:,.0f}")
    
    with col2:
        st.metric("Improved Margin Scenario (+20%)", f"${scenario_low:,.0f} - ${scenario_high:,.0f}")
    
    increase = ((scenario_high - current_high) / current_high) * 100
    st.success(f"💰 **Potential Value Increase:** +{increase:.1f}% (${scenario_high - current_high:,.0f})")


def render_insights_section(core):
    """Render insights based on financial data"""
    
    st.markdown("### 💡 Valuation Insights")
    
    insights = generate_valuation_insights(core)
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.caption("Complete more financial data to generate insights")


def render_value_drivers_section():
    """Render the value drivers education section"""
    
    st.markdown("### 🎯 Key Value Drivers")
    
    drivers = get_value_drivers()
    
    for driver in drivers:
        st.markdown(driver)


def render_integration_hook(core):
    """Render integration hook for downstream modules"""
    
    st.markdown("### 🔗 Use This Valuation")
    
    if "valuation_range" in st.session_state:
        low, high = st.session_state["valuation_range"]
        
        st.info(f"💡 **Valuation stored:** ${low:,.0f} - ${high:,.0f}")
        st.caption("This valuation can be used in Funding Strategy and other modules")
    else:
        st.caption("Valuation will be available for use in downstream modules once calculated")
