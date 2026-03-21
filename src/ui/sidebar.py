"""
North Star Unified Shell - Sidebar Component
Grouped navigation structure for full platform
"""
import streamlit as st
from src.config.settings import MODULE_CONFIG
from src.state.app_state import get_active_module, set_active_module


def render_sidebar():
    """Render the left sidebar navigation with grouped module structure"""
    with st.sidebar:
        st.markdown("## 🧭 Platform Navigation")
        st.divider()
        
        current_module = get_active_module()
        
        module_groups = MODULE_CONFIG.get("module_groups", {})
        
        for group_key, group_data in module_groups.items():
            render_module_group(group_data, current_module)
            st.divider()
        
        st.markdown("---")
        st.caption("North Star Business Lab")
        st.caption("Decision Support Platform")


def render_module_group(group_data, current_module):
    """Render a group of modules with section header"""
    
    st.markdown(f"### {group_data['title']}")
    
    for module in group_data['modules']:
        module_name = module['name']
        icon = module['icon']
        implemented = module['implemented']
        
        is_active = (current_module == module_name)
        
        button_label = f"{icon} {module_name}"
        
        if implemented:
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                button_label,
                use_container_width=True,
                type=button_type,
                key=f"nav_{module_name}"
            ):
                set_active_module(module_name)
                st.rerun()
        else:
            if st.button(
                button_label,
                use_container_width=True,
                disabled=False,
                key=f"nav_{module_name}",
                type="secondary"
            ):
                set_active_module(module_name)
                st.rerun()
            
            st.caption("*Coming soon*")
