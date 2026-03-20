"""
North Star Unified Shell - Footer Component
"""
import streamlit as st
from src.state.app_state import get_app_mode


def render_footer():
    """Render the bottom insights/status strip"""
    st.divider()
    
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.markdown("**📊 System Status**")
        st.success("✓ System Ready")
    
    with col2:
        st.markdown("**🔔 Alerts & Insights**")
        mode = get_app_mode()
        if mode == "Lite":
            st.info("💡 Lite Mode Active - Core analysis tools available")
        else:
            st.info("No active alerts")
    
    with col3:
        st.markdown("**📈 Quick Stats**")
        st.caption("Ready for analysis")
