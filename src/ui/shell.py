"""
North Star Unified Shell - Main Shell Layout
"""
import streamlit as st
from src.ui.topbar import render_topbar
from src.ui.sidebar import render_sidebar
from src.ui.footer import render_footer


def render_shell(content_renderer):
    """
    Render the complete shell layout with provided content
    
    Args:
        content_renderer: Function that renders the main content area
    """
    render_topbar()
    
    render_sidebar()
    
    content_renderer()
    
    render_footer()
