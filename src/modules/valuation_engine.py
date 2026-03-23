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
    calculate_valuation_readiness_score,
    evaluate_unlock_conditions,
    is_method_available,
    calculate_primary_valuation,
    calculate_revenue_multiple_valuation,
    calculate_earnings_multiple_valuation,
    calculate_weighted_valuation,
    calculate_scenario_valuation,
    generate_valuation_insights,
    generate_unlock_guidance,
    get_value_drivers,
    get_method_status,
    get_method_status_detailed
)
from src.modules.valuation_distribution import (
    collect_valuation_methods,
    calculate_distribution_stats,
    generate_distribution_curve,
    calculate_confidence_intervals,
    calculate_variability_level,
    generate_distribution_summary
)
from src.modules.valuation_distribution_chart import (
    create_distribution_chart,
    create_confidence_summary_chart,
    create_method_comparison_chart
)
from src.ui.ui_guidance import show_contextual_help, show_smart_prompt_high_variability, is_guidance_enabled


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
    readiness_score = calculate_valuation_readiness_score(core)
    
    render_readiness_section(readiness_score, core)
    
    st.divider()
    
    render_primary_valuation_section(core)
    
    st.divider()
    
    render_method_breakdown_panel_enhanced(core)
    
    st.divider()
    
    render_unlock_guidance_section(core)
    
    st.divider()
    
    render_scenario_section(core)
    
    st.divider()
    
    render_insights_section(core)
    
    st.divider()
    
    render_value_drivers_section()
    
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


def render_readiness_section(readiness_score, core):
    """Render valuation readiness with progress tracking"""
    
    st.markdown("### 📊 Valuation Readiness")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.progress(readiness_score / 100)
    
    with col2:
        st.metric("Readiness", f"{readiness_score:.0f}%")
    
    with col3:
        conditions = evaluate_unlock_conditions(core)
        unlocked_count = sum([conditions["revenue"], conditions["profit"]])
        st.metric("Methods", f"{unlocked_count}/2")
    
    if readiness_score < 100:
        st.caption("💡 Improve financial metrics to unlock advanced valuation methods")
    else:
        st.success("✅ All core valuation methods unlocked!")


def render_primary_valuation_section(core):
    """Render the primary valuation estimate with distribution curve"""
    
    st.markdown("### 💰 Estimated Business Value Distribution")
    
    # Collect all valuation methods
    methods = collect_valuation_methods(core)
    
    if not methods:
        st.warning("⚠️ Insufficient data for valuation. Complete Financial Modeler inputs.")
        return
    
    # Calculate distribution statistics
    stats = calculate_distribution_stats(methods)
    
    if not stats:
        st.warning("⚠️ Unable to calculate valuation distribution.")
        return
    
    # Calculate confidence intervals
    confidence_intervals = calculate_confidence_intervals(stats["mean"], stats["std_dev"])
    
    # Calculate variability level
    variability = calculate_variability_level(stats["std_dev"], stats["mean"])
    
    # Generate distribution summary
    summary = generate_distribution_summary(stats, confidence_intervals, variability)
    
    # Display primary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean Valuation", f"${stats['mean']:,.0f}")
    
    with col2:
        st.metric("Std Deviation", f"${stats['std_dev']:,.0f}")
    
    with col3:
        ci_68 = confidence_intervals["ci_68"]
        st.metric("68% Range", f"${ci_68['low']:,.0f} - ${ci_68['high']:,.0f}")
    
    with col4:
        st.metric("Variability", f"{variability['icon']} {variability['level']}")
    
    # Show variability message
    if variability["level"] == "High":
        st.warning(f"⚠️ {variability['message']}")
        if is_guidance_enabled():
            show_smart_prompt_high_variability()
    elif variability["level"] == "Moderate":
        st.info(f"ℹ️ {variability['message']}")
    else:
        st.success(f"✅ {variability['message']}")
    
    st.divider()
    
    # Generate and display distribution curve
    x_values, y_values = generate_distribution_curve(stats["mean"], stats["std_dev"])
    
    fig = create_distribution_chart(stats, confidence_intervals, methods, x_values, y_values)
    st.plotly_chart(fig, use_container_width=True)
    
    if is_guidance_enabled():
        st.caption("📊 *Distribution curve shows probability density of valuation. Shaded areas represent confidence intervals: darker = higher confidence.*")
    else:
        st.caption("📊 *Distribution curve shows probability density of valuation.*")
    
    st.divider()
    
    # Display confidence intervals summary
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("#### 68% Confidence Range")
        st.markdown(f"**Low:** ${ci_68['low']:,.0f}")
        st.markdown(f"**Mid:** ${stats['mean']:,.0f}")
        st.markdown(f"**High:** ${ci_68['high']:,.0f}")
        st.caption("*68% probability the true value falls in this range*")
    
    with col6:
        ci_95 = confidence_intervals["ci_95"]
        st.markdown("#### 95% Confidence Range")
        st.markdown(f"**Low:** ${ci_95['low']:,.0f}")
        st.markdown(f"**Mid:** ${stats['mean']:,.0f}")
        st.markdown(f"**High:** ${ci_95['high']:,.0f}")
        st.caption("*95% probability the true value falls in this range*")
    
    st.divider()
    
    # Method comparison chart
    if len(methods) > 1:
        fig_comparison = create_method_comparison_chart(methods)
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.caption("⚠️ *These are estimated ranges, not certified valuations. Actual value depends on market conditions, growth potential, and buyer perspective.*")
    
    # Store for downstream use (use 95% CI as range)
    st.session_state["valuation_range"] = (ci_95["low"], ci_95["high"])
    st.session_state["valuation_distribution"] = {
        "mean": stats["mean"],
        "std_dev": stats["std_dev"],
        "confidence_68": confidence_intervals["ci_68"],
        "confidence_95": confidence_intervals["ci_95"],
        "variability": variability,
        "methods": methods,
    }


def render_method_breakdown_panel_enhanced(core):
    """Render enhanced method availability with unlock conditions"""
    
    st.markdown("### 🔍 Valuation Method Status")
    
    method_status = get_method_status_detailed(core)
    
    for method_name, details in method_status.items():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if details["available"]:
                    st.markdown(f"**{method_name}** {details['icon']}")
                else:
                    st.markdown(f"{method_name} {details['icon']}")
                st.caption(details["description"])
                
                if details["conditions"]:
                    for condition in details["conditions"]:
                        if condition["met"]:
                            st.caption(f"   ✔ {condition['label']}")
                        else:
                            st.caption(f"   ❌ {condition['label']}")
            
            with col2:
                if details["available"]:
                    st.success("Available")
                elif method_name in ["DCF", "Industry Comps"]:
                    st.info("Future")
                else:
                    st.warning("Locked")
            
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


def render_unlock_guidance_section(core):
    """Render actionable guidance for unlocking valuation methods"""
    
    st.markdown("### 👉 How to Improve Your Valuation")
    
    guidance = generate_unlock_guidance(core)
    
    if guidance:
        for guide_item in guidance:
            if guide_item.startswith("**"):
                st.markdown(guide_item)
            else:
                st.markdown(guide_item)
    else:
        st.success("✅ All valuation methods unlocked - focus on scaling!")
    
    st.caption("💡 *These recommendations help unlock advanced valuation methods and improve your business value*")


def render_integration_hook(core):
    """Render integration hook for downstream modules"""
    
    st.markdown("### 🔗 Use This Valuation")
    
    if "valuation_range" in st.session_state:
        low, high = st.session_state["valuation_range"]
        
        st.info(f"💡 **Valuation stored:** ${low:,.0f} - ${high:,.0f}")
        st.caption("This valuation can be used in Funding Strategy and other modules")
    else:
        st.caption("Valuation will be available for use in downstream modules once calculated")
