"""
North Star Unified Shell - Valuation Logic Module
Progressive unlock valuation system with tiered methods
"""


class ValuationTier:
    """Represents a valuation method tier with unlock conditions"""
    
    def __init__(self, name, description, required_fields, icon_locked, icon_unlocked):
        self.name = name
        self.description = description
        self.required_fields = required_fields
        self.icon_locked = icon_locked
        self.icon_unlocked = icon_unlocked
    
    def is_unlocked(self, data):
        """Check if this tier is unlocked based on available data"""
        for field in self.required_fields:
            if field not in data or data[field] is None or data[field] == 0:
                return False
        return True


VALUATION_TIERS = {
    "revenue_multiple": ValuationTier(
        name="Revenue Multiple",
        description="Value based on revenue multiples (1.5x - 4.0x)",
        required_fields=["revenue"],
        icon_locked="🔒",
        icon_unlocked="✅"
    ),
    "earnings_multiple": ValuationTier(
        name="Earnings Multiple",
        description="Value based on profit multiples (3x - 6x)",
        required_fields=["profit"],
        icon_locked="🔓",
        icon_unlocked="✅"
    ),
    "weighted_value": ValuationTier(
        name="Weighted Value",
        description="Combined valuation using multiple methods",
        required_fields=["revenue", "profit"],
        icon_locked="🔒",
        icon_unlocked="✅"
    ),
    "dcf": ValuationTier(
        name="Discounted Cash Flow (DCF)",
        description="Advanced cash flow-based valuation",
        required_fields=["revenue", "profit", "growth_rate", "cash_flow"],
        icon_locked="🔒",
        icon_unlocked="✅"
    )
}


def calculate_completion_score(data):
    """
    Calculate valuation readiness score based on data completeness
    
    Args:
        data: Dictionary with revenue, expenses, profit, etc.
    
    Returns:
        int: Completion score (0-100)
    """
    score = 0
    
    if data.get("revenue") and data["revenue"] > 0:
        score += 40
    
    if data.get("expenses") and data["expenses"] > 0:
        score += 30
    
    if data.get("profit") is not None:
        score += 30
    
    return min(score, 100)


def calculate_revenue_multiple(revenue):
    """
    Calculate valuation using revenue multiple method
    
    Args:
        revenue: Annual or monthly revenue
    
    Returns:
        dict: {"low": float, "high": float, "method": str}
    """
    low_multiple = 1.5
    high_multiple = 4.0
    
    return {
        "low": revenue * low_multiple,
        "high": revenue * high_multiple,
        "method": "Revenue Multiple",
        "multiple_range": f"{low_multiple}x - {high_multiple}x"
    }


def calculate_earnings_multiple(profit):
    """
    Calculate valuation using earnings multiple method
    
    Args:
        profit: Annual or monthly profit
    
    Returns:
        dict: {"low": float, "high": float, "method": str}
    """
    low_multiple = 3.0
    high_multiple = 6.0
    
    return {
        "low": profit * low_multiple,
        "high": profit * high_multiple,
        "method": "Earnings Multiple",
        "multiple_range": f"{low_multiple}x - {high_multiple}x"
    }


def calculate_weighted_value(revenue, profit):
    """
    Calculate weighted average valuation (future implementation)
    
    Args:
        revenue: Annual or monthly revenue
        profit: Annual or monthly profit
    
    Returns:
        dict: {"low": float, "high": float, "method": str}
    """
    revenue_val = calculate_revenue_multiple(revenue)
    earnings_val = calculate_earnings_multiple(profit)
    
    weight_revenue = 0.4
    weight_earnings = 0.6
    
    low = (revenue_val["low"] * weight_revenue) + (earnings_val["low"] * weight_earnings)
    high = (revenue_val["high"] * weight_revenue) + (earnings_val["high"] * weight_earnings)
    
    return {
        "low": low,
        "high": high,
        "method": "Weighted Average",
        "weights": f"Revenue {weight_revenue*100:.0f}% / Earnings {weight_earnings*100:.0f}%"
    }


def get_available_methods(data):
    """
    Get list of available valuation methods based on data
    
    Args:
        data: Dictionary with revenue, expenses, profit, etc.
    
    Returns:
        list: Available method names
    """
    available = []
    
    for method_key, tier in VALUATION_TIERS.items():
        if tier.is_unlocked(data):
            available.append(method_key)
    
    return available


def get_locked_methods(data):
    """
    Get list of locked valuation methods with unlock requirements
    
    Args:
        data: Dictionary with revenue, expenses, profit, etc.
    
    Returns:
        list: Tuples of (method_name, missing_fields)
    """
    locked = []
    
    for method_key, tier in VALUATION_TIERS.items():
        if not tier.is_unlocked(data):
            missing = [field for field in tier.required_fields 
                      if field not in data or data[field] is None or data[field] == 0]
            locked.append((tier.name, missing))
    
    return locked


def generate_valuation_insights(data, valuations):
    """
    Generate insights based on valuation results
    
    Args:
        data: Input data dictionary
        valuations: List of valuation results
    
    Returns:
        list: Insight strings
    """
    insights = []
    
    if data.get("profit") and data.get("revenue"):
        profit_margin = (data["profit"] / data["revenue"]) * 100
        
        if profit_margin > 20:
            insights.append("💎 Strong profit margins (>20%) support higher valuation multiples and investor appeal.")
        elif profit_margin > 10:
            insights.append("📊 Moderate profit margins suggest room for operational improvement to increase value.")
        else:
            insights.append("⚠️ Low profit margins may constrain valuation. Focus on margin improvement strategies.")
    
    if data.get("revenue"):
        if data["revenue"] < 100000:
            insights.append("📈 Limited revenue scale may constrain current valuation. Growth can significantly increase value.")
        elif data["revenue"] > 1000000:
            insights.append("🚀 Strong revenue base provides solid foundation for valuation and growth potential.")
    
    if data.get("profit") and data["profit"] > 0:
        insights.append("✅ Positive profitability unlocks earnings-based valuation methods and increases investor confidence.")
    elif data.get("profit") and data["profit"] < 0:
        insights.append("💡 Current losses limit valuation options. Path to profitability is critical for value creation.")
    
    if len(valuations) > 1:
        values = [v["high"] for v in valuations]
        if max(values) / min(values) > 2:
            insights.append("🔍 Wide valuation range suggests different methods weight factors differently. Consider multiple perspectives.")
    
    return insights


def get_value_drivers():
    """
    Get list of key value drivers for education
    
    Returns:
        list: Value driver descriptions
    """
    return [
        "📈 **Revenue Growth**: Increasing revenue directly expands valuation range across all methods",
        "💰 **Profitability**: Strong margins significantly increase earnings-based valuations",
        "📊 **Margin Improvement**: Even small margin gains can dramatically increase business value",
        "🎯 **Consistency**: Stable, predictable performance commands higher multiples",
        "🚀 **Growth Trajectory**: Demonstrated growth potential increases investor confidence and multiples"
    ]


def get_unlock_guidance(missing_fields):
    """
    Get user-friendly guidance for unlocking methods
    
    Args:
        missing_fields: List of missing field names
    
    Returns:
        str: Guidance message
    """
    field_map = {
        "revenue": "revenue data",
        "profit": "profit/earnings data (complete expense inputs)",
        "expenses": "expense data",
        "growth_rate": "growth rate projections",
        "cash_flow": "cash flow information"
    }
    
    readable_fields = [field_map.get(f, f) for f in missing_fields]
    
    if len(readable_fields) == 1:
        return f"Add {readable_fields[0]} to unlock this method"
    else:
        return f"Add {', '.join(readable_fields)} to unlock this method"
