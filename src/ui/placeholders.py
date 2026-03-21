"""
North Star Unified Shell - Placeholder Module Screens
Reusable placeholder rendering for not-yet-implemented modules
"""
import streamlit as st


MODULE_DESCRIPTIONS = {
    "Idea Screener": {
        "tagline": "Rapid Business Concept Assessment",
        "description": "Quickly assess business concepts and identify whether an idea is ready for deeper modeling.",
        "features": [
            "Concept viability scoring",
            "Market opportunity assessment",
            "Resource requirement estimation",
            "Risk factor identification",
            "Go/No-Go recommendation"
        ],
        "use_case": "Use this tool before building detailed financial models to validate whether a business idea warrants deeper investment of time and resources."
    },
    "Insights Engine": {
        "tagline": "Cross-Module Intelligence Layer",
        "description": "Connect outputs across modules to generate intelligent observations and next-step guidance.",
        "features": [
            "Pattern recognition across financial data",
            "Automated anomaly detection",
            "Trend analysis and forecasting",
            "Strategic recommendations",
            "Priority action identification"
        ],
        "use_case": "The Insights Engine aggregates data from all active modules to surface non-obvious opportunities and risks that emerge from the complete picture of your business."
    },
    "Business Plan Builder": {
        "tagline": "Structured Planning Document Generator",
        "description": "Translate financial and strategic inputs into structured planning documents.",
        "features": [
            "Executive summary generation",
            "Financial projections integration",
            "Market analysis framework",
            "Operational plan templates",
            "Export to professional formats"
        ],
        "use_case": "Transform your financial models and strategic inputs into investor-ready or lender-ready business plan documents with minimal manual effort."
    },
    "Growth Scenario Planner": {
        "tagline": "Multi-Path Strategic Modeling",
        "description": "Model and compare multiple growth trajectories to identify optimal strategic paths.",
        "features": [
            "Scenario comparison (best/base/worst)",
            "Sensitivity analysis",
            "Resource allocation modeling",
            "Timeline and milestone planning",
            "Risk-adjusted projections"
        ],
        "use_case": "Explore different strategic options side-by-side to understand trade-offs and make data-driven decisions about growth investments."
    },
    "Workforce / RPLH Analyzer": {
        "tagline": "Labor Planning & Revenue Per Labor Hour Analysis",
        "description": "Optimize workforce planning and analyze productivity metrics for labor-intensive businesses.",
        "features": [
            "Revenue per labor hour calculation",
            "Staffing level optimization",
            "Labor cost modeling",
            "Productivity benchmarking",
            "Hiring timeline planning"
        ],
        "use_case": "Essential for service businesses and operations where labor is a primary cost driver. Understand optimal staffing levels and productivity targets."
    },
    "Clients": {
        "tagline": "Client Portfolio Management",
        "description": "Manage multiple client profiles and switch between business contexts seamlessly.",
        "features": [
            "Client profile creation and storage",
            "Quick client switching",
            "Client-specific data isolation",
            "Portfolio overview dashboard",
            "Client comparison tools"
        ],
        "use_case": "For advisors and consultants managing multiple small business clients, or business owners managing multiple ventures."
    },
    "Settings": {
        "tagline": "Platform Configuration & Preferences",
        "description": "Customize your North Star platform experience and manage account settings.",
        "features": [
            "Display preferences",
            "Default assumptions and parameters",
            "Data export/import options",
            "Notification preferences",
            "Account management"
        ],
        "use_case": "Personalize the platform to match your workflow and business context."
    },
    "Advisor Mode": {
        "tagline": "Advanced Professional Features",
        "description": "Unlock the full suite of advanced analysis tools and professional-grade capabilities.",
        "features": [
            "All premium modules unlocked",
            "Advanced scenario modeling",
            "White-label reporting",
            "API access for integrations",
            "Priority support"
        ],
        "use_case": "Designed for business advisors, consultants, and sophisticated business owners who need the complete analytical toolkit."
    },
    "Advanced Modules": {
        "tagline": "Specialized Analysis Tools",
        "description": "Access to specialized modules for specific industries and advanced use cases.",
        "features": [
            "Industry-specific templates",
            "Advanced valuation methods",
            "M&A readiness assessment",
            "Tax optimization modeling",
            "Custom module development"
        ],
        "use_case": "For specialized analytical needs beyond the core platform capabilities."
    }
}


def render_placeholder(module_name):
    """
    Render a polished placeholder page for a not-yet-implemented module
    
    Args:
        module_name: Name of the module to render placeholder for
    """
    
    if module_name not in MODULE_DESCRIPTIONS:
        render_generic_placeholder(module_name)
        return
    
    info = MODULE_DESCRIPTIONS[module_name]
    
    st.markdown(f"## {module_name}")
    st.markdown(f"*{info['tagline']}*")
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Overview")
        st.write(info['description'])
        
        st.divider()
        
        st.markdown("### 🎯 Planned Capabilities")
        for feature in info['features']:
            st.markdown(f"- {feature}")
        
        st.divider()
        
        st.markdown("### 💡 Use Case")
        st.info(info['use_case'])
    
    with col2:
        st.markdown("### 🚧 Status")
        st.warning("**Coming Soon**")
        st.caption("This module is planned for a future release")
        
        st.divider()
        
        st.markdown("### 🔔 Get Notified")
        st.write("Want to be notified when this module launches?")
        
        if st.button("Express Interest", use_container_width=True):
            st.success("✓ Interest noted! We'll keep you updated.")
        
        st.divider()
        
        st.markdown("### 🔗 Related Tools")
        render_related_modules(module_name)
    
    st.divider()
    
    st.markdown("### 🏗️ Development Roadmap")
    render_roadmap_hint(module_name)


def render_generic_placeholder(module_name):
    """Render a basic placeholder for modules without detailed descriptions"""
    
    st.markdown(f"## {module_name}")
    st.markdown("*Planned Capability*")
    st.divider()
    
    st.info(f"**{module_name}** is a planned module that will be added to the North Star platform in a future release.")
    
    st.markdown("### 🚧 Status")
    st.warning("This module is currently under development")
    
    st.divider()
    
    st.markdown("### 🔙 Available Now")
    st.write("While this module is being developed, explore our active tools:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("- 💰 **Financial Modeler Lite**")
        st.markdown("- 💎 **Financial Modeler Pro**")
    
    with col2:
        st.markdown("- 💎 **Value Engine**")
        st.markdown("- 🏦 **Funding Engine**")


def render_related_modules(module_name):
    """Render suggestions for related active modules"""
    
    related = {
        "Idea Screener": ["Financial Modeler Lite", "Value Engine"],
        "Insights Engine": ["Financial Modeler Pro", "Value Engine"],
        "Business Plan Builder": ["Financial Modeler Pro", "Funding Engine"],
        "Growth Scenario Planner": ["Financial Modeler Pro", "Value Engine"],
        "Workforce / RPLH Analyzer": ["Financial Modeler Pro"],
        "Clients": ["Financial Modeler Lite", "Financial Modeler Pro"],
        "Settings": ["All Modules"],
        "Advisor Mode": ["Financial Modeler Pro", "Value Engine"],
        "Advanced Modules": ["Financial Modeler Pro", "Value Engine"]
    }
    
    if module_name in related:
        st.write("**Try these active modules:**")
        for mod in related[module_name]:
            st.caption(f"• {mod}")
    else:
        st.caption("Explore active modules in the sidebar")


def render_roadmap_hint(module_name):
    """Render development timeline hint"""
    
    priority_modules = ["Idea Screener", "Insights Engine", "Business Plan Builder"]
    
    if module_name in priority_modules:
        st.success("✨ **High Priority** - Scheduled for near-term development")
        st.caption("Expected in next major release")
    else:
        st.info("📅 **Planned** - On the development roadmap")
        st.caption("Timeline to be determined based on user demand")
    
    st.divider()
    
    st.markdown("### 💬 Feedback Welcome")
    st.write("Have specific needs for this module? Your input helps us prioritize features.")
    
    if st.button("Share Feedback", use_container_width=True, key=f"feedback_{module_name}"):
        st.success("✓ Thank you! Your feedback has been noted.")
