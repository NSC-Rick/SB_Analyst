"""
North Star Unified Shell - Save/Load Panel
UI component for project state persistence
"""
import streamlit as st
import json
from src.state.persistence import (
    export_project_state,
    load_project_state,
    get_state_summary,
    clear_project_state,
    generate_project_filename,
    get_state_file_info
)


def render_save_load_panel():
    """
    Render the save/load panel for project persistence
    Can be embedded in sidebar or main content area
    """
    st.markdown("### 💾 Save / Load Project")
    
    # Get current state summary
    summary = get_state_summary()
    
    # Show current workspace status
    with st.expander("📊 Current Workspace Status", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("State Items", summary["total_state_items"])
            if summary["has_financial_data"]:
                st.caption("✅ Financial data")
            else:
                st.caption("⚪ No financial data")
        
        with col2:
            st.metric("Active Module", summary["active_module"])
            if summary["has_idea_context"]:
                st.caption("✅ Idea context")
            if summary["has_project_evaluation"]:
                st.caption("✅ Project evaluation")
    
    st.divider()
    
    # Save section
    render_save_section(summary)
    
    st.divider()
    
    # Load section
    render_load_section()
    
    st.divider()
    
    # Clear/Reset section
    render_reset_section(summary)


def render_save_section(summary):
    """Render the save/download section"""
    
    st.markdown("#### 💾 Save Project")
    
    if summary["total_state_items"] == 0:
        st.info("ℹ️ No data to save yet. Complete a module to create saveable data.")
        return
    
    st.caption(f"Save your current workspace with {summary['total_state_items']} data items")
    
    # Generate filename
    default_filename = generate_project_filename()
    
    # Export state
    state_data = export_project_state()
    json_string = json.dumps(state_data, indent=2)
    
    # Download button
    st.download_button(
        label="💾 Download Project File",
        data=json_string,
        file_name=default_filename,
        mime="application/json",
        use_container_width=True,
        type="primary",
        help="Download your project as a JSON file that you can reload later"
    )
    
    st.caption("✅ File will contain all your inputs, calculations, and results")


def render_load_section():
    """Render the load/upload section"""
    
    st.markdown("#### 📂 Load Project")
    
    st.caption("Restore a previously saved project from a file")
    
    uploaded_file = st.file_uploader(
        "Choose a project file",
        type=["json"],
        help="Upload a .json project file previously saved from this app",
        key="project_file_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Read and parse JSON
            file_contents = uploaded_file.read()
            data = json.loads(file_contents)
            
            # Show file info
            file_info = get_state_file_info(data)
            
            with st.expander("📄 File Information", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.caption(f"**Version:** {file_info['version']}")
                    st.caption(f"**Saved:** {file_info['saved_at'][:10]}")
                    st.caption(f"**Items:** {file_info['state_keys_count']}")
                
                with col2:
                    if file_info.get("idea_title"):
                        st.caption(f"**Idea:** {file_info['idea_title']}")
                    if file_info.get("project_name"):
                        st.caption(f"**Project:** {file_info['project_name']}")
                    
                    if file_info["has_financials"]:
                        st.caption("✅ Financial data")
                    if file_info["has_valuation"]:
                        st.caption("✅ Valuation")
            
            # Load button
            if st.button("📥 Load This Project", type="primary", use_container_width=True):
                success, message = load_project_state(data)
                
                if success:
                    st.success(f"✅ {message}")
                    st.caption("🔄 Reloading app to apply changes...")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        
        except json.JSONDecodeError:
            st.error("❌ Invalid file format: not a valid JSON file")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")


def render_reset_section(summary):
    """Render the reset/clear workspace section"""
    
    st.markdown("#### 🔄 Reset Workspace")
    
    if summary["total_state_items"] == 0:
        st.caption("⚪ Workspace is already empty")
        return
    
    st.caption("⚠️ Clear all project data and start fresh")
    
    with st.expander("⚠️ Danger Zone", expanded=False):
        st.warning("This will delete all your current work. Make sure to save first if needed!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("🗑️ Clear All Data", use_container_width=True):
                clear_project_state()
                st.success("✅ Workspace cleared")
                st.rerun()
        
        with col2:
            st.caption("This action cannot be undone")


def render_save_load_compact():
    """
    Render a compact version for sidebar integration
    Just the essential save/load buttons
    """
    st.markdown("### 💾 Project")
    
    summary = get_state_summary()
    
    # Save button
    if summary["total_state_items"] > 0:
        state_data = export_project_state()
        json_string = json.dumps(state_data, indent=2)
        default_filename = generate_project_filename()
        
        st.download_button(
            label="💾 Save",
            data=json_string,
            file_name=default_filename,
            mime="application/json",
            use_container_width=True,
            help=f"Download project ({summary['total_state_items']} items)"
        )
    else:
        st.button("💾 Save", disabled=True, use_container_width=True, help="No data to save")
    
    # Load button
    uploaded_file = st.file_uploader(
        "📂 Load",
        type=["json"],
        help="Upload a saved project file",
        label_visibility="collapsed",
        key="sidebar_project_uploader"
    )
    
    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read()
            data = json.loads(file_contents)
            
            success, message = load_project_state(data)
            
            if success:
                st.success("✅ Loaded!")
                st.rerun()
            else:
                st.error(f"❌ {message}")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:50]}")


def render_save_load_in_module():
    """
    Render save/load options within a module context
    Useful for module-specific save points
    """
    with st.sidebar:
        st.divider()
        render_save_load_compact()
