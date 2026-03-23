"""
Valuation Distribution Curve Logic
Probabilistic valuation analysis with uncertainty visualization
"""
import numpy as np
from scipy import stats


def collect_valuation_methods(core_financials):
    """
    Collect all available valuation method results
    
    Args:
        core_financials: Core financial data
    
    Returns:
        dict: Available method values
    """
    from src.modules.valuation_logic import (
        calculate_revenue_multiple_valuation,
        calculate_earnings_multiple_valuation,
        is_method_available
    )
    
    methods = {}
    
    # Revenue Multiple Method
    if is_method_available("revenue", core_financials):
        revenue_val = calculate_revenue_multiple_valuation(core_financials)
        if revenue_val:
            methods["revenue_method"] = revenue_val["mid"]
    
    # Earnings Multiple Method
    if is_method_available("earnings", core_financials):
        earnings_val = calculate_earnings_multiple_valuation(core_financials)
        if earnings_val:
            methods["earnings_method"] = earnings_val["mid"]
    
    # Asset Method (simplified - based on cash + revenue/4)
    revenue = core_financials.get("revenue", 0)
    cash = core_financials.get("cash_on_hand", 0)
    if revenue > 0:
        asset_value = cash + (revenue * 12 / 4)  # Cash + 3 months revenue
        methods["asset_method"] = asset_value
    
    return methods


def calculate_distribution_stats(methods):
    """
    Calculate mean, std dev, min, max from valuation methods
    
    Args:
        methods: Dict of method values
    
    Returns:
        dict: Distribution statistics
    """
    if not methods:
        return None
    
    values = list(methods.values())
    
    if len(values) == 0:
        return None
    
    mean_val = np.mean(values)
    
    # Calculate std dev
    if len(values) == 1:
        # Single method - use 20% of value as std dev
        std_dev = mean_val * 0.20
    else:
        std_dev = np.std(values, ddof=1)
    
    # Ensure minimum std dev (at least 10% of mean)
    min_std_dev = mean_val * 0.10
    std_dev = max(std_dev, min_std_dev)
    
    return {
        "mean": mean_val,
        "std_dev": std_dev,
        "min": min(values),
        "max": max(values),
        "count": len(values),
        "values": values,
    }


def generate_distribution_curve(mean, std_dev, num_points=200):
    """
    Generate normal distribution curve data
    
    Args:
        mean: Mean valuation
        std_dev: Standard deviation
        num_points: Number of points in curve
    
    Returns:
        tuple: (x_values, y_values)
    """
    # Generate x range: mean ± 3 std deviations
    x_min = max(0, mean - 3 * std_dev)  # Don't go negative
    x_max = mean + 3 * std_dev
    
    x_values = np.linspace(x_min, x_max, num_points)
    
    # Calculate normal distribution
    y_values = stats.norm.pdf(x_values, mean, std_dev)
    
    return x_values, y_values


def calculate_confidence_intervals(mean, std_dev):
    """
    Calculate confidence intervals for distribution
    
    Args:
        mean: Mean valuation
        std_dev: Standard deviation
    
    Returns:
        dict: Confidence intervals
    """
    # 68% confidence interval (±1 std dev)
    ci_68_low = max(0, mean - std_dev)
    ci_68_high = mean + std_dev
    
    # 95% confidence interval (±2 std dev)
    ci_95_low = max(0, mean - 2 * std_dev)
    ci_95_high = mean + 2 * std_dev
    
    return {
        "ci_68": {
            "low": ci_68_low,
            "high": ci_68_high,
            "range": ci_68_high - ci_68_low,
        },
        "ci_95": {
            "low": ci_95_low,
            "high": ci_95_high,
            "range": ci_95_high - ci_95_low,
        },
    }


def calculate_variability_level(std_dev, mean):
    """
    Determine variability level of valuation
    
    Args:
        std_dev: Standard deviation
        mean: Mean valuation
    
    Returns:
        dict: Variability assessment
    """
    # Calculate coefficient of variation (CV)
    cv = (std_dev / mean) * 100 if mean > 0 else 0
    
    if cv < 15:
        level = "Low"
        color = "green"
        message = "Valuation methods show strong agreement"
        icon = "✅"
    elif cv < 30:
        level = "Moderate"
        color = "orange"
        message = "Some variability between valuation methods"
        icon = "⚠️"
    else:
        level = "High"
        color = "red"
        message = "High variability between valuation methods - consider gathering more data"
        icon = "❌"
    
    return {
        "level": level,
        "cv": cv,
        "color": color,
        "message": message,
        "icon": icon,
    }


def generate_distribution_summary(stats, confidence_intervals, variability):
    """
    Generate summary statistics for display
    
    Args:
        stats: Distribution statistics
        confidence_intervals: Confidence intervals
        variability: Variability assessment
    
    Returns:
        dict: Summary for display
    """
    return {
        "mean_valuation": stats["mean"],
        "std_deviation": stats["std_dev"],
        "confidence_68": {
            "low": confidence_intervals["ci_68"]["low"],
            "mid": stats["mean"],
            "high": confidence_intervals["ci_68"]["high"],
        },
        "confidence_95": {
            "low": confidence_intervals["ci_95"]["low"],
            "mid": stats["mean"],
            "high": confidence_intervals["ci_95"]["high"],
        },
        "variability": variability,
        "method_count": stats["count"],
    }


def calculate_weighted_distribution(methods, weights=None):
    """
    Calculate weighted distribution (future enhancement)
    
    Args:
        methods: Dict of method values
        weights: Optional dict of weights per method
    
    Returns:
        dict: Weighted statistics
    """
    if not weights:
        # Default equal weights
        weights = {method: 1.0 / len(methods) for method in methods}
    
    # Normalize weights
    total_weight = sum(weights.values())
    normalized_weights = {k: v / total_weight for k, v in weights.items()}
    
    # Calculate weighted mean
    weighted_mean = sum(methods[m] * normalized_weights.get(m, 0) for m in methods)
    
    # Calculate weighted variance
    weighted_variance = sum(
        normalized_weights.get(m, 0) * (methods[m] - weighted_mean) ** 2
        for m in methods
    )
    weighted_std_dev = np.sqrt(weighted_variance)
    
    return {
        "mean": weighted_mean,
        "std_dev": weighted_std_dev,
        "weights": normalized_weights,
    }


def adjust_confidence_manually(mean, std_dev, confidence_adjustment=1.0):
    """
    Allow manual adjustment of confidence intervals (future enhancement)
    
    Args:
        mean: Mean valuation
        std_dev: Standard deviation
        confidence_adjustment: Multiplier for std dev (0.5 = tighter, 2.0 = wider)
    
    Returns:
        float: Adjusted std dev
    """
    adjusted_std_dev = std_dev * confidence_adjustment
    
    # Ensure minimum 5% of mean
    min_std_dev = mean * 0.05
    adjusted_std_dev = max(adjusted_std_dev, min_std_dev)
    
    return adjusted_std_dev


def get_distribution_percentiles(mean, std_dev):
    """
    Calculate key percentiles for distribution
    
    Args:
        mean: Mean valuation
        std_dev: Standard deviation
    
    Returns:
        dict: Percentile values
    """
    return {
        "p10": max(0, mean - 1.28 * std_dev),  # 10th percentile
        "p25": max(0, mean - 0.67 * std_dev),  # 25th percentile
        "p50": mean,  # Median (50th percentile)
        "p75": mean + 0.67 * std_dev,  # 75th percentile
        "p90": mean + 1.28 * std_dev,  # 90th percentile
    }
