"""
North Star Unified Shell - Valuation Engine UI Module
Progressive unlock valuation interface with guided experience
"""
import streamlit as st
from src.modules.valuation_logic import (
    calculate_completion_score,
    calculate_revenue_multiple,
    calculate_earnings_multiple,
    calculate_weighted_value,
    get_available_methods,
    get_locked_methods,
    generate_valuation_insights,
    get_value_drivers,
    get_unlock_guidance,
    VALUATION_TIERS
)


def render_valuation_engine():
    """Main render function for the Valuation Engine tab"""
    
    st.markdown("## 💎 Business Valuation Engine")
    st.markdown("*Progressive valuation system - unlock advanced methods as you complete inputs*")
    st.divider()
    
    valuation_data = extract_valuation_data()
    
    completion_score = calculate_completion_score(valuation_data)
    
    render_progress_section(completion_score)
    
    st.divider()
    
    render_method_availability_panel(valuation_data)
    
    st.divider()
    
    valuations = calculate_valuations(valuation_data)
    
    if valuations:
        render_valuation_results(valuations)
        
        st.divider()
        
        render_insights_section(valuation_data, valuations)
        
        st.divider()
        
        render_value_drivers_section()
    else:
        render_no_data_message()


def extract_valuation_data():
    """Extract valuation data from Financial Modeler inputs"""
    
    if "fm_inputs" not in st.session_state or not st.session_state.fm_inputs:
        return {}
    
    inputs = st.session_state.fm_inputs
    
    revenue = inputs.get("monthly_revenue", 0)
    
    if revenue and revenue > 0:
        cogs = revenue * inputs.get("cogs_percent", 0)
        fixed_costs = inputs.get("fixed_costs", 0)
        variable_costs = revenue * inputs.get("variable_costs_percent", 0)
        
        expenses = cogs + fixed_costs + variable_costs
        profit = revenue - expenses
    else:
        expenses = 0
        profit = 0
    
    return {
        "revenue": revenue if revenue > 0 else None,
        "expenses": expenses if expenses > 0 else None,
        "profit": profit if profit != 0 else None
    }


def render_progress_section(completion_score):
    """Render the valuation readiness progress section"""
    
    st.markdown("### 📊 Valuation Readiness")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.progress(completion_score / 100)
    
    with col2:
        st.metric("Readiness", f"{completion_score}%")
    
    if completion_score < 100:
        st.caption("💡 Complete more inputs in the **Model Inputs** tab to unlock additional valuation methods")
    else:
        st.caption("✅ All basic inputs complete - full valuation methods available")


def render_method_availability_panel(data):
    """Render the method availability status panel"""
    
    st.markdown("### 🔓 Available Valuation Methods")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("**Method**")
    with col2:
        st.markdown("**Status**")
    
    st.markdown("---")
    
    for method_key, tier in VALUATION_TIERS.items():
        col1, col2 = st.columns([3, 1])
        
        is_unlocked = tier.is_unlocked(data)
        
        with col1:
            if is_unlocked:
                st.markdown(f"**{tier.name}**")
                st.caption(tier.description)
            else:
                st.markdown(f"{tier.name}")
                st.caption(tier.description)
        
        with col2:
            if method_key in ["revenue_multiple", "earnings_multiple"]:
                if is_unlocked:
                    st.success(f"{tier.icon_unlocked} Available")
                else:
                    st.warning(f"{tier.icon_locked} Locked")
            else:
                st.info(f"{tier.icon_locked} Coming Soon")
        
        if not is_unlocked and method_key in ["revenue_multiple", "earnings_multiple"]:
            missing = [field for field in tier.required_fields 
                      if field not in data or data[field] is None or data[field] == 0]
            guidance = get_unlock_guidance(missing)
            st.caption(f"🔑 {guidance}")
        
        st.markdown("")


def calculate_valuations(data):
    """Calculate all available valuations based on data"""
    
    valuations = []
    
    if data.get("revenue") and data["revenue"] > 0:
        revenue_val = calculate_revenue_multiple(data["revenue"])
        valuations.append(revenue_val)
    
    if data.get("profit") and data["profit"] != 0:
        earnings_val = calculate_earnings_multiple(data["profit"])
        valuations.append(earnings_val)
    
    return valuations


def render_valuation_results(valuations):
    """Render the valuation results section"""
    
    st.markdown("### 💰 Estimated Business Value")
    
    if len(valuations) == 1:
        val = valuations[0]
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.metric("Low Estimate", f"${val['low']:,.0f}")
        
        with col2:
            st.metric("High Estimate", f"${val['high']:,.0f}")
        
        with col3:
            st.caption(f"**Method:**\n{val['method']}")
            st.caption(f"**Multiple:**\n{val['multiple_range']}")
        
        midpoint = (val['low'] + val['high']) / 2
        st.info(f"💡 **Midpoint Estimate:** ${midpoint:,.0f}")
        
    else:
        for idx, val in enumerate(valuations):
            with st.expander(f"📊 {val['method']} Valuation", expanded=(idx == 0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Low Estimate", f"${val['low']:,.0f}")
                
                with col2:
                    st.metric("High Estimate", f"${val['high']:,.0f}")
                
                st.caption(f"Multiple Range: {val['multiple_range']}")
                
                midpoint = (val['low'] + val['high']) / 2
                st.info(f"Midpoint: ${midpoint:,.0f}")
        
        all_lows = [v['low'] for v in valuations]
        all_highs = [v['high'] for v in valuations]
        
        st.markdown("#### 🎯 Combined Range")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Overall Low", f"${min(all_lows):,.0f}")
        
        with col2:
            st.metric("Overall High", f"${max(all_highs):,.0f}")
        
        avg_midpoint = sum([(v['low'] + v['high']) / 2 for v in valuations]) / len(valuations)
        st.success(f"✨ **Average Valuation:** ${avg_midpoint:,.0f}")
    
    st.caption("⚠️ *These are estimated ranges, not certified valuations. Actual value depends on many factors including market conditions, growth potential, and buyer perspective.*")


def render_insights_section(data, valuations):
    """Render the insights and recommendations section"""
    
    st.markdown("### 💡 Valuation Insights")
    
    insights = generate_valuation_insights(data, valuations)
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.caption("Complete more inputs to generate insights")
    
    if data.get("profit") and data.get("revenue"):
        profit_margin = (data["profit"] / data["revenue"]) * 100
        
        st.markdown("#### 📈 Margin Impact Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Current Margin", f"{profit_margin:.1f}%")
        
        with col2:
            if profit_margin > 0:
                improved_margin = profit_margin + 5
                improved_profit = data["revenue"] * (improved_margin / 100)
                improved_val = calculate_earnings_multiple(improved_profit)
                current_val = calculate_earnings_multiple(data["profit"])
                
                value_increase = ((improved_val["high"] - current_val["high"]) / current_val["high"]) * 100
                
                st.metric(
                    "Value Impact of +5% Margin",
                    f"+{value_increase:.1f}%",
                    delta=f"${improved_val['high'] - current_val['high']:,.0f}"
                )


def render_value_drivers_section():
    """Render the value drivers education section"""
    
    st.markdown("### 🎯 Key Value Drivers")
    
    drivers = get_value_drivers()
    
    for driver in drivers:
        st.markdown(driver)
    
    st.divider()
    
    st.markdown("#### 🚀 Increase Your Business Value")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Short-term Actions:**
        - Optimize pricing strategy
        - Reduce unnecessary expenses
        - Improve operational efficiency
        - Focus on high-margin products/services
        """)
    
    with col2:
        st.markdown("""
        **Long-term Strategies:**
        - Build recurring revenue streams
        - Develop scalable systems
        - Strengthen market position
        - Document processes and IP
        """)


def render_no_data_message():
    """Render message when no valuation data is available"""
    
    st.info("👈 **Get Started:** Complete the inputs in the **Model Inputs** tab to calculate your business valuation")
    
    st.markdown("### 🎯 What You'll Get")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Valuation Methods:**
        - Revenue Multiple (1.5x - 4.0x)
        - Earnings Multiple (3x - 6x)
        - Combined weighted analysis
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
    
    with st.expander("🎯 Progressive Unlock System"):
        st.markdown("""
        **How it works:** More data = more valuation methods
        
        **Basic inputs** → Revenue Multiple available
        
        **Complete inputs** → Earnings Multiple unlocked
        
        **Full data** → Advanced methods (coming soon)
        
        This ensures you get accurate valuations based on available information.
        """)
