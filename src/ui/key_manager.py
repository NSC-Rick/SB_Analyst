"""
North Star Unified Shell - Key Manager
Centralized widget key generation to prevent DuplicateWidgetID errors
"""
import re
from typing import Set, Dict, List


def generate_nav_key(group_key: str, module_name: str, index: int) -> str:
    """
    Generate a globally unique navigation key for sidebar widgets.
    
    Args:
        group_key: The module group identifier (e.g., 'active_tools', 'intelligence')
        module_name: The display name of the module
        index: The position index within the group
    
    Returns:
        A unique, deterministic key string
    
    Example:
        generate_nav_key("active_tools", "Financial Modeler Lite", 0)
        -> "nav_active_tools_financial_modeler_lite_0"
    """
    safe_group = _sanitize_key_component(group_key)
    safe_name = _sanitize_key_component(module_name)
    
    return f"nav_{safe_group}_{safe_name}_{index}"


def _sanitize_key_component(component: str) -> str:
    """
    Sanitize a string component for use in widget keys.
    
    - Converts to lowercase
    - Replaces spaces with underscores
    - Removes special characters
    - Ensures no leading/trailing underscores
    
    Args:
        component: Raw string to sanitize
    
    Returns:
        Sanitized string safe for widget keys
    """
    component = component.lower()
    component = re.sub(r'[^\w\s-]', '', component)
    component = re.sub(r'[\s-]+', '_', component)
    component = component.strip('_')
    
    return component


def validate_unique_modules(module_groups: Dict) -> Dict[str, List[str]]:
    """
    Validate module configuration for duplicate module names.
    
    Args:
        module_groups: The MODULE_CONFIG["module_groups"] dictionary
    
    Returns:
        Dictionary mapping duplicate module names to their group locations
    
    Example:
        {
            "LOC Analyzer": ["intelligence", "intelligence"],
            "Funding Engine": ["intelligence", "intelligence"]
        }
    """
    module_registry: Dict[str, List[str]] = {}
    duplicates: Dict[str, List[str]] = {}
    
    for group_key, group_data in module_groups.items():
        for module in group_data.get("modules", []):
            module_name = module.get("name", "")
            
            if module_name in module_registry:
                module_registry[module_name].append(group_key)
                duplicates[module_name] = module_registry[module_name]
            else:
                module_registry[module_name] = [group_key]
    
    return duplicates


def get_module_collision_report(module_groups: Dict) -> str:
    """
    Generate a human-readable report of module name collisions.
    
    Args:
        module_groups: The MODULE_CONFIG["module_groups"] dictionary
    
    Returns:
        Formatted string report of duplicates, or empty string if none found
    """
    duplicates = validate_unique_modules(module_groups)
    
    if not duplicates:
        return ""
    
    report_lines = ["⚠️ **Duplicate Module Names Detected:**\n"]
    
    for module_name, groups in duplicates.items():
        report_lines.append(f"- **{module_name}** appears {len(groups)} times in groups: {', '.join(groups)}")
    
    report_lines.append("\n*Keys are now unique per group+index, but consider renaming for clarity.*")
    
    return "\n".join(report_lines)


def generate_debug_key_map(module_groups: Dict) -> Dict[str, str]:
    """
    Generate a complete mapping of all module names to their generated keys.
    
    Useful for debugging and verification.
    
    Args:
        module_groups: The MODULE_CONFIG["module_groups"] dictionary
    
    Returns:
        Dictionary mapping display paths to generated keys
    """
    key_map = {}
    
    for group_key, group_data in module_groups.items():
        for index, module in enumerate(group_data.get("modules", [])):
            module_name = module.get("name", "")
            generated_key = generate_nav_key(group_key, module_name, index)
            
            display_path = f"{group_data.get('title', group_key)} → {module_name} (#{index})"
            key_map[display_path] = generated_key
    
    return key_map
