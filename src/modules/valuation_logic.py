"""
North Star Unified Shell - Business Valuation Logic
Multi-method valuation calculations with progressive unlock
"""


def calculate_valuation_completeness(core_financials):
    """
    Calculate valuation completeness score based on available data
    
    Args:
        core_financials: Dict with revenue, profit, growth_rate
    
    Returns:
        int: Completeness score (0-100)
    """
    score = 0
    
    if core_financials.get("revenue", 0) > 0:
        score += 40
    
    if core_financials.get("profit", 0) > 0:
        score += 40
    
    if core_financials.get("growth_rate", 0) > 0:
        score += 20
    
    return score


def is_method_available(method_name, core_financials):
    """
    Check if a valuation method is available based on data
    
    Args:
        method_name: Name of valuation method
        core_financials: Dict with financial data
    
    Returns:
        bool: True if method is available
    """
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    
    if method_name == "revenue_multiple":
        return revenue > 0
    
    elif method_name == "earnings_multiple":
        return profit > 0
    
    elif method_name == "weighted_value":
        return revenue > 0 and profit > 0
    
    elif method_name in ["dcf", "industry_comps", "pre_revenue"]:
        return False  # Locked for future implementation
    
    return False


def calculate_revenue_multiple_valuation(revenue):
    """
    Calculate valuation using revenue multiples
    
    Args:
        revenue: Monthly revenue
    
    Returns:
        tuple: (low_value, high_value)
    """
    annual_revenue = revenue * 12
    
    low = annual_revenue * 1.5
    high = annual_revenue * 4.0
    
    return (low, high)


def calculate_earnings_multiple_valuation(profit):
    """
    Calculate valuation using earnings/profit multiples
    
    Args:
        profit: Monthly profit
    
    Returns:
        tuple: (low_value, high_value)
    """
    annual_profit = profit * 12
    
    low = annual_profit * 3.0
    high = annual_profit * 6.0
    
    return (low, high)


def calculate_weighted_valuation(revenue, profit):
    """
    Calculate weighted average valuation combining revenue and earnings methods
    
    Args:
        revenue: Monthly revenue
        profit: Monthly profit
    
    Returns:
        tuple: (low_value, high_value)
    """
    rev_low, rev_high = calculate_revenue_multiple_valuation(revenue)
    earn_low, earn_high = calculate_earnings_multiple_valuation(profit)
    
    weighted_low = (rev_low + earn_low) / 2
    weighted_high = (rev_high + earn_high) / 2
    
    return (weighted_low, weighted_high)


def calculate_primary_valuation(core_financials):
    """
    Calculate primary valuation range based on available data
    
    Args:
        core_financials: Dict with revenue, profit, etc.
    
    Returns:
        tuple: (low_value, high_value, method_used)
    """
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    
    if revenue > 0 and profit > 0:
        low, high = calculate_weighted_valuation(revenue, profit)
        return (low, high, "Weighted Value")
    
    elif profit > 0:
        low, high = calculate_earnings_multiple_valuation(profit)
        return (low, high, "Earnings Multiple")
    
    elif revenue > 0:
        low, high = calculate_revenue_multiple_valuation(revenue)
        return (low, high, "Revenue Multiple")
    
    return (0, 0, "Insufficient Data")


def generate_valuation_insights(core_financials):
    """
    Generate insights based on financial data
    
    Args:
        core_financials: Dict with revenue, profit, expenses, growth_rate
    
    Returns:
        list: Insight strings
    """
    insights = []
    
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    growth_rate = core_financials.get("growth_rate", 0)
    
    if revenue > 0 and profit > 0:
        profit_margin = (profit / revenue) * 100
        
        if profit_margin > 20:
            insights.append("💎 Strong profit margins (>20%) support higher valuation multiples and investor appeal.")
        elif profit_margin > 10:
            insights.append("📊 Moderate profit margins suggest room for operational improvement to increase value.")
        else:
            insights.append("⚠️ Low profit margins may constrain valuation. Focus on margin improvement strategies.")
    
    if revenue > 0:
        if revenue < 100000:
            insights.append("📈 Limited revenue scale may constrain current valuation. Growth can significantly increase value.")
        elif revenue > 1000000:
            insights.append("🚀 Strong revenue base provides solid foundation for valuation and growth potential.")
    
    if profit > 0:
        insights.append("✅ Positive profitability unlocks earnings-based valuation methods and increases investor confidence.")
    elif profit < 0:
        insights.append("💡 Current losses limit valuation options. Path to profitability is critical for value creation.")
    
    if growth_rate > 0.15:
        insights.append("🚀 Strong growth rate (>15%/month) supports higher valuation multiples.")
    elif growth_rate > 0:
        insights.append("📈 Positive growth trajectory adds value beyond current performance.")
    
    return insights


def calculate_scenario_valuation(core_financials, margin_improvement=0.2):
    """
    Calculate scenario valuation with improved margins
    
    Args:
        core_financials: Dict with revenue, profit, expenses
        margin_improvement: Decimal improvement (0.2 = 20% improvement)
    
    Returns:
        tuple: (scenario_low, scenario_high) or None if not applicable
    """
    profit = core_financials.get("profit", 0)
    
    if profit <= 0:
        return None
    
    improved_profit = profit * (1 + margin_improvement)
    
    low, high = calculate_earnings_multiple_valuation(improved_profit)
    
    return (low, high)


def get_value_drivers():
    """
    Get list of key value drivers
    
    Returns:
        list: Value driver descriptions
    """
    return [
        "📈 **Revenue Scale**: Increasing revenue directly expands valuation range",
        "💰 **Profit Margin**: Strong margins significantly increase earnings-based valuations",
        "🚀 **Growth Rate**: Demonstrated growth potential increases investor confidence and multiples"
    ]


def get_method_status(core_financials):
    """
    Get status of all valuation methods
    
    Args:
        core_financials: Dict with financial data
    
    Returns:
        dict: Method name -> (available, icon, description)
    """
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    
    return {
        "Revenue Multiple": (
            revenue > 0,
            "✅" if revenue > 0 else "🔒",
            "Value based on revenue multiples (1.5x - 4.0x annual revenue)"
        ),
        "Earnings Multiple": (
            profit > 0,
            "✅" if profit > 0 else "🔓",
            "Value based on profit multiples (3x - 6x annual profit)"
        ),
        "Weighted Value": (
            revenue > 0 and profit > 0,
            "✅" if (revenue > 0 and profit > 0) else "🔓",
            "Combined valuation using multiple methods"
        ),
        "DCF": (
            False,
            "🔒",
            "Discounted Cash Flow (Future implementation)"
        ),
        "Industry Comps": (
            False,
            "🔒",
            "Industry comparables (Future implementation)"
        )
    }
