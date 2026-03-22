"""
North Star Unified Shell - Insights Engine Module
Cross-module intelligence and recommendations
"""
import streamlit as st
from src.state.financial_state import get_core_financials
from src.modules.insights_logic import (
    generate_financial_insights,
    generate_valuation_insights,
    generate_loc_insights,
    generate_project_insights,
    generate_idea_insights,
    generate_cross_module_insights,
    categorize_insights,
    generate_summary_takeaways,
    generate_recommended_actions,
    check_data_availability
)


def render_insights_engine():
    """Main render function for Insights Engine module"""
    
    st.markdown("## 🧠 Insights Engine")
    st.markdown("*Cross-module intelligence and strategic recommendations*")
    st.caption("🔄 Synced with all module states")
    st.divider()
    
    # Gather data from all modules
    core_financials = get_core_financials()
    valuation_range = st.session_state.get("valuation_range")
    loc_data = st.session_state.get("loc_recommendation")
    project_eval = st.session_state.get("project_evaluation")
    idea_context = st.session_state.get("idea_context")
    
    # Check data availability
    availability = check_data_availability(
        core_financials,
        valuation_range,
        loc_data,
        project_eval,
        idea_context
    )
    
    if not availability["any_data"]:
        render_no_data_state()
        return
    
    # Generate all insights
    all_insights = []
    
    if availability["financial"]:
        all_insights.extend(generate_financial_insights(core_financials))
    
    if availability["valuation"]:
        all_insights.extend(generate_valuation_insights(valuation_range, core_financials))
    
    if availability["loc"]:
        all_insights.extend(generate_loc_insights(loc_data, core_financials))
    
    if availability["project"]:
        all_insights.extend(generate_project_insights(project_eval))
    
    if availability["idea"]:
        all_insights.extend(generate_idea_insights(idea_context))
    
    # Cross-module insights
    all_insights.extend(generate_cross_module_insights(
        core_financials,
        valuation_range,
        loc_data,
        project_eval,
        idea_context
    ))
    
    # Categorize insights
    categorized = categorize_insights(all_insights)
    
    # Generate summary and actions
    takeaways = generate_summary_takeaways(categorized, core_financials)
    actions = generate_recommended_actions(
        categorized,
        core_financials,
        valuation_range,
        loc_data,
        project_eval
    )
    
    # Render UI
    render_data_sources(availability)
    
    st.divider()
    
    render_key_takeaways(takeaways)
    
    st.divider()
    
    render_categorized_insights(categorized)
    
    st.divider()
    
    render_recommended_actions_section(actions)


def render_no_data_state():
    """Render state when no data is available"""
    
    st.info("👈 **Get Started:** Complete modules to unlock cross-platform insights")
    
    st.markdown("### 🎯 What You'll Get")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Insights From:**
        - 📊 Financial Model (margins, growth, costs)
        - 💎 Business Valuation (value drivers)
        - 💳 LOC Analyzer (cash flow, liquidity)
        """)
    
    with col2:
        st.markdown("""
        **Strategic Guidance:**
        - 🎯 Project prioritization
        - 💡 Idea viability assessment
        - 🏦 Funding readiness signals
        - 📈 Growth opportunities
        """)
    
    st.divider()
    
    st.markdown("### 🧠 How It Works")
    
    st.markdown("""
    The Insights Engine reads data from all major modules and generates:
    
    1. **Key Takeaways** - Top 3-5 most important observations
    2. **Categorized Insights** - Organized by Financial, Valuation, Cash Flow, Funding, and Strategy
    3. **Recommended Actions** - Clear next steps based on your data
    
    Complete any of the following modules to start generating insights:
    - Financial Modeler Lite or Pro
    - Business Valuation
    - LOC Analyzer
    - Project Evaluator
    - Idea Screener
    """)


def render_data_sources(availability):
    """Render data source indicators"""
    
    st.markdown("### 📊 Data Sources")
    
    cols = st.columns(5)
    
    sources = [
        ("financial", "💰 Financial", "Financial Model"),
        ("valuation", "💎 Valuation", "Business Valuation"),
        ("loc", "💳 LOC", "LOC Analyzer"),
        ("project", "🎯 Project", "Project Evaluator"),
        ("idea", "💡 Idea", "Idea Screener")
    ]
    
    for idx, (key, icon, name) in enumerate(sources):
        with cols[idx]:
            if availability[key]:
                st.success(f"{icon}")
                st.caption(name)
            else:
                st.caption(f"{icon}")
                st.caption(f"~~{name}~~")


def render_key_takeaways(takeaways):
    """Render key takeaways section"""
    
    st.markdown("### 🎯 Key Takeaways")
    
    if not takeaways:
        st.caption("No takeaways available yet")
        return
    
    for takeaway in takeaways:
        st.markdown(f"- {takeaway}")


def render_categorized_insights(categorized):
    """Render insights organized by category"""
    
    st.markdown("### 💡 Platform Insights")
    
    categories_config = [
        ("financial", "📊 Financial Health", "Financial performance and metrics"),
        ("valuation", "💎 Value Insights", "Business valuation and value drivers"),
        ("cash_flow", "💳 Cash Flow & Liquidity", "Working capital and cash management"),
        ("funding", "🏦 Funding Readiness", "Financing eligibility and opportunities"),
        ("strategy", "🎯 Strategic Direction", "Projects, ideas, and priorities")
    ]
    
    for category_key, title, description in categories_config:
        insights = categorized.get(category_key, [])
        
        if insights:
            with st.expander(f"{title}", expanded=True):
                st.caption(description)
                st.markdown("")
                
                for insight, priority in insights:
                    if priority == "high":
                        st.warning(insight)
                    elif priority == "positive":
                        st.success(insight)
                    else:
                        st.info(insight)


def render_recommended_actions_section(actions):
    """Render recommended actions section"""
    
    st.markdown("### 🚀 Recommended Next Steps")
    
    if not actions:
        st.caption("Complete more modules to unlock action recommendations")
        return
    
    st.markdown("Based on your current data, consider these actions:")
    st.markdown("")
    
    for action in actions:
        st.markdown(f"- {action}")
    
    st.markdown("")
    
    # Quick navigation
    st.markdown("#### Quick Navigation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Financial Modeler", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Lite"
            st.rerun()
    
    with col2:
        if st.button("💎 Business Valuation", use_container_width=True):
            st.session_state["active_module"] = "Business Valuation"
            st.rerun()
    
    with col3:
        if st.button("💳 LOC Analyzer", use_container_width=True):
            st.session_state["active_module"] = "LOC Analyzer"
            st.rerun()
