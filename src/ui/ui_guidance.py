"""
North Star Unified Shell - UI Guidance System
Standardized, reusable user guidance across all modules
"""
import streamlit as st


def is_guidance_enabled():
    """
    Check if guidance is enabled in session state
    
    Returns:
        bool: True if guidance should be shown
    """
    if "show_guidance" not in st.session_state:
        st.session_state.show_guidance = True
    
    return st.session_state.show_guidance


def show_tooltip(label, help_key):
    """
    Display label with tooltip icon that shows help text
    
    Args:
        label: Label text to display
        help_key: Key to look up in help registry
    
    Returns:
        str: Label with tooltip if guidance enabled
    """
    if not is_guidance_enabled():
        return label
    
    from src.ui.help_content import get_help_content
    
    help_text = get_help_content(help_key, "tooltip")
    
    if help_text:
        return f"{label} ℹ️"
    
    return label


def show_info(text, help_key=None):
    """
    Display inline info bubble with guidance text
    
    Args:
        text: Text to display in info bubble
        help_key: Optional key to look up additional detail
    """
    if not is_guidance_enabled():
        return
    
    if help_key:
        from src.ui.help_content import get_help_content
        detail = get_help_content(help_key, "detail")
        if detail:
            text = f"{text}\n\n{detail}"
    
    st.info(text)


def show_prompt(condition, message, help_key=None, prompt_type="info"):
    """
    Display contextual guidance when condition is met
    
    Args:
        condition: Boolean condition to check
        message: Message to display if condition is True
        help_key: Optional key for additional help
        prompt_type: Type of prompt ("info", "warning", "success", "error")
    """
    if not is_guidance_enabled():
        return
    
    if not condition:
        return
    
    if help_key:
        from src.ui.help_content import get_help_content
        detail = get_help_content(help_key, "detail")
        if detail:
            message = f"{message}\n\n{detail}"
    
    if prompt_type == "info":
        st.info(message)
    elif prompt_type == "warning":
        st.warning(message)
    elif prompt_type == "success":
        st.success(message)
    elif prompt_type == "error":
        st.error(message)


def show_modal(trigger_label, title, content, help_key=None):
    """
    Display popup modal with extended explanation
    
    Args:
        trigger_label: Label for button/link that triggers modal
        title: Modal title
        content: Modal content (markdown supported)
        help_key: Optional key for help content
    
    Returns:
        bool: True if modal was opened
    """
    if not is_guidance_enabled():
        return False
    
    if help_key:
        from src.ui.help_content import get_help_content
        detail = get_help_content(help_key, "detail")
        if detail:
            content = f"{content}\n\n---\n\n{detail}"
    
    # Use expander as modal alternative (Streamlit doesn't have native modals)
    with st.expander(f"ℹ️ {trigger_label}"):
        st.markdown(f"### {title}")
        st.markdown(content)
        return True
    
    return False


def show_help_icon(help_key):
    """
    Display standalone help icon with tooltip
    
    Args:
        help_key: Key to look up in help registry
    """
    if not is_guidance_enabled():
        return
    
    from src.ui.help_content import get_help_content
    
    tooltip = get_help_content(help_key, "tooltip")
    detail = get_help_content(help_key, "detail")
    
    if tooltip:
        st.caption(f"ℹ️ {tooltip}")
        
        if detail:
            with st.expander("Learn more"):
                st.markdown(detail)


def show_contextual_help(context_type, **kwargs):
    """
    Show contextual help based on current state
    
    Args:
        context_type: Type of context ("empty_revenue", "incomplete_data", etc.)
        **kwargs: Additional context data
    """
    if not is_guidance_enabled():
        return
    
    from src.ui.help_content import get_contextual_help
    
    help_data = get_contextual_help(context_type, **kwargs)
    
    if not help_data:
        return
    
    message = help_data.get("message", "")
    prompt_type = help_data.get("type", "info")
    
    if prompt_type == "info":
        st.info(message)
    elif prompt_type == "warning":
        st.warning(message)
    elif prompt_type == "success":
        st.success(message)


def show_field_help(label, help_key, field_type="text"):
    """
    Display field label with integrated help
    
    Args:
        label: Field label
        help_key: Help registry key
        field_type: Type of field for context
    
    Returns:
        str: Enhanced label with help
    """
    if not is_guidance_enabled():
        return label
    
    from src.ui.help_content import get_help_content
    
    tooltip = get_help_content(help_key, "tooltip")
    
    if tooltip:
        return f"{label} ℹ️"
    
    return label


def render_help_toggle():
    """
    Render global help toggle for sidebar
    Should be called in sidebar
    """
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    current_state = is_guidance_enabled()
    
    show_guidance = st.toggle(
        "Show Guidance",
        value=current_state,
        help="Toggle contextual help and tooltips throughout the app"
    )
    
    st.session_state.show_guidance = show_guidance
    
    if show_guidance:
        st.caption("✅ Guidance enabled")
    else:
        st.caption("Guidance disabled")


def show_module_intro(module_name, description, help_key=None):
    """
    Display module introduction with optional help
    
    Args:
        module_name: Name of the module
        description: Short description
        help_key: Optional help key for extended info
    """
    if not is_guidance_enabled():
        return
    
    if help_key:
        from src.ui.help_content import get_help_content
        detail = get_help_content(help_key, "detail")
        
        if detail:
            with st.expander(f"ℹ️ About {module_name}"):
                st.markdown(detail)


def show_smart_prompt_empty_revenue():
    """Smart prompt for empty revenue state"""
    show_prompt(
        condition=True,
        message="💡 **Get Started:** Enter your monthly revenue to unlock financial projections and valuation analysis",
        prompt_type="info"
    )


def show_smart_prompt_incomplete_data():
    """Smart prompt for incomplete data state"""
    show_prompt(
        condition=True,
        message="📊 **Improve Accuracy:** Complete additional financial fields to increase valuation precision and unlock advanced methods",
        prompt_type="info"
    )


def show_smart_prompt_no_profit():
    """Smart prompt for no profit state"""
    show_prompt(
        condition=True,
        message="⚠️ **Note:** Current losses limit earnings-based valuation. Focus on path to profitability to unlock additional methods.",
        prompt_type="warning"
    )


def show_smart_prompt_high_variability():
    """Smart prompt for high valuation variability"""
    show_prompt(
        condition=True,
        message="⚠️ **High Uncertainty:** Valuation methods show significant disagreement. Consider refining financial inputs or gathering additional data.",
        prompt_type="warning"
    )


def show_input_help(label, help_key, input_widget, **widget_kwargs):
    """
    Wrapper to show input with integrated help
    
    Args:
        label: Input label
        help_key: Help registry key
        input_widget: Streamlit input function (st.number_input, st.text_input, etc.)
        **widget_kwargs: Arguments to pass to input widget
    
    Returns:
        Input widget return value
    """
    from src.ui.help_content import get_help_content
    
    # Get help text
    help_text = get_help_content(help_key, "tooltip") if is_guidance_enabled() else None
    
    # Add help to widget kwargs if not already present
    if help_text and "help" not in widget_kwargs:
        widget_kwargs["help"] = help_text
    
    # Call input widget
    return input_widget(label, **widget_kwargs)


def show_section_help(section_title, help_key):
    """
    Display section header with help icon
    
    Args:
        section_title: Section title (markdown)
        help_key: Help registry key
    """
    if not is_guidance_enabled():
        st.markdown(section_title)
        return
    
    from src.ui.help_content import get_help_content
    
    col1, col2 = st.columns([10, 1])
    
    with col1:
        st.markdown(section_title)
    
    with col2:
        tooltip = get_help_content(help_key, "tooltip")
        detail = get_help_content(help_key, "detail")
        
        if tooltip or detail:
            if st.button("ℹ️", key=f"help_{help_key}"):
                st.session_state[f"show_help_{help_key}"] = True
    
    # Show detail if button clicked
    if st.session_state.get(f"show_help_{help_key}"):
        detail = get_help_content(help_key, "detail")
        if detail:
            st.info(detail)
            if st.button("Close", key=f"close_help_{help_key}"):
                st.session_state[f"show_help_{help_key}"] = False
                st.rerun()


def show_onboarding_checklist(module_name, required_steps):
    """
    Display onboarding checklist for module
    
    Args:
        module_name: Name of the module
        required_steps: List of (step_name, completed) tuples
    """
    if not is_guidance_enabled():
        return
    
    with st.expander(f"📋 {module_name} Setup Checklist"):
        for step_name, completed in required_steps:
            icon = "✅" if completed else "⬜"
            st.markdown(f"{icon} {step_name}")
        
        completed_count = sum(1 for _, completed in required_steps if completed)
        total_count = len(required_steps)
        
        if completed_count == total_count:
            st.success("All steps completed!")
        else:
            st.caption(f"{completed_count}/{total_count} steps completed")
