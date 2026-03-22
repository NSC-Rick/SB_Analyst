"""
North Star Unified Shell - Top Bar Component
"""
import streamlit as st
from src.config.settings import APP_CONFIG, FEATURE_FLAGS
from src.state.app_state import get_app_mode, get_active_client


def render_topbar():
    """Render the top navigation bar with header band styling"""
    
    st.markdown('<div class="ns-header">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        st.markdown(f"# ⭐ {APP_CONFIG['app_name']}")
        st.caption(APP_CONFIG['app_tagline'])
    
    with col2:
        if FEATURE_FLAGS["show_client_selector"]:
            st.markdown("#### 👤 Client")
            client = get_active_client()
            st.markdown(f"**{client}**")
    
    with col3:
        if FEATURE_FLAGS["show_mode_toggle"]:
            st.markdown("#### 🎯 Mode")
            mode = get_app_mode()
            if mode == "Lite":
                st.success("Lite Mode Active")
            else:
                st.info(f"{mode} Mode")
    
    with col4:
        if FEATURE_FLAGS["show_upgrade_prompt"] and get_app_mode() == "Lite":
            st.markdown("#### 🚀 Expand")
            st.caption("Advisor Mode (Coming Soon)")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("")
