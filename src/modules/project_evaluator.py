"""
North Star Unified Shell - Project Evaluator Module
Project assessment and decision engine
"""
import streamlit as st
import plotly.graph_objects as go
from src.modules.project_logic import (
    calculate_project_score,
    classify_priority,
    generate_recommendation,
    generate_insights,
    get_matrix_quadrant,
    get_dimension_description,
    get_rating_guidance,
    create_project_evaluation
)


def render_project_evaluator():
    """Main render function for Project Evaluator module"""
    
    st.markdown("## 🎯 Project Evaluator")
    st.markdown("*Assess whether to pursue a business project right now*")
    st.divider()
    
    # Check if we have results to show
    if "project_evaluator_results" in st.session_state and st.session_state.project_evaluator_results:
        render_results_view()
    else:
        render_input_view()


def render_input_view():
    """Render the input form for project evaluation"""
    
    st.markdown("### Project Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        project_name = st.text_input(
            "Project Name",
            placeholder="e.g., Launch Online Store",
            help="A clear name for this business initiative"
        )
    
    with col2:
        st.markdown("")  # Spacing
    
    project_description = st.text_area(
        "Short Description",
        placeholder="Describe the project in 2-3 sentences...",
        help="Brief overview of what this project involves",
        height=100
    )
    
    st.divider()
    
    st.markdown("### Evaluation Dimensions")
    st.caption("Rate each dimension on a 1-5 scale")
    
    # Financial Impact
    render_dimension_rating(
        "financial_impact",
        "💰 Financial Impact",
        "financial_rating",
        "Expected revenue increase, cost savings, or ROI potential"
    )
    
    st.markdown("")
    
    # Strategic Alignment
    render_dimension_rating(
        "strategic_alignment",
        "🎯 Strategic Alignment",
        "alignment_rating",
        "Alignment with business goals and core direction"
    )
    
    st.markdown("")
    
    # Capacity / Readiness
    render_dimension_rating(
        "capacity_readiness",
        "✅ Capacity / Readiness",
        "capacity_rating",
        "Team capacity and capital availability"
    )
    
    st.markdown("")
    
    # Effort / Complexity
    render_dimension_rating(
        "effort_complexity",
        "🏋️ Effort / Complexity",
        "effort_rating",
        "Time required and operational complexity (lower is better)"
    )
    
    st.markdown("")
    
    # Risk Level
    render_dimension_rating(
        "risk_level",
        "⚠️ Risk Level",
        "risk_rating",
        "Uncertainty, dependencies, and potential obstacles (lower is better)"
    )
    
    st.divider()
    
    # Evaluate button
    if st.button("🔍 Evaluate Project", type="primary", use_container_width=True):
        # Collect inputs
        inputs = {
            "project_name": project_name,
            "project_description": project_description,
            "financial_rating": st.session_state.get("financial_rating", 3),
            "alignment_rating": st.session_state.get("alignment_rating", 3),
            "capacity_rating": st.session_state.get("capacity_rating", 3),
            "effort_rating": st.session_state.get("effort_rating", 3),
            "risk_rating": st.session_state.get("risk_rating", 3)
        }
        
        # Validate required fields
        if not project_name:
            st.error("⚠️ Please provide a project name")
            return
        
        # Calculate score and classification
        score = calculate_project_score(inputs)
        priority = classify_priority(score)
        recommendation = generate_recommendation(score, priority, inputs)
        insights = generate_insights(inputs)
        
        # Create project evaluation
        project_eval = create_project_evaluation(
            inputs,
            score,
            priority,
            recommendation,
            insights
        )
        
        # Store in session state
        st.session_state["project_evaluation"] = project_eval
        st.session_state["project_evaluator_results"] = True
        
        st.rerun()


def render_dimension_rating(dimension_key, title, session_key, description):
    """Render a dimension rating slider with guidance"""
    
    guidance = get_rating_guidance(dimension_key)
    
    with st.expander(f"{title}", expanded=False):
        st.caption(description)
        
        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=3,
            key=session_key,
            help="1 = Low/Minimal, 3 = Moderate, 5 = High/Significant"
        )
        
        # Show guidance for current rating
        if rating in guidance:
            st.caption(f"**{rating}/5:** {guidance[rating]}")


def render_results_view():
    """Render the results view after evaluation"""
    
    project_eval = st.session_state.get("project_evaluation", {})
    
    if not project_eval:
        st.session_state["project_evaluator_results"] = False
        st.rerun()
        return
    
    # Header with project name
    st.markdown(f"### 📋 Evaluation Results: {project_eval['project_name']}")
    
    if project_eval.get("project_description"):
        st.caption(project_eval["project_description"])
    
    st.divider()
    
    # Project Score and Priority
    render_score_section(project_eval)
    
    st.divider()
    
    # Dimension Breakdown
    render_dimension_breakdown(project_eval)
    
    st.divider()
    
    # Recommendation
    render_recommendation_section(project_eval)
    
    st.divider()
    
    # Effort vs Impact Matrix
    render_matrix_visualization(project_eval)
    
    st.divider()
    
    # Insights
    render_insights_section(project_eval)
    
    st.divider()
    
    # Next Steps
    render_next_steps(project_eval)
    
    st.divider()
    
    # Evaluate Another button
    if st.button("🔄 Evaluate Another Project", use_container_width=True):
        st.session_state["project_evaluator_results"] = False
        st.rerun()


def render_score_section(project_eval):
    """Render the project score section"""
    
    st.markdown("### 🎯 Project Score")
    
    score = project_eval["score"]
    priority = project_eval["priority"]
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.metric("Score", f"{score:.0f}/100")
    
    with col2:
        st.metric("Priority Level", priority)
    
    with col3:
        # Visual indicator
        if priority == "High Priority":
            st.success("High")
        elif priority == "Medium Priority":
            st.warning("Medium")
        else:
            st.info("Low")
    
    # Progress bar
    st.progress(score / 100)


def render_dimension_breakdown(project_eval):
    """Render dimension scores breakdown"""
    
    st.markdown("### 📊 Dimension Breakdown")
    
    cols = st.columns(5)
    
    dimensions = [
        ("financial", "💰 Financial", False),
        ("alignment", "🎯 Alignment", False),
        ("capacity", "✅ Capacity", False),
        ("effort", "🏋️ Effort", True),
        ("risk", "⚠️ Risk", True)
    ]
    
    for idx, (key, label, is_inverted) in enumerate(dimensions):
        with cols[idx]:
            value = project_eval[key]
            st.metric(label, f"{value}/5")
            
            if is_inverted:
                st.caption("(lower is better)")


def render_recommendation_section(project_eval):
    """Render recommendation section"""
    
    st.markdown("### 💡 Recommendation")
    
    recommendation = project_eval["recommendation"]
    priority = project_eval["priority"]
    
    if priority == "High Priority":
        st.success(recommendation)
    elif priority == "Medium Priority":
        st.warning(recommendation)
    else:
        st.info(recommendation)


def render_matrix_visualization(project_eval):
    """Render effort vs impact matrix visualization"""
    
    st.markdown("### 📈 Effort vs Impact Matrix")
    
    financial = project_eval["financial"]
    effort = project_eval["effort"]
    quadrant = project_eval["quadrant"]
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add quadrant background rectangles
    # Do Now (High Impact, Low Effort) - Green
    fig.add_shape(
        type="rect",
        x0=0.5, y0=3, x1=3, y1=5.5,
        fillcolor="rgba(0, 255, 0, 0.1)",
        line=dict(width=0)
    )
    
    # Plan (High Impact, High Effort) - Yellow
    fig.add_shape(
        type="rect",
        x0=3, y0=3, x1=5.5, y1=5.5,
        fillcolor="rgba(255, 255, 0, 0.1)",
        line=dict(width=0)
    )
    
    # Optional (Low Impact, Low Effort) - Blue
    fig.add_shape(
        type="rect",
        x0=0.5, y0=0.5, x1=3, y1=3,
        fillcolor="rgba(0, 0, 255, 0.1)",
        line=dict(width=0)
    )
    
    # Avoid (Low Impact, High Effort) - Red
    fig.add_shape(
        type="rect",
        x0=3, y0=0.5, x1=5.5, y1=3,
        fillcolor="rgba(255, 0, 0, 0.1)",
        line=dict(width=0)
    )
    
    # Add quadrant labels
    fig.add_annotation(x=1.75, y=4.25, text="<b>Do Now</b>", showarrow=False, font=dict(size=12, color="green"))
    fig.add_annotation(x=4.25, y=4.25, text="<b>Plan</b>", showarrow=False, font=dict(size=12, color="orange"))
    fig.add_annotation(x=1.75, y=1.75, text="<b>Optional</b>", showarrow=False, font=dict(size=12, color="blue"))
    fig.add_annotation(x=4.25, y=1.75, text="<b>Avoid</b>", showarrow=False, font=dict(size=12, color="red"))
    
    # Add project point
    fig.add_trace(go.Scatter(
        x=[effort],
        y=[financial],
        mode='markers+text',
        marker=dict(size=20, color='darkblue', symbol='diamond'),
        text=[project_eval["project_name"]],
        textposition="top center",
        textfont=dict(size=10, color='darkblue'),
        name='Your Project',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        xaxis=dict(
            title="Effort / Complexity →",
            range=[0.5, 5.5],
            tickvals=[1, 2, 3, 4, 5],
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title="Financial Impact →",
            range=[0.5, 5.5],
            tickvals=[1, 2, 3, 4, 5],
            gridcolor='lightgray'
        ),
        height=500,
        plot_bgcolor='white',
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quadrant interpretation
    st.caption(f"**Your project is in the '{quadrant}' quadrant**")
    
    quadrant_guidance = {
        "Do Now": "High impact with low effort — excellent opportunity for quick wins",
        "Plan": "High impact but requires significant effort — plan carefully and allocate resources",
        "Optional": "Low effort but limited impact — consider as a secondary priority",
        "Avoid": "High effort with low impact — ROI may not justify the investment"
    }
    
    st.info(quadrant_guidance.get(quadrant, ""))


def render_insights_section(project_eval):
    """Render insights section"""
    
    st.markdown("### 💡 Key Insights")
    
    insights = project_eval.get("insights", [])
    
    if insights:
        for insight in insights:
            st.markdown(insight)
    else:
        st.caption("Complete evaluation to see insights")


def render_next_steps(project_eval):
    """Render next steps section"""
    
    st.markdown("### 🚀 Next Steps")
    
    priority = project_eval["priority"]
    
    if priority == "High Priority":
        st.markdown("**Ready to move forward?** Consider building detailed financial projections for this project.")
    elif priority == "Medium Priority":
        st.markdown("**Plan and refine:** Address key concerns, then consider detailed financial modeling.")
    else:
        st.markdown("**Refine or defer:** Consider strengthening the project fundamentals or exploring higher-priority opportunities.")
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Proceed to Financial Modeling", type="primary", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Lite"
            st.rerun()
    
    with col2:
        if st.button("💎 Open Financial Modeler Pro", use_container_width=True):
            st.session_state["active_module"] = "Financial Modeler Pro"
            st.rerun()
    
    st.caption("💡 Your project evaluation will be available for reference")
