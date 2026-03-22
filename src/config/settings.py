"""
North Star Unified Shell - Configuration Settings
"""

APP_CONFIG = {
    "app_name": "Small Business Lab",
    "app_tagline": "Small Business Decision Support Platform",
    "version": "1.0.0 Lite",
    "mode": "Lite",
}

UI_CONFIG = {
    "page_title": "Small Business Lab",
    "page_icon": "⭐",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

THEME_CONFIG = {
    "primary_color": "#1f77b4",
    "background_color": "#ffffff",
    "secondary_background_color": "#f0f2f6",
    "text_color": "#262730",
    "font": "sans serif",
}

MODULE_CONFIG = {
    "default_module": "Idea Screener",
    "available_modules": {
        "lite": ["Financial Modeler Lite"],
        "advisor": ["Financial Modeler Lite", "Cash Flow Engine", "Valuation Engine", "Business Plan Builder"],
    },
    "module_groups": {
        "active_tools": {
            "title": "ACTIVE TOOLS",
            "modules": [
                {"name": "Idea Screener", "icon": "", "implemented": True},
                {"name": "Entity Assistant", "icon": "🏛️", "implemented": True},
                {"name": "Financial Modeler Lite", "icon": "", "implemented": True},
                {"name": "Financial Modeler Pro", "icon": "", "implemented": True},
                {"name": "LOC Analyzer", "icon": "", "implemented": True},
                {"name": "Business Valuation", "icon": "", "implemented": True},
            ]
        },
        "intelligence": {
            "title": "INTELLIGENCE",
            "modules": [
                
                {"name": "Funding Engine", "icon": "", "implemented": True},
                {"name": "Insights Engine", "icon": "", "implemented": True},
            ]
        },
        "planning": {
            "title": "PLANNING",
            "modules": [
                {"name": "Project Evaluator", "icon": "🎯", "implemented": True},
                {"name": "Business Plan Assistant", "icon": "📊", "implemented": False},
                {"name": "Growth Scenario Planner", "icon": "📈", "implemented": False},
                {"name": "Labor Analyzer", "icon": "👥", "implemented": False},
            ]
        },
        "system": {
            "title": "SYSTEM",
            "modules": [
                {"name": "Clients", "icon": "📂", "implemented": False},
                {"name": "Settings", "icon": "⚙️", "implemented": False},
            ]
        },
        "expand": {
            "title": "EXPAND",
            "modules": [
                {"name": "Advisor Mode", "icon": "🚀", "implemented": False},
                {"name": "Advanced Modules", "icon": "🔓", "implemented": False},
            ]
        }
    }
}

FEATURE_FLAGS = {
    "show_mode_toggle": True,
    "show_client_selector": False,
    "show_upgrade_prompt": True,
    "show_insights_panel": True,
    "enable_advisor_mode": False,
}
