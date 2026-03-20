"""
North Star Unified Shell - State Management
"""
import streamlit as st
from src.config.settings import MODULE_CONFIG, APP_CONFIG


def initialize_state():
    """Initialize session state variables"""
    if "active_module" not in st.session_state:
        st.session_state.active_module = MODULE_CONFIG["default_module"]
    
    if "app_mode" not in st.session_state:
        st.session_state.app_mode = APP_CONFIG["mode"]
    
    if "active_client" not in st.session_state:
        st.session_state.active_client = "No Client Selected"
    
    if "show_upgrade_banner" not in st.session_state:
        st.session_state.show_upgrade_banner = False
    
    if "insights_visible" not in st.session_state:
        st.session_state.insights_visible = True


def set_active_module(module_name):
    """Set the active module"""
    st.session_state.active_module = module_name


def get_active_module():
    """Get the current active module"""
    return st.session_state.get("active_module", MODULE_CONFIG["default_module"])


def set_app_mode(mode):
    """Set the application mode"""
    st.session_state.app_mode = mode


def get_app_mode():
    """Get the current application mode"""
    return st.session_state.get("app_mode", APP_CONFIG["mode"])


def set_active_client(client_name):
    """Set the active client"""
    st.session_state.active_client = client_name


def get_active_client():
    """Get the current active client"""
    return st.session_state.get("active_client", "No Client Selected")
