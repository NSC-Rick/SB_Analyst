"""
North Star Unified Shell - Command Center Dashboard
Central hub for business state overview and quick navigation
"""
import streamlit as st
from src.state.financial_state import get_core_financials, get_financial_summary
from src.state.app_state import set_active_module
from src.ui.styles import card_start, card_end


def render_command_center():
    """Main render function for Command Center Dashboard"""
    
    st.markdown("## 🏠 Command Center")
    st.markdown("*Your business intelligence hub*")
    st.markdown("")
    
    # Header Band - System Status
    render_system_status_band()
    
    # KPI Snapshot
    render_kpi_snapshot()
    
    # Key Insights
    render_key_insights()
    
    # Module Status
    render_module_status()
    
    # Quick Actions
    render_quick_actions()
    
    # Data Health
    render_data_health()


def render_system_status_band():
    """Render header band with system status, alerts, and readiness"""
    
    st.markdown('<div class="ns-header">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # System Status
    with col1:
        st.markdown("#### 📊 System Status")
        core = get_core_financials()
        if core.get("revenue", 0) > 0:
            st.success("Active")
        else:
            st.info("Ready")
    
    # Alerts
    with col2:
        st.markdown("#### 🔔 Alerts")
        alerts = get_system_alerts()
        if alerts["count"] > 0:
            st.warning(f"{alerts['count']} Alert(s)")
        else:
            st.success("All Clear")
    
    # Mode
    with col3:
        st.markdown("#### 🎯 Mode")
        mode = st.session_state.get("app_mode", "Lite")
        st.info(f"{mode} Mode")
    
    # Readiness
    with col4:
        st.markdown("#### ✅ Readiness")
        readiness = calculate_readiness_score()
        if readiness >= 75:
            st.success(f"{readiness}%")
        elif readiness >= 50:
            st.warning(f"{readiness}%")
        else:
            st.info(f"{readiness}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("")


def render_kpi_snapshot():
    """Render key performance indicators"""
    
    st.markdown("### 📈 Key Metrics")
    
    card_start()
    
    core = get_core_financials()
    valuation = st.session_state.get("valuation_range")
    loc = st.session_state.get("loc_recommendation")
    project = st.session_state.get("project_evaluation")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        revenue = core.get("revenue", 0)
        st.metric(
            label="💰 Revenue",
            value=f"${revenue:,.0f}" if revenue > 0 else "Not Set",
            help="Monthly revenue"
        )
    
    with col2:
        profit = core.get("profit", 0)
        margin = (profit / revenue * 100) if revenue > 0 else 0
        st.metric(
            label="💵 Profit",
            value=f"${profit:,.0f}" if profit != 0 else "Not Set",
            delta=f"{margin:.1f}% margin" if revenue > 0 else None,
            help="Monthly profit"
        )
    
    with col3:
        if valuation:
            val_low, val_high = valuation
            val_mid = (val_low + val_high) / 2
            st.metric(
                label="💎 Valuation",
                value=f"${val_mid:,.0f}",
                delta=f"${val_low:,.0f} - ${val_high:,.0f}",
                help="Business valuation range"
            )
        else:
            st.metric(
                label="💎 Valuation",
                value="Not Calculated",
                help="Run Business Valuation module"
            )
    
    with col4:
        if loc and isinstance(loc, dict):
            loc_amount = loc.get("recommended_amount", 0)
            st.metric(
                label="🏦 LOC Need",
                value=f"${loc_amount:,.0f}" if loc_amount > 0 else "Not Needed",
                help="Recommended line of credit"
            )
        else:
            st.metric(
                label="🏦 LOC Need",
                value="Not Analyzed",
                help="Run LOC Analyzer module"
            )
    
    with col5:
        if project and isinstance(project, dict):
            score = project.get("overall_score", 0)
            priority = project.get("priority_classification", "Unknown")
            st.metric(
                label="🎯 Project Score",
                value=f"{score}/100" if score > 0 else "Not Rated",
                delta=priority if score > 0 else None,
                help="Project evaluation score"
            )
        else:
            st.metric(
                label="🎯 Project Score",
                value="Not Evaluated",
                help="Run Project Evaluator module"
            )
    
    card_end()


def render_key_insights():
    """Render top 3 insights from the system"""
    
    st.markdown("### 💡 Key Insights")
    
    insights = get_top_insights()
    
    if not insights:
        card_start()
        st.info("💡 Complete modules to generate insights")
        card_end()
        return
    
    for insight in insights[:3]:
        if insight["priority"] == "high":
            st.warning(f"**{insight['title']}** - {insight['message']}")
        elif insight["priority"] == "medium":
            st.info(f"**{insight['title']}** - {insight['message']}")
        else:
            st.success(f"**{insight['title']}** - {insight['message']}")


def render_module_status():
    """Render module completion status"""
    
    st.markdown("### 📋 Module Status")
    
    card_start()
    
    status = get_module_status()
    
    col1, col2 = st.columns([3, 1])
    
    for module_name, module_status in status.items():
        with col1:
            st.markdown(f"**{module_name}**")
        
        with col2:
            if module_status == "Complete":
                st.success("✅ Complete")
            elif module_status == "Partial":
                st.warning("⚠️ Partial")
            else:
                st.info("⚪ Not Started")
        
        st.markdown("")
    
    card_end()


def render_quick_actions():
    """Render quick action buttons for common tasks"""
    
    st.markdown("### 🚀 Quick Actions")
    
    card_start()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 Update Financials", use_container_width=True, type="primary"):
            set_active_module("Financial Modeler Lite")
            st.rerun()
    
    with col2:
        if st.button("💎 Run Valuation", use_container_width=True):
            set_active_module("Business Valuation")
            st.rerun()
    
    with col3:
        if st.button("🎯 Evaluate Project", use_container_width=True):
            set_active_module("Project Evaluator")
            st.rerun()
    
    with col4:
        if st.button("🏦 Analyze LOC", use_container_width=True):
            set_active_module("LOC Analyzer")
            st.rerun()
    
    st.markdown("")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        if st.button("💡 Screen Idea", use_container_width=True):
            set_active_module("Idea Screener")
            st.rerun()
    
    with col6:
        if st.button("🏛️ Choose Entity", use_container_width=True):
            set_active_module("Entity Assistant")
            st.rerun()
    
    with col7:
        if st.button("💎 Advanced Model", use_container_width=True):
            set_active_module("Financial Modeler Pro")
            st.rerun()
    
    with col8:
        if st.button("📊 View Insights", use_container_width=True):
            set_active_module("Insights Engine")
            st.rerun()
    
    card_end()


def render_data_health():
    """Render data health and missing inputs"""
    
    st.markdown("### 🔍 Data Health")
    
    card_start()
    
    health = get_data_health()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Completeness")
        st.progress(health["completeness"] / 100)
        st.caption(f"{health['completeness']}% of core data entered")
    
    with col2:
        st.markdown("#### Missing Inputs")
        if health["missing"]:
            for item in health["missing"]:
                st.caption(f"⚪ {item}")
        else:
            st.caption("✅ All core data complete")
    
    card_end()


def get_system_alerts():
    """Get system alerts and warnings"""
    alerts = []
    
    core = get_core_financials()
    
    # Check for negative profit
    if core.get("profit", 0) < 0:
        alerts.append({"level": "warning", "message": "Negative profit margin"})
    
    # Check for missing valuation
    if not st.session_state.get("valuation_range"):
        if core.get("revenue", 0) > 0:
            alerts.append({"level": "info", "message": "Valuation not calculated"})
    
    # Check for high expenses
    revenue = core.get("revenue", 0)
    expenses = core.get("expenses", 0)
    if revenue > 0 and expenses > revenue * 0.9:
        alerts.append({"level": "warning", "message": "High expense ratio"})
    
    return {
        "count": len(alerts),
        "alerts": alerts
    }


def calculate_readiness_score():
    """Calculate overall system readiness score"""
    score = 0
    max_score = 100
    
    # Financial data (40 points)
    core = get_core_financials()
    if core.get("revenue", 0) > 0:
        score += 20
    if core.get("expenses", 0) > 0:
        score += 10
    if core.get("profit", 0) != 0:
        score += 10
    
    # Valuation (20 points)
    if st.session_state.get("valuation_range"):
        score += 20
    
    # Idea context (15 points)
    if st.session_state.get("idea_context"):
        score += 15
    
    # Entity structure (10 points)
    if st.session_state.get("entity_structure"):
        score += 10
    
    # Project evaluation (15 points)
    if st.session_state.get("project_evaluation"):
        score += 15
    
    return score


def get_top_insights():
    """Get top insights from various modules"""
    insights = []
    
    core = get_core_financials()
    revenue = core.get("revenue", 0)
    profit = core.get("profit", 0)
    expenses = core.get("expenses", 0)
    
    # Financial insights
    if revenue > 0:
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        if margin < 10:
            insights.append({
                "priority": "high",
                "title": "Low Profit Margin",
                "message": f"Your {margin:.1f}% margin is below healthy range. Consider reducing expenses or increasing prices."
            })
        elif margin > 30:
            insights.append({
                "priority": "low",
                "title": "Strong Margins",
                "message": f"Your {margin:.1f}% profit margin is excellent. Consider reinvesting in growth."
            })
        
        if expenses > revenue * 0.8:
            insights.append({
                "priority": "medium",
                "title": "High Expense Ratio",
                "message": f"Expenses are {(expenses/revenue*100):.0f}% of revenue. Look for cost optimization opportunities."
            })
    
    # Valuation insights
    valuation = st.session_state.get("valuation_range")
    if valuation and revenue > 0:
        val_mid = (valuation[0] + valuation[1]) / 2
        multiple = val_mid / (revenue * 12)
        
        if multiple > 3:
            insights.append({
                "priority": "low",
                "title": "Strong Valuation",
                "message": f"Your business is valued at {multiple:.1f}x annual revenue, indicating strong market position."
            })
    
    # LOC insights
    loc = st.session_state.get("loc_recommendation")
    if loc and isinstance(loc, dict):
        if loc.get("recommended_amount", 0) > 0:
            insights.append({
                "priority": "medium",
                "title": "LOC Recommended",
                "message": f"Consider a ${loc['recommended_amount']:,.0f} line of credit for working capital flexibility."
            })
    
    # Project insights
    project = st.session_state.get("project_evaluation")
    if project and isinstance(project, dict):
        score = project.get("overall_score", 0)
        if score >= 70:
            insights.append({
                "priority": "low",
                "title": "Project Ready",
                "message": f"Your project scored {score}/100. Strong candidate for execution."
            })
        elif score < 50:
            insights.append({
                "priority": "high",
                "title": "Project Concerns",
                "message": f"Project scored {score}/100. Review feasibility before proceeding."
            })
    
    # Entity insights
    entity = st.session_state.get("entity_structure")
    if entity and isinstance(entity, dict):
        entity_type = entity.get("entity_type", "")
        if "S-Corp" in entity_type and revenue * 12 > 60000:
            insights.append({
                "priority": "medium",
                "title": "Tax Optimization",
                "message": f"With {entity_type}, you may save on self-employment taxes. Consult a CPA."
            })
    
    return insights


def get_module_status():
    """Get completion status of all modules"""
    core = get_core_financials()
    
    status = {}
    
    # Idea Screener
    if st.session_state.get("idea_context"):
        status["💡 Idea Screener"] = "Complete"
    else:
        status["💡 Idea Screener"] = "Not Started"
    
    # Entity Assistant
    if st.session_state.get("entity_structure"):
        status["🏛️ Entity Assistant"] = "Complete"
    else:
        status["🏛️ Entity Assistant"] = "Not Started"
    
    # Financial Model
    if core.get("revenue", 0) > 0 and core.get("expenses", 0) > 0:
        status["💰 Financial Model"] = "Complete"
    elif core.get("revenue", 0) > 0 or core.get("expenses", 0) > 0:
        status["💰 Financial Model"] = "Partial"
    else:
        status["💰 Financial Model"] = "Not Started"
    
    # Business Valuation
    if st.session_state.get("valuation_range"):
        status["💎 Business Valuation"] = "Complete"
    else:
        status["💎 Business Valuation"] = "Not Started"
    
    # LOC Analyzer
    if st.session_state.get("loc_recommendation"):
        status["🏦 LOC Analyzer"] = "Complete"
    else:
        status["🏦 LOC Analyzer"] = "Not Started"
    
    # Project Evaluator
    if st.session_state.get("project_evaluation"):
        status["🎯 Project Evaluator"] = "Complete"
    else:
        status["🎯 Project Evaluator"] = "Not Started"
    
    return status


def get_data_health():
    """Get data health metrics"""
    core = get_core_financials()
    
    required_fields = ["revenue", "expenses"]
    optional_fields = ["growth_rate", "profit"]
    
    completed = 0
    total = len(required_fields) + len(optional_fields)
    missing = []
    
    # Check required fields
    for field in required_fields:
        if core.get(field, 0) > 0:
            completed += 1
        else:
            missing.append(field.replace("_", " ").title())
    
    # Check optional fields
    for field in optional_fields:
        if core.get(field, 0) != 0:
            completed += 1
    
    # Check other modules
    if st.session_state.get("idea_context"):
        completed += 1
        total += 1
    else:
        total += 1
        missing.append("Idea Context")
    
    if st.session_state.get("entity_structure"):
        completed += 1
        total += 1
    else:
        total += 1
        missing.append("Entity Structure")
    
    completeness = int((completed / total) * 100) if total > 0 else 0
    
    return {
        "completeness": completeness,
        "missing": missing[:5]  # Top 5 missing items
    }
