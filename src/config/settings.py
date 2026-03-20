"""
North Star Unified Shell - Configuration Settings
"""

APP_CONFIG = {
    "app_name": "North Star Business Lab",
    "app_tagline": "Small Business Decision Support Platform",
    "version": "1.0.0 Lite",
    "mode": "Lite",
}

UI_CONFIG = {
    "page_title": "North Star Business Lab",
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
    "default_module": "Financial Modeler Lite",
    "available_modules": {
        "lite": ["Financial Modeler Lite"],
        "advisor": ["Financial Modeler Lite", "Cash Flow Engine", "Valuation Engine", "Business Plan Builder"],
    },
}

FEATURE_FLAGS = {
    "show_mode_toggle": True,
    "show_client_selector": True,
    "show_upgrade_prompt": True,
    "show_insights_panel": True,
    "enable_advisor_mode": False,
}
