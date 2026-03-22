"""
LOC Analyzer - Cash Flow Logic Module
Cash trough detection and line of credit calculation
"""


def project_cash_flow(starting_cash, monthly_revenue, monthly_expenses, months=12, revenue_growth=0, expense_growth=0):
    """
    Project monthly cash balance over time
    
    Args:
        starting_cash: Initial cash balance
        monthly_revenue: Starting monthly revenue
        monthly_expenses: Starting monthly expenses
        months: Number of months to project (default 12)
        revenue_growth: Monthly revenue growth rate (default 0)
        expense_growth: Monthly expense growth rate (default 0)
    
    Returns:
        dict with cash_balance, inflows, outflows lists
    """
    
    cash_balance = [starting_cash]
    inflows = []
    outflows = []
    
    for month in range(1, months + 1):
        month_revenue = monthly_revenue * ((1 + revenue_growth) ** (month - 1))
        month_expenses = monthly_expenses * ((1 + expense_growth) ** (month - 1))
        
        inflows.append(month_revenue)
        outflows.append(month_expenses)
        
        new_balance = cash_balance[-1] + month_revenue - month_expenses
        cash_balance.append(new_balance)
    
    return {
        "cash_balance": cash_balance,
        "inflows": inflows,
        "outflows": outflows,
        "months": list(range(0, months + 1))
    }


def identify_cash_trough(cash_balance):
    """
    Identify the lowest cash point (trough)
    
    Args:
        cash_balance: List of cash balances over time
    
    Returns:
        dict with lowest_cash, trough_month, trough_index
    """
    
    lowest_cash = min(cash_balance)
    trough_index = cash_balance.index(lowest_cash)
    
    return {
        "lowest_cash": lowest_cash,
        "trough_month": trough_index,
        "trough_index": trough_index
    }


def calculate_loc_recommendation(lowest_cash, safety_buffer=1.25, stress_buffer=1.5):
    """
    Calculate recommended line of credit amounts
    
    Args:
        lowest_cash: The lowest cash balance in projection
        safety_buffer: Multiplier for recommended LOC (default 1.25 = 25% buffer)
        stress_buffer: Multiplier for stress scenario LOC (default 1.5 = 50% buffer)
    
    Returns:
        dict with base_loc, recommended_loc, stress_loc
    """
    
    base_loc = abs(lowest_cash) if lowest_cash < 0 else 0
    
    recommended_loc = base_loc * safety_buffer if base_loc > 0 else 0
    
    stress_loc = base_loc * stress_buffer if base_loc > 0 else 0
    
    return {
        "base_loc": base_loc,
        "recommended_loc": recommended_loc,
        "stress_loc": stress_loc,
        "needs_loc": lowest_cash < 0
    }


def generate_loc_insights(cash_flow_data, trough_data, loc_data, monthly_revenue):
    """
    Generate insights based on cash flow analysis
    
    Args:
        cash_flow_data: Cash flow projection data
        trough_data: Trough identification data
        loc_data: LOC recommendation data
        monthly_revenue: Starting monthly revenue
    
    Returns:
        list of insight strings
    """
    
    insights = []
    
    lowest_cash = trough_data["lowest_cash"]
    trough_month = trough_data["trough_month"]
    base_loc = loc_data["base_loc"]
    
    if lowest_cash < 0:
        insights.append(f"💰 **Cash Shortfall Detected**: Business experiences a cash deficit of ${abs(lowest_cash):,.0f} requiring external funding or line of credit.")
    else:
        insights.append(f"✅ **Positive Cash Flow**: Business maintains positive cash balance throughout the projection period. No LOC required.")
    
    if trough_month <= 3 and lowest_cash < 0:
        insights.append(f"⚠️ **Early Cash Pressure**: Cash trough occurs in Month {trough_month}, indicating insufficient starting capital or early-stage cash flow challenges.")
    elif trough_month > 9 and lowest_cash < 0:
        insights.append(f"📊 **Late-Stage Pressure**: Cash trough occurs in Month {trough_month}, suggesting seasonal patterns or delayed cash flow issues.")
    
    if abs(lowest_cash) > (monthly_revenue * 2):
        insights.append(f"🔴 **Structural Cash Gap**: Cash deficit exceeds 2x monthly revenue, suggesting fundamental cash flow issues beyond normal timing gaps.")
    
    if base_loc > 0:
        if base_loc < monthly_revenue:
            insights.append(f"💡 **Manageable Gap**: Required LOC (${base_loc:,.0f}) is less than one month's revenue, indicating a timing issue rather than structural problem.")
        elif base_loc > monthly_revenue * 3:
            insights.append(f"⚠️ **Significant Capital Need**: Required LOC exceeds 3x monthly revenue. Consider equity financing or business model adjustments.")
    
    cash_volatility = max(cash_flow_data["cash_balance"]) - min(cash_flow_data["cash_balance"])
    if cash_volatility > monthly_revenue * 2:
        insights.append(f"📈 **High Cash Volatility**: Cash balance swings by ${cash_volatility:,.0f}. Consider strategies to smooth cash flow timing.")
    
    if len(insights) < 2:
        insights.append("💡 **Healthy Cash Position**: Current projections show stable cash management with minimal external funding needs.")
    
    return insights


def calculate_working_capital_metrics(cash_flow_data, monthly_revenue, monthly_expenses):
    """
    Calculate working capital metrics
    
    Args:
        cash_flow_data: Cash flow projection data
        monthly_revenue: Starting monthly revenue
        monthly_expenses: Starting monthly expenses
    
    Returns:
        dict with various working capital metrics
    """
    
    cash_balances = cash_flow_data["cash_balance"]
    
    avg_cash = sum(cash_balances) / len(cash_balances)
    
    max_cash = max(cash_balances)
    min_cash = min(cash_balances)
    
    cash_volatility = max_cash - min_cash
    
    months_of_runway = (avg_cash / monthly_expenses) if monthly_expenses > 0 else 0
    
    return {
        "avg_cash": avg_cash,
        "max_cash": max_cash,
        "min_cash": min_cash,
        "cash_volatility": cash_volatility,
        "months_of_runway": months_of_runway
    }


def calculate_cash_conversion_cycle(revenue_delay_days=30, expense_delay_days=0):
    """
    Calculate cash conversion cycle impact
    
    Args:
        revenue_delay_days: Days between sale and cash receipt
        expense_delay_days: Days between expense and cash payment
    
    Returns:
        dict with cash conversion metrics
    """
    
    cash_conversion_days = revenue_delay_days - expense_delay_days
    
    return {
        "revenue_delay_days": revenue_delay_days,
        "expense_delay_days": expense_delay_days,
        "cash_conversion_days": cash_conversion_days,
        "cash_timing_impact": "Negative" if cash_conversion_days > 0 else "Positive"
    }


def simulate_loc_usage(cash_balance, loc_amount):
    """
    Simulate how LOC would be used over time
    
    Args:
        cash_balance: List of cash balances
        loc_amount: Available LOC amount
    
    Returns:
        dict with loc_usage, remaining_cash, max_loc_used
    """
    
    loc_usage = []
    remaining_cash = []
    
    for balance in cash_balance:
        if balance < 0:
            loc_used = min(abs(balance), loc_amount)
            loc_usage.append(loc_used)
            remaining_cash.append(balance + loc_used)
        else:
            loc_usage.append(0)
            remaining_cash.append(balance)
    
    max_loc_used = max(loc_usage) if loc_usage else 0
    
    return {
        "loc_usage": loc_usage,
        "remaining_cash": remaining_cash,
        "max_loc_used": max_loc_used,
        "loc_utilization": (max_loc_used / loc_amount * 100) if loc_amount > 0 else 0
    }
