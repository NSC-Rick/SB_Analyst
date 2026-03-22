"""
North Star Unified Shell - Entity Assistant Module
Business entity structure and setup advisor
"""
import streamlit as st
from src.modules.entity_logic import (
    get_entity_recommendation,
    get_entity_comparison,
    get_next_steps,
    get_tax_implications,
    create_entity_context
)


def render_entity_assistant():
    """Main render function for Entity Assistant module"""
    
    st.markdown("## 🏛️ Entity Assistant")
    st.markdown("*Choose the right business structure for your venture*")
    st.divider()
    
    # Check if we have results to show
    if "entity_assistant_results" in st.session_state and st.session_state.entity_assistant_results:
        render_results_view()
    else:
        render_input_view()


def render_input_view():
    """Render the input form for entity selection"""
    
    st.markdown("### Business Profile")
    
    # Check for Idea Screener context
    idea_context = st.session_state.get("idea_context", {})
    if idea_context:
        st.info(f"💡 **Idea Context Detected:** {idea_context.get('idea_title', 'Your Business Idea')}")
    
    st.divider()
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue & Growth")
        
        revenue = st.number_input(
            "Expected Annual Revenue (Year 1)",
            min_value=0,
            max_value=10000000,
            value=50000,
            step=10000,
            help="Your projected first-year revenue"
        )
        
        growth_ambition = st.selectbox(
            "Growth Ambition",
            options=["lifestyle", "scalable", "high-growth"],
            format_func=lambda x: {
                "lifestyle": "Lifestyle Business (Steady income)",
                "scalable": "Scalable Growth (Moderate expansion)",
                "high-growth": "High Growth (Rapid scaling)"
            }[x],
            help="Your long-term growth goals"
        )
        
        investor_intent = st.checkbox(
            "Planning to seek investors or venture capital",
            help="Will you raise money from outside investors?"
        )
    
    with col2:
        st.markdown("#### Risk & Operations")
        
        risk_level = st.selectbox(
            "Business Risk Level",
            options=["low", "medium", "high"],
            format_func=lambda x: {
                "low": "Low Risk (Service-based, minimal liability)",
                "medium": "Medium Risk (Standard business operations)",
                "high": "High Risk (Product liability, regulatory exposure)"
            }[x],
            index=1,
            help="Level of potential liability and risk"
        )
        
        hiring_plans = st.checkbox(
            "Planning to hire employees within 12 months",
            help="Will you have employees or contractors?"
        )
    
    st.divider()
    
    # Education Section
    with st.expander("📚 Learn About Entity Types", expanded=False):
        render_entity_comparison_table()
    
    st.divider()
    
    # Submit Button
    if st.button("🔍 Get Entity Recommendation", type="primary", use_container_width=True):
        inputs = {
            "revenue": revenue,
            "risk_level": risk_level,
            "hiring_plans": hiring_plans,
            "investor_intent": investor_intent,
            "growth_ambition": growth_ambition
        }
        
        # Get recommendation
        recommendation = get_entity_recommendation(inputs)
        
        # Create entity context
        entity_context = create_entity_context(inputs, recommendation)
        
        # Store in session state
        st.session_state["entity_structure"] = entity_context
        st.session_state["entity_assistant_results"] = True
        
        st.rerun()


def render_results_view():
    """Render the results view after recommendation"""
    
    entity_context = st.session_state.get("entity_structure", {})
    
    if not entity_context:
        st.session_state["entity_assistant_results"] = False
        st.rerun()
        return
    
    entity = entity_context["entity_type"]
    reasoning = entity_context["recommendation_reasoning"]
    considerations = entity_context["considerations"]
    revenue = entity_context["revenue_expectation"]
    
    # Header
    st.success(f"### ✅ Recommended Entity: **{entity}**")
    
    st.divider()
    
    # Main Recommendation Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Why This Structure")
        for reason in reasoning:
            st.markdown(f"- {reason}")
    
    with col2:
        st.markdown("### 📊 Your Profile")
        st.metric("Expected Revenue", f"${revenue:,}")
        st.caption(f"Risk: {entity_context['risk_level'].title()}")
        st.caption(f"Growth: {entity_context['growth_ambition'].replace('-', ' ').title()}")
        if entity_context['investor_intent']:
            st.caption("🎯 Seeking investors")
        if entity_context['hiring_plans']:
            st.caption("👥 Hiring planned")
    
    st.divider()
    
    # Considerations
    st.markdown("### ⚠️ Important Considerations")
    for consideration in considerations:
        st.warning(f"• {consideration}")
    
    st.divider()
    
    # Tax Implications
    render_tax_section(entity, revenue)
    
    st.divider()
    
    # Next Steps
    render_next_steps_section(entity)
    
    st.divider()
    
    # Entity Comparison
    with st.expander("📊 Compare All Entity Types", expanded=False):
        render_entity_comparison_table()
    
    st.divider()
    
    # Navigation
    render_navigation_section()


def render_entity_comparison_table():
    """Render comparison table of all entity types"""
    
    comparison = get_entity_comparison()
    
    for entity_type, details in comparison.items():
        with st.container():
            st.markdown(f"**{entity_type}**")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.caption(f"**Liability:** {details['liability']}")
                st.caption(f"**Complexity:** {details['complexity']}")
            
            with col2:
                st.caption(f"**Taxation:** {details['taxation']}")
                st.caption(f"**Cost:** {details['cost']}")
            
            st.caption(f"**Best For:** {details['best_for']}")
            st.markdown("")


def render_tax_section(entity, revenue):
    """Render tax implications section"""
    
    st.markdown("### 💰 Tax Implications")
    
    tax_info = get_tax_implications(entity, revenue)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Federal Filing:**")
        st.info(tax_info["federal"])
        
        st.markdown("**Self-Employment Tax:**")
        st.info(tax_info["self_employment"])
    
    with col2:
        st.markdown("**Estimated Taxes:**")
        st.info(tax_info["estimated_taxes"])
        
        st.markdown("**Tax Savings Opportunity:**")
        st.success(tax_info["savings_opportunity"])
    
    st.caption("💡 *Consult with a tax professional for personalized advice*")


def render_next_steps_section(entity):
    """Render actionable next steps"""
    
    st.markdown("### 📋 Next Steps to Form Your Entity")
    
    steps = get_next_steps(entity)
    
    for step in steps:
        st.markdown(f"**{step}**")
    
    st.info("💡 **Pro Tip:** Consider using a formation service like LegalZoom, Incfile, or consult a business attorney for complex situations.")


def render_navigation_section():
    """Render navigation options"""
    
    st.markdown("### 🚀 Continue Your Journey")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Try Different Inputs", use_container_width=True):
            st.session_state["entity_assistant_results"] = False
            st.rerun()
    
    with col2:
        if st.button("📊 Financial Modeler Lite", type="primary", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Lite"
            st.rerun()
    
    with col3:
        if st.button("💎 Financial Modeler Pro", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Pro"
            st.rerun()
    
    st.caption("💡 Your entity structure is saved and will be available in other modules")
