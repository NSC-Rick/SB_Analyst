"""
North Star Unified Shell - Business Valuation Logic
Multi-method valuation calculations with progressive unlock
"""


UNLOCK_RULES = {
    "revenue_multiple": {
        "requirements": ["revenue > 0"],
        "label": "Requires revenue",
        "conditions": {
            "revenue": {"threshold": 0, "operator": ">", "display": "Revenue detected"}
        }
    },
    "earnings_multiple": {
        "requirements": ["profit > 0"],
        "label": "Requires positive profit",
        "conditions": {
            "profit": {"threshold": 0, "operator": ">", "display": "Profit must be positive"}
        }
    },
    "weighted_value": {
        "requirements": ["revenue > 0", "profit > 0"],
        "label": "Requires revenue and profit",
        "conditions": {
            "revenue": {"threshold": 0, "operator": ">", "display": "Revenue detected"},
            "profit": {"threshold": 0, "operator": ">", "display": "Profit must be positive"}
        }
    },
    "dcf": {
        "requirements": ["future_implementation"],
        "label": "Future implementation",
        "conditions": {}
    },
    "industry_comps": {
        "requirements": ["future_implementation"],
        "label": "Future implementation",
        "conditions": {}
    }
}


def evaluate_unlock_conditions(core_financials):
    """
    Evaluate which unlock conditions are met
    
    Args:
        core_financials: Dict with revenue, profit, etc.
    
    Returns:
        dict: Condition name -> bool (met/not met)
    """
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    
    return {
        "revenue": revenue > 0,
        "profit": profit > 0,
        "has_revenue": revenue > 0,
        "has_profit": profit > 0,
        "is_profitable": profit > 0,
        "has_scale": revenue >= 50000
    }


def calculate_valuation_readiness_score(core_financials):
    """
    Calculate valuation readiness score (0-100%)
    
    Args:
        core_financials: Dict with revenue, profit, growth_rate
    
    Returns:
        float: Readiness score (0-100)
    """
    conditions = evaluate_unlock_conditions(core_financials)
    
    total_conditions = 2  # revenue and profit are the core conditions
    met_conditions = 0
    
    if conditions["revenue"]:
        met_conditions += 1
    
    if conditions["profit"]:
        met_conditions += 1
    
    score = (met_conditions / total_conditions) * 100
    
    return score


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


def generate_unlock_guidance(core_financials):
    """
    Generate actionable guidance for unlocking valuation methods
    
    Args:
        core_financials: Dict with revenue, profit, expenses
    
    Returns:
        list: Guidance strings with specific actions
    """
    guidance = []
    
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    expenses = core_financials.get("expenses", 0)
    
    if profit <= 0:
        guidance.append("**To unlock Earnings-Based Valuation:**")
        
        if revenue > 0 and expenses > 0:
            margin_gap = abs(profit)
            guidance.append(f"   • Reduce expenses by ${margin_gap:,.0f}/month to reach breakeven")
            
            if revenue > 0:
                needed_revenue = expenses - revenue
                guidance.append(f"   • OR increase revenue by ${needed_revenue:,.0f}/month to reach breakeven")
        
        guidance.append("   • Focus on improving profit margins")
        guidance.append("   • Review and optimize operating expenses")
        guidance.append("   • Consider pricing strategy adjustments")
    
    if revenue < 50000 and revenue > 0:
        guidance.append("**To improve valuation range:**")
        guidance.append("   • Scale revenue to $50K+/month for stronger valuation")
        guidance.append("   • Expand customer base or increase average transaction size")
        guidance.append("   • Explore new revenue streams or market segments")
    
    if revenue > 0 and profit > 0:
        profit_margin = (profit / revenue) * 100
        
        if profit_margin < 20:
            guidance.append("**To maximize valuation:**")
            guidance.append(f"   • Current margin: {profit_margin:.1f}% - aim for 20%+ for premium multiples")
            guidance.append("   • Improve operational efficiency")
            guidance.append("   • Optimize pricing and cost structure")
    
    if not guidance:
        guidance.append("**Excellent progress!**")
        guidance.append("   • All core valuation methods unlocked")
        guidance.append("   • Focus on scaling revenue and maintaining margins")
        guidance.append("   • Consider growth strategies to increase valuation multiples")
    
    return guidance


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


def get_method_status_detailed(core_financials):
    """
    Get detailed status of all valuation methods with unlock conditions
    
    Args:
        core_financials: Dict with financial data
    
    Returns:
        dict: Method name -> dict with status details
    """
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    conditions = evaluate_unlock_conditions(core_financials)
    
    return {
        "Revenue Multiple": {
            "available": revenue > 0,
            "icon": "✅" if revenue > 0 else "🔒",
            "description": "Value based on revenue multiples (1.5x - 4.0x annual revenue)",
            "conditions": [
                {"met": conditions["revenue"], "label": "Revenue detected"}
            ],
            "unlock_guidance": "Enter monthly revenue in Financial Modeler to unlock this method."
        },
        "Earnings Multiple": {
            "available": profit > 0,
            "icon": "✅" if profit > 0 else "🔒",
            "description": "Value based on profit multiples (3x - 6x annual profit)",
            "conditions": [
                {"met": conditions["revenue"], "label": "Revenue detected"},
                {"met": conditions["profit"], "label": "Profit must be positive"}
            ],
            "unlock_guidance": "Achieve positive profit by increasing revenue or reducing expenses."
        },
        "Weighted Value": {
            "available": revenue > 0 and profit > 0,
            "icon": "✅" if (revenue > 0 and profit > 0) else "🔒",
            "description": "Combined valuation using multiple methods",
            "conditions": [
                {"met": conditions["revenue"], "label": "Revenue detected"},
                {"met": conditions["profit"], "label": "Profit must be positive"}
            ],
            "unlock_guidance": "Unlock both Revenue and Earnings methods to access weighted valuation."
        },
        "DCF": {
            "available": False,
            "icon": "🔒",
            "description": "Discounted Cash Flow (Future implementation)",
            "conditions": [],
            "unlock_guidance": "Coming in future release - advanced cash flow projection method."
        },
        "Industry Comps": {
            "available": False,
            "icon": "🔒",
            "description": "Industry comparables (Future implementation)",
            "conditions": [],
            "unlock_guidance": "Coming in future release - industry benchmark comparison."
        }
    }


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
            "✅" if profit > 0 else "�",
            "Value based on profit multiples (3x - 6x annual profit)"
        ),
        "Weighted Value": (
            revenue > 0 and profit > 0,
            "✅" if (revenue > 0 and profit > 0) else "�",
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
