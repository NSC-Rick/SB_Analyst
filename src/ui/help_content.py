"""
North Star Unified Shell - Help Content Registry
Centralized help text and guidance content for all UI elements
"""


HELP_CONTENT = {
    # Financial Modeler Lite
    "revenue_input": {
        "tooltip": "Enter your expected monthly revenue",
        "detail": "Use realistic projections based on past performance, market research, or conservative assumptions. This is the foundation for all financial analysis."
    },
    "expenses_input": {
        "tooltip": "Enter your total monthly expenses",
        "detail": "Include all costs: COGS, operating expenses, payroll, rent, utilities, marketing, etc. Be comprehensive to get accurate profit calculations."
    },
    "growth_rate_input": {
        "tooltip": "Expected monthly revenue growth rate",
        "detail": "Conservative: 2-5% | Moderate: 5-10% | Aggressive: 10-20%. Base this on market conditions, sales pipeline, and historical data."
    },
    "projection_months": {
        "tooltip": "How many months to project forward",
        "detail": "12 months = 1 year view | 24 months = 2 year view | 36 months = 3 year view. Longer projections have more uncertainty."
    },
    "cogs_percent": {
        "tooltip": "Cost of Goods Sold as percentage of revenue",
        "detail": "Direct costs to produce/deliver your product or service. Typical ranges: Services 20-40% | Products 40-60% | Manufacturing 50-70%."
    },
    "fixed_costs": {
        "tooltip": "Monthly costs that don't vary with revenue",
        "detail": "Rent, salaries, insurance, software subscriptions, utilities. These stay constant regardless of sales volume."
    },
    "variable_costs": {
        "tooltip": "Costs that scale with revenue",
        "detail": "Sales commissions, transaction fees, shipping, materials. These increase as revenue grows."
    },
    
    # Financial Modeler Pro
    "revenue_streams": {
        "tooltip": "Model multiple revenue sources separately",
        "detail": "Break down revenue by product line, service type, or customer segment. Each stream can have different pricing and growth rates."
    },
    "stream_price": {
        "tooltip": "Average price per unit or transaction",
        "detail": "Use your actual pricing or average transaction value. This will be multiplied by volume to calculate stream revenue."
    },
    "stream_volume": {
        "tooltip": "Number of units sold per month",
        "detail": "Monthly transaction count, units sold, or customer count. Be realistic based on capacity and market demand."
    },
    "stream_growth": {
        "tooltip": "Monthly growth rate for this revenue stream",
        "detail": "Each stream can grow at different rates. Consider market maturity, competition, and sales capacity."
    },
    "labor_costs": {
        "tooltip": "Employee compensation and benefits",
        "detail": "Include salaries, wages, payroll taxes, benefits, and contractor costs. This is often the largest expense category."
    },
    
    # Valuation Engine
    "valuation_curve": {
        "tooltip": "Probabilistic valuation distribution",
        "detail": "This curve shows the probability distribution of your business value based on multiple valuation methods. Shaded areas represent confidence intervals: darker = higher confidence."
    },
    "valuation_mean": {
        "tooltip": "Average valuation across all methods",
        "detail": "The mean represents the central estimate of your business value. It's calculated by averaging all available valuation methods."
    },
    "valuation_std_dev": {
        "tooltip": "Standard deviation of valuation estimates",
        "detail": "Measures the spread of valuation methods. Lower = methods agree more. Higher = more uncertainty in the estimate."
    },
    "confidence_68": {
        "tooltip": "68% confidence interval",
        "detail": "There's a 68% probability your true business value falls within this range. This represents ±1 standard deviation from the mean."
    },
    "confidence_95": {
        "tooltip": "95% confidence interval",
        "detail": "There's a 95% probability your true business value falls within this range. This represents ±2 standard deviations from the mean."
    },
    "variability_level": {
        "tooltip": "Agreement level between valuation methods",
        "detail": "Low = methods agree strongly (reliable estimate) | Moderate = some disagreement | High = significant disagreement (gather more data)"
    },
    "revenue_multiple": {
        "tooltip": "Valuation based on revenue multiples",
        "detail": "Values your business as a multiple of annual revenue (typically 1.5x - 4.0x). Best for early-stage or high-growth businesses."
    },
    "earnings_multiple": {
        "tooltip": "Valuation based on earnings/profit multiples",
        "detail": "Values your business as a multiple of annual profit (typically 3x - 6x). Best for profitable, established businesses."
    },
    "asset_method": {
        "tooltip": "Valuation based on asset value",
        "detail": "Values your business based on cash and near-term revenue potential. Conservative method, often used as a floor value."
    },
    
    # LOC Analyzer
    "loc_recommendation": {
        "tooltip": "Recommended line of credit amount",
        "detail": "Based on your cash flow trough analysis. This is the working capital needed to cover gaps between expenses and revenue."
    },
    "cash_trough": {
        "tooltip": "Lowest point in your cash flow projection",
        "detail": "The point where you'll have the least cash on hand. This determines your working capital needs."
    },
    "utilization_rate": {
        "tooltip": "Expected usage of your line of credit",
        "detail": "How much of the LOC you'll likely use on average. Lower utilization = better credit terms and lower costs."
    },
    
    # Project Evaluator
    "project_score": {
        "tooltip": "Overall project viability score (0-100)",
        "detail": "Composite score based on market opportunity, financial viability, execution feasibility, and risk assessment."
    },
    "priority_classification": {
        "tooltip": "Project priority level",
        "detail": "High = pursue immediately | Medium = good opportunity, plan carefully | Low = reconsider or defer"
    },
    
    # Capital Stack
    "capital_stack": {
        "tooltip": "Your business funding structure",
        "detail": "Shows how your business is financed: equity (ownership), debt (loans), and other capital sources. Balanced stacks reduce risk."
    },
    "debt_equity_ratio": {
        "tooltip": "Ratio of debt to equity financing",
        "detail": "Lower ratio = less risky, more equity | Higher ratio = more leveraged, more debt. Typical healthy range: 0.5 - 2.0"
    },
    
    # General
    "sync_status": {
        "tooltip": "Data synchronization status",
        "detail": "Shows which module last updated the shared financial data. All modules read from the same source to ensure consistency."
    },
    "data_integrity": {
        "tooltip": "System data integrity score",
        "detail": "Measures how complete and valid your data is across all modules. 100% = all data validated and consistent."
    },
}


def get_help_content(help_key, content_type="tooltip"):
    """
    Retrieve help content from registry
    
    Args:
        help_key: Key to look up
        content_type: Type of content ("tooltip" or "detail")
    
    Returns:
        str: Help content or None
    """
    if help_key not in HELP_CONTENT:
        return None
    
    return HELP_CONTENT[help_key].get(content_type)


def get_contextual_help(context_type, **kwargs):
    """
    Get contextual help based on current state
    
    Args:
        context_type: Type of context
        **kwargs: Additional context data
    
    Returns:
        dict: Help data with message and type
    """
    contextual_help = {
        "empty_revenue": {
            "message": "💡 **Get Started:** Enter your monthly revenue to unlock financial projections, valuation analysis, and working capital recommendations",
            "type": "info"
        },
        "incomplete_data": {
            "message": "📊 **Improve Accuracy:** Complete additional financial fields to increase valuation precision and unlock advanced analysis methods",
            "type": "info"
        },
        "no_profit": {
            "message": "⚠️ **Note:** Current losses limit earnings-based valuation methods. Focus on path to profitability to unlock additional valuation approaches.",
            "type": "warning"
        },
        "high_variability": {
            "message": "⚠️ **High Uncertainty:** Valuation methods show significant disagreement. Consider refining financial inputs or gathering additional market data.",
            "type": "warning"
        },
        "low_revenue": {
            "message": "📊 **Limited Scale:** Revenue under $100K/month may constrain valuation and funding options. Focus on growth strategies.",
            "type": "info"
        },
        "negative_growth": {
            "message": "📉 **Declining Revenue:** Negative growth requires immediate attention. Review market position, pricing, and customer retention.",
            "type": "warning"
        },
        "high_expenses": {
            "message": "💸 **Cost Optimization:** Expenses exceed 90% of revenue. Review cost structure for optimization opportunities.",
            "type": "warning"
        },
        "strong_performance": {
            "message": "✅ **Strong Performance:** Healthy margins and positive growth create strong foundation for valuation and funding.",
            "type": "success"
        },
        "valuation_ready": {
            "message": "✅ **Valuation Ready:** All core financial data complete. Run valuation analysis to see your business value distribution.",
            "type": "success"
        },
        "loc_recommended": {
            "message": "💳 **Working Capital:** Based on your cash flow, a line of credit is recommended to cover operational gaps.",
            "type": "info"
        },
    }
    
    return contextual_help.get(context_type)


def add_help_to_registry(help_key, tooltip, detail):
    """
    Add new help content to registry (for dynamic additions)
    
    Args:
        help_key: Unique key for help content
        tooltip: Short tooltip text
        detail: Detailed explanation
    """
    HELP_CONTENT[help_key] = {
        "tooltip": tooltip,
        "detail": detail,
    }


def get_all_help_keys():
    """
    Get all available help keys
    
    Returns:
        list: All help keys in registry
    """
    return list(HELP_CONTENT.keys())


def search_help_content(query):
    """
    Search help content by query
    
    Args:
        query: Search query
    
    Returns:
        list: Matching help keys
    """
    query_lower = query.lower()
    matches = []
    
    for key, content in HELP_CONTENT.items():
        tooltip = content.get("tooltip", "").lower()
        detail = content.get("detail", "").lower()
        
        if query_lower in tooltip or query_lower in detail or query_lower in key:
            matches.append(key)
    
    return matches
