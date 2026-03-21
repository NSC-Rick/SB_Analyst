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
from src.modules.financial_modeler_lite import render_financial_modeler_lite
from src.modules.financial_modeler_pro import render_financial_modeler_pro
from src.modules.valuation_logic import calculate_revenue_multiple, calculate_earnings_multiple
from src.modules.insights_panel import render_insights_panel


st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["initial_sidebar_state"],
)


def load_custom_css():
    """Load custom CSS for professional styling"""
    st.markdown("""
    <style>
        /* Main app styling */
        .main {
            padding: 0rem 1rem;
        }
        
        /* Header styling */
        h1 {
            color: #1f77b4;
            font-weight: 600;
        }
        
        h2 {
            color: #262730;
            font-weight: 600;
            margin-top: 1rem;
        }
        
        h3 {
            color: #262730;
            font-weight: 500;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 5px;
            font-weight: 500;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        
        /* Dividers */
        hr {
            margin: 1.5rem 0;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 5px;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-weight: 500;
            font-size: 1rem;
        }
        
        /* Cards and containers */
        [data-testid="stExpander"] {
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }
        
        /* Clean spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_main_content():
    """Render the main content area based on active module"""
    active_module = get_active_module()
    
    if active_module == "Financial Modeler Lite":
        render_financial_modeler_lite()
    elif active_module == "Financial Modeler Pro":
        render_financial_modeler_pro()
    elif active_module == "Value Engine":
        render_value_engine()
    elif active_module == "Funding Engine":
        render_funding_engine()
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
