"""
North Star Unified Shell App - Main Entry Point
A unified small-business decision support platform

Author: North Star Business Intelligence
Version: 1.0.0 Lite
"""
import streamlit as st
from src.config.settings import UI_CONFIG, MODULE_CONFIG
from src.state.app_state import initialize_state, get_active_module
from src.ui.shell import render_shell
from src.ui.placeholders import render_placeholder
from src.modules.command_center import render_command_center
from src.modules.idea_screener import render_idea_screener
from src.modules.entity_assistant import render_entity_assistant
from src.modules.financial_modeler_lite import render_financial_modeler_lite
from src.modules.financial_modeler_pro import render_financial_modeler_pro
from src.modules.project_evaluator import render_project_evaluator
from src.modules.loc_analyzer import render_loc_analyzer
from src.modules.valuation_engine import render_business_valuation
from src.modules.insights_engine import render_insights_engine
from src.modules.insights_panel import render_insights_panel
from src.ui.styles import apply_global_styles


st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["initial_sidebar_state"],
)


def load_custom_css():
    """Load custom CSS - now using centralized design system"""
    apply_global_styles()


def render_debug_panel():
    """Render data integrity debug panel with sync validation"""
    from src.state.data_validator import validate_system_integrity
    from src.state.financial_state import get_core_financials
    from src.state.system_validator import validate_system_sync, get_integrity_score, generate_sync_report
    from src.state.sync_engine import sync_status, get_sync_history
    
    with st.expander("🔍 Data Integrity & Sync Debug Panel"):
        st.markdown("### System State Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Core Financials")
            core = get_core_financials()
            st.json({
                "revenue": core.get("revenue", 0),
                "expenses": core.get("expenses", 0),
                "profit": core.get("profit", 0),
                "growth_rate": core.get("growth_rate", 0),
                "source": core.get("source_module", "Not set")
            })
            
            st.markdown("#### Valuation")
            valuation = st.session_state.get("valuation_range")
            if valuation:
                st.json({"low": valuation[0], "high": valuation[1]})
            else:
                st.caption("Not calculated")
            
            st.markdown("#### LOC Recommendation")
            loc = st.session_state.get("loc_recommendation")
            if loc:
                st.json({
                    "amount": loc.get("recommended_amount", 0),
                    "purpose": loc.get("purpose", "N/A")
                })
            else:
                st.caption("Not analyzed")
        
        with col2:
            st.markdown("#### Project Evaluation")
            project = st.session_state.get("project_evaluation")
            if project:
                st.json({
                    "score": project.get("overall_score", 0),
                    "priority": project.get("priority_classification", "N/A")
                })
            else:
                st.caption("Not evaluated")
            
            st.markdown("#### Idea Context")
            idea = st.session_state.get("idea_context")
            if idea:
                st.json({
                    "title": idea.get("idea_title", "N/A"),
                    "score": idea.get("viability_score", 0)
                })
            else:
                st.caption("Not screened")
            
            st.markdown("#### Entity Structure")
            entity = st.session_state.get("entity_structure")
            if entity:
                st.json({"type": entity.get("entity_type", "N/A")})
            else:
                st.caption("Not selected")
        
        st.divider()
        
        st.markdown("### System Integrity Report")
        report = validate_system_integrity(st.session_state)
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("Integrity Score", f"{report['integrity_score']}%")
        
        with col4:
            st.metric("Valid Keys", len(report['valid_keys']))
        
        with col5:
            st.metric("Missing Keys", len(report['missing_keys']))
        
        if report['missing_keys']:
            st.warning(f"Missing: {', '.join(report['missing_keys'])}")
        
        if report['invalid_data']:
            st.error(f"Invalid: {', '.join(report['invalid_data'])}")
        
        if report['integrity_score'] == 100:
            st.success("✅ All data contracts validated successfully!")
        
        st.divider()
        
        st.markdown("### Sync Validation")
        
        # Check sync issues
        sync_issues = validate_system_sync()
        sync_score = get_integrity_score()
        
        col6, col7 = st.columns(2)
        
        with col6:
            st.metric("Sync Score", f"{sync_score}%")
            
            # Show sync status
            status = sync_status()
            if status["has_data"]:
                st.success(f"✅ Synced - Last by: {status['last_updated_by']}")
            else:
                st.warning("⚠️ No data in core")
        
        with col7:
            st.metric("Sync Issues", len(sync_issues))
            
            # Show sync history
            history = get_sync_history()
            if history:
                last_sync = history[-1]
                st.caption(f"Last sync: {last_sync['source']}")
        
        if sync_issues:
            st.error("**Sync Issues Detected:**")
            for issue in sync_issues:
                st.write(issue)
        else:
            st.success("✅ All modules synced correctly!")


def render_main_content():
    """Render the main content area based on active module"""
    active_module = get_active_module()
    
    # Add debug panel at top
    render_debug_panel()
    
    if active_module == "Command Center":
        render_command_center()
    elif active_module == "Idea Screener":
        render_idea_screener()
    elif active_module == "Entity Assistant":
        render_entity_assistant()
    elif active_module == "Financial Modeler Lite":
        render_financial_modeler_lite()
    elif active_module == "Financial Modeler Pro":
        render_financial_modeler_pro()
    elif active_module == "Project Evaluator":
        render_project_evaluator()
    elif active_module == "Business Valuation":
        render_business_valuation()
    elif active_module == "LOC Analyzer":
        render_loc_analyzer()
    elif active_module == "Funding Engine":
        render_funding_engine()
    elif active_module == "Insights Engine":
        render_insights_engine()
    elif active_module == "Insights":
        render_insights_panel()
    else:
        if is_module_implemented(active_module):
            st.error(f"Module '{active_module}' is implemented but not routed correctly")
        else:
            render_placeholder(active_module)


def is_module_implemented(module_name):
    """Check if a module is marked as implemented in config"""
    module_groups = MODULE_CONFIG.get("module_groups", {})
    for group_data in module_groups.values():
        for module in group_data["modules"]:
            if module["name"] == module_name:
                return module["implemented"]
    return False


def render_value_engine():
    """Render the Value Engine module (integrated valuation)"""
    st.markdown("## 💎 Value Engine")
    st.markdown("*Business valuation and value driver analysis*")
    st.divider()
    
    st.info("💡 **Value Engine** provides comprehensive business valuation across all your financial models.")
    
    st.markdown("### 🎯 Quick Valuation")
    st.write("The Value Engine is integrated into Financial Modeler Lite as the **Valuation** tab.")
    
    st.markdown("### 📊 How to Use")
    st.markdown("1. Navigate to **Financial Modeler Lite** in the sidebar")
    st.markdown("2. Complete your inputs in the **Model Inputs** tab")
    st.markdown("3. Open the **Valuation** tab to see your business value estimates")
    
    st.divider()
    
    st.markdown("### 💎 Valuation Methods Available")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Revenue Multiple**")
        st.write("Value based on revenue (1.5x - 4.0x)")
        st.caption("✅ Available now")
        
        st.markdown("**Earnings Multiple**")
        st.write("Value based on profit (3x - 6x)")
        st.caption("✅ Available now")
    
    with col2:
        st.markdown("**Weighted Valuation**")
        st.write("Combined multi-method approach")
        st.caption("🔒 Coming soon")
        
        st.markdown("**DCF Analysis**")
        st.write("Discounted cash flow valuation")
        st.caption("🔒 Coming soon")
    
    st.divider()
    
    if st.button("🚀 Go to Financial Modeler Lite", type="primary", use_container_width=True):
        from src.state.app_state import set_active_module
        set_active_module("Financial Modeler Lite")
        st.rerun()


def render_funding_engine():
    """Render the Funding Engine module (placeholder with roadmap)"""
    st.markdown("## 🏦 Funding Engine")
    st.markdown("*Capital planning and financing strategy*")
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Overview")
        st.write("The Funding Engine helps you model capital needs, compare financing options, and plan your funding strategy.")
        
        st.divider()
        
        st.markdown("### 🎯 Planned Capabilities")
        st.markdown("- **Capital Needs Calculator** - Determine how much funding you need")
        st.markdown("- **Financing Options Comparison** - Compare debt vs equity vs bootstrapping")
        st.markdown("- **Loan Modeling** - Model different loan terms and repayment schedules")
        st.markdown("- **Dilution Calculator** - Understand equity dilution scenarios")
        st.markdown("- **Runway Analysis** - Calculate cash runway and burn rate")
        st.markdown("- **Investor Readiness** - Assess readiness for fundraising")
        
        st.divider()
        
        st.markdown("### 💡 Use Case")
        st.info("Essential for businesses planning to raise capital, take on debt, or optimize their capital structure. Integrates with Financial Modeler to project funding needs based on growth plans.")
    
    with col2:
        st.markdown("### 🚧 Status")
        st.warning("**In Development**")
        st.caption("High priority module")
        
        st.divider()
        
        st.markdown("### 🔔 Get Notified")
        if st.button("Express Interest", use_container_width=True):
            st.success("✓ Interest noted!")
        
        st.divider()
        
        st.markdown("### 🔗 Related Tools")
        st.caption("• Financial Modeler Pro")
        st.caption("• Value Engine")
    
    st.divider()
    
    st.markdown("### 🏗️ Development Roadmap")
    st.success("✨ **High Priority** - Scheduled for near-term development")
    st.caption("Expected in next major release")
    
    st.divider()
    
    st.markdown("### 💬 Feedback Welcome")
    st.write("Have specific needs for funding analysis? Your input helps us prioritize features.")
    if st.button("Share Feedback", use_container_width=True, key="funding_feedback"):
        st.success("✓ Thank you! Your feedback has been noted.")


def main():
    """Main application entry point"""
    initialize_state()
    
    load_custom_css()
    
    render_shell(render_main_content)


if __name__ == "__main__":
    main()
