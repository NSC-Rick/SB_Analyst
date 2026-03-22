"""
North Star Unified Shell - Sidebar Component
Grouped navigation structure for full platform
"""
import streamlit as st
from src.config.settings import MODULE_CONFIG
from src.state.app_state import get_active_module, set_active_module
from src.ui.key_manager import (
    generate_nav_key,
    get_module_collision_report,
    generate_debug_key_map
)


def render_sidebar():
    """Render the left sidebar navigation with grouped module structure"""
    with st.sidebar:
        st.markdown("## 🧭 Platform Navigation")
        st.divider()
        
        current_module = get_active_module()
        module_groups = MODULE_CONFIG.get("module_groups", {})
        
        collision_report = get_module_collision_report(module_groups)
        if collision_report:
            with st.expander("⚠️ Configuration Warning", expanded=False):
                st.markdown(collision_report)
        
        debug_mode = st.checkbox(
            "🔍 Debug Navigation Keys",
            value=False,
            key="sidebar_debug_mode",
            help="Show generated widget keys for debugging"
        )
        
        if debug_mode:
            with st.expander("Debug: Key Map", expanded=True):
                key_map = generate_debug_key_map(module_groups)
                for path, key in key_map.items():
                    st.code(f"{path}\n→ {key}", language="text")
        
        st.divider()
        
        for group_key, group_data in module_groups.items():
            render_module_group(group_key, group_data, current_module, debug_mode)
            st.divider()
        
        st.markdown("---")
        st.caption("North Star Business Lab")
        st.caption("Decision Support Platform")


def render_module_group(group_key, group_data, current_module, debug_mode=False):
    """Render a group of modules with section header"""
    
    st.markdown(f"### {group_data['title']}")
    
    for index, module in enumerate(group_data['modules']):
        module_name = module['name']
        icon = module['icon']
        implemented = module['implemented']
        
        unique_key = generate_nav_key(group_key, module_name, index)
        
        is_active = (current_module == module_name)
        
        button_label = f"{icon} {module_name}"
        
        if debug_mode:
            st.caption(f"🔑 `{unique_key}`")
        
        if implemented:
            button_type = "primary" if is_active else "secondary"
            
            if st.button(
                button_label,
                use_container_width=True,
                type=button_type,
                key=unique_key
            ):
                set_active_module(module_name)
                st.rerun()
        else:
            if st.button(
                button_label,
                use_container_width=True,
                disabled=False,
                key=unique_key,
                type="secondary"
            ):
                set_active_module(module_name)
                st.rerun()
            
            st.caption("*Coming soon*")
