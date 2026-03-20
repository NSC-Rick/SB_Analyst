"""
North Star Unified Shell - Sidebar Component
"""
import streamlit as st
from src.config.settings import MODULE_CONFIG, FEATURE_FLAGS
from src.state.app_state import get_active_module, set_active_module, get_app_mode


def render_sidebar():
    """Render the left sidebar navigation"""
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        st.divider()
        
        current_module = get_active_module()
        mode = get_app_mode()
        
        available_modules = MODULE_CONFIG["available_modules"].get(mode.lower(), ["Financial Modeler Lite"])
        
        st.markdown("### 📊 Active Tools")
        
        if st.button(
            "💰 Financial Modeler Lite",
            use_container_width=True,
            type="primary" if current_module == "Financial Modeler Lite" else "secondary"
        ):
            set_active_module("Financial Modeler Lite")
            st.rerun()
        
        st.divider()
        
        if FEATURE_FLAGS["show_insights_panel"]:
            st.markdown("### 💡 Insights")
            if st.button("📈 View Insights", use_container_width=True, disabled=True):
                pass
            st.caption("*Analysis summaries and alerts*")
        
        st.divider()
        
        if FEATURE_FLAGS["show_upgrade_prompt"] and mode == "Lite":
            st.markdown("### 🔓 Unlock More Tools")
            
            with st.expander("🎯 Available in Advisor Mode", expanded=False):
                st.markdown("""
                **Coming Soon:**
                - 💵 Cash Flow / LOC Engine
                - 📊 Valuation Engine
                - 📋 Business Plan Builder
                - 🎯 Change Readiness
                - 🧠 Intelligence Layer
                """)
                
                st.info("Advisor Mode expands your workspace with advanced analysis tools")
        
        st.divider()
        
        st.markdown("---")
        st.caption("North Star Business Lab v1.0")
        st.caption("Lite Edition")
