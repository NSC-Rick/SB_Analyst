"""
North Star Unified Shell App - Main Entry Point
A unified small-business decision support platform

Author: North Star Business Intelligence
Version: 1.0.0 Lite
"""
import streamlit as st
from src.config.settings import UI_CONFIG
from src.state.app_state import initialize_state, get_active_module
from src.ui.shell import render_shell
from src.modules.financial_modeler_lite import render_financial_modeler_lite
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
    elif active_module == "Insights":
        render_insights_panel()
    else:
        st.error(f"Module '{active_module}' not found")


def main():
    """Main application entry point"""
    initialize_state()
    
    load_custom_css()
    
    render_shell(render_main_content)


if __name__ == "__main__":
    main()
