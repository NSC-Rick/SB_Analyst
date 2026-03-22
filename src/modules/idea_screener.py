"""
North Star Unified Shell - Idea Screener Module
Business concept evaluation and intake module
"""
import streamlit as st
from src.modules.idea_logic import (
    calculate_category_scores,
    calculate_overall_viability,
    classify_viability,
    generate_recommendation,
    identify_strengths,
    identify_watchouts,
    create_idea_context,
    get_category_label,
    get_category_description,
    get_rating_guidance
)


def render_idea_screener():
    """Main render function for Idea Screener module"""
    
    st.markdown("## 💡 Idea Screener")
    st.markdown("*Evaluate a business concept before moving into deeper modeling*")
    st.divider()
    
    # Check if we have results to show
    if "idea_screener_results" in st.session_state and st.session_state.idea_screener_results:
        render_results_view()
    else:
        render_input_view()


def render_input_view():
    """Render the input form for idea evaluation"""
    
    st.markdown("### Business Concept Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        idea_title = st.text_input(
            "Idea Title / Business Name",
            placeholder="e.g., Local Coffee Roastery",
            help="A short, memorable name for your business concept"
        )
        
        target_customer = st.text_input(
            "Target Customer",
            placeholder="e.g., Coffee enthusiasts in urban areas",
            help="Who is your primary customer?"
        )
    
    with col2:
        location = st.text_input(
            "Location / Market Area",
            placeholder="e.g., Downtown Seattle (optional)",
            help="Geographic focus (optional)"
        )
        
        revenue_approach = st.text_input(
            "Revenue Approach",
            placeholder="e.g., Retail sales + wholesale to cafes",
            help="How will the business make money?"
        )
    
    idea_description = st.text_area(
        "Short Description",
        placeholder="Describe your business concept in 2-3 sentences...",
        help="Brief overview of what the business does and how it creates value",
        height=100
    )
    
    st.divider()
    
    st.markdown("### Evaluation Dimensions")
    st.caption("Rate each dimension on a 1-5 scale based on your current understanding")
    
    # Market Opportunity
    render_category_rating(
        "market_opportunity",
        "🎯 Market Opportunity",
        "market_rating"
    )
    
    st.markdown("")
    
    # Revenue Potential
    render_category_rating(
        "revenue_potential",
        "💰 Revenue Potential",
        "revenue_rating"
    )
    
    st.markdown("")
    
    # Cost / Feasibility
    render_category_rating(
        "cost_feasibility",
        "✅ Cost / Feasibility Reality",
        "cost_rating"
    )
    
    st.markdown("")
    
    # Execution Readiness
    render_category_rating(
        "execution_readiness",
        "🚀 Execution Readiness",
        "execution_rating"
    )
    
    st.markdown("")
    
    # Risk Level
    render_category_rating(
        "risk_level",
        "⚠️ Risk Level",
        "risk_rating"
    )
    
    st.divider()
    
    # Evaluate button
    if st.button("🔍 Evaluate Idea", type="primary", use_container_width=True):
        # Collect inputs
        inputs = {
            "idea_title": idea_title,
            "idea_description": idea_description,
            "target_customer": target_customer,
            "location": location,
            "revenue_approach": revenue_approach,
            "market_rating": st.session_state.get("market_rating", 3),
            "revenue_rating": st.session_state.get("revenue_rating", 3),
            "cost_rating": st.session_state.get("cost_rating", 3),
            "execution_rating": st.session_state.get("execution_rating", 3),
            "risk_rating": st.session_state.get("risk_rating", 3)
        }
        
        # Validate required fields
        if not idea_title or not idea_description:
            st.error("⚠️ Please provide at least an idea title and description")
            return
        
        # Calculate scores
        category_scores = calculate_category_scores(inputs)
        overall_score = calculate_overall_viability(category_scores)
        classification = classify_viability(overall_score)
        recommendation = generate_recommendation(overall_score, category_scores, classification)
        strengths = identify_strengths(category_scores)
        watchouts = identify_watchouts(category_scores)
        
        # Create idea context
        idea_context = create_idea_context(
            inputs,
            category_scores,
            overall_score,
            classification,
            recommendation,
            strengths,
            watchouts
        )
        
        # Store in session state
        st.session_state["idea_context"] = idea_context
        st.session_state["idea_screener_results"] = True
        
        st.rerun()


def render_category_rating(category_key, title, session_key):
    """Render a category rating slider with guidance"""
    
    description = get_category_description(category_key)
    guidance = get_rating_guidance(category_key)
    
    with st.expander(f"{title}", expanded=False):
        st.caption(description)
        
        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=3,
            key=session_key,
            help="1 = Weak/Unclear, 3 = Moderate, 5 = Strong/Clear"
        )
        
        # Show guidance for current rating
        if rating in guidance:
            st.caption(f"**{rating}/5:** {guidance[rating]}")


def render_results_view():
    """Render the results view after evaluation"""
    
    idea_context = st.session_state.get("idea_context", {})
    
    if not idea_context:
        st.session_state["idea_screener_results"] = False
        st.rerun()
        return
    
    # Header with idea title
    st.markdown(f"### 📋 Evaluation Results: {idea_context['idea_title']}")
    
    if idea_context.get("idea_description"):
        st.caption(idea_context["idea_description"])
    
    st.divider()
    
    # Overall Viability Score
    render_viability_score(idea_context)
    
    st.divider()
    
    # Category Breakdown
    render_category_breakdown(idea_context)
    
    st.divider()
    
    # Recommendation
    render_recommendation_section(idea_context)
    
    st.divider()
    
    # Strengths and Watchouts
    render_strengths_watchouts(idea_context)
    
    st.divider()
    
    # Next Steps / Handoff
    render_next_steps(idea_context)
    
    st.divider()
    
    # Start Over button
    if st.button("🔄 Evaluate Another Idea", use_container_width=True):
        st.session_state["idea_screener_results"] = False
        # Keep idea_context for potential use in modelers
        st.rerun()


def render_viability_score(idea_context):
    """Render the overall viability score section"""
    
    st.markdown("### 🎯 Overall Viability Score")
    
    score = idea_context["viability_score"]
    classification = idea_context["classification"]
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.metric("Viability Score", f"{score}/100")
    
    with col2:
        st.metric("Classification", classification)
    
    with col3:
        # Visual indicator
        if score >= 70:
            st.success("Strong")
        elif score >= 50:
            st.warning("Promising")
        else:
            st.info("Early Stage")
    
    # Progress bar
    st.progress(score / 100)


def render_category_breakdown(idea_context):
    """Render category scores breakdown"""
    
    st.markdown("### 📊 Category Breakdown")
    
    category_scores = idea_context["category_scores"]
    
    # Create columns for category metrics
    cols = st.columns(5)
    
    categories = [
        ("market_opportunity", "🎯 Market"),
        ("revenue_potential", "💰 Revenue"),
        ("cost_feasibility", "✅ Feasibility"),
        ("execution_readiness", "🚀 Execution"),
        ("risk_level", "⚠️ Risk")
    ]
    
    for idx, (cat_key, cat_label) in enumerate(categories):
        with cols[idx]:
            score = category_scores[cat_key]
            
            # For risk, show inverted score (lower risk = better)
            if cat_key == "risk_level":
                display_score = 100 - score
                st.metric(cat_label, f"{display_score:.0f}")
                st.caption("(lower is better)")
            else:
                st.metric(cat_label, f"{score:.0f}")


def render_recommendation_section(idea_context):
    """Render recommendation section"""
    
    st.markdown("### 💡 Recommendation")
    
    recommendation = idea_context["recommendation"]
    classification = idea_context["classification"]
    
    if classification == "Strong Opportunity":
        st.success(recommendation)
    elif classification == "Promising but Needs Clarification":
        st.warning(recommendation)
    else:
        st.info(recommendation)


def render_strengths_watchouts(idea_context):
    """Render strengths and watchouts"""
    
    strengths = idea_context.get("strengths", [])
    watchouts = idea_context.get("watchouts", [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✨ Strengths")
        
        if strengths:
            for strength in strengths:
                st.markdown(strength)
        else:
            st.caption("Complete evaluation to see strengths")
    
    with col2:
        st.markdown("#### 👀 Watchouts")
        
        if watchouts:
            for watchout in watchouts:
                st.markdown(watchout)
        else:
            st.caption("No significant watchouts identified")


def render_next_steps(idea_context):
    """Render next steps and handoff buttons"""
    
    st.markdown("### 🚀 Next Steps")
    
    classification = idea_context["classification"]
    
    if classification == "Strong Opportunity":
        st.markdown("**Ready to model this concept?** Move into financial modeling to build detailed projections.")
    elif classification == "Promising but Needs Clarification":
        st.markdown("**Refine and model:** Consider clarifying key assumptions, then move into modeling to test viability.")
    else:
        st.markdown("**Strengthen the concept:** Refine core assumptions before detailed modeling, or explore with basic projections.")
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Continue to Financial Modeler Lite", type="primary", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Lite"
            st.rerun()
    
    with col2:
        if st.button("💎 Continue to Financial Modeler Pro", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Pro"
            st.rerun()
    
    st.caption("💡 Your idea context will be available in the modelers")
