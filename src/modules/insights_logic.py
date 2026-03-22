"""
North Star Unified Shell - Insights Engine Logic
Cross-module insight generation and analysis
"""


def generate_financial_insights(core_financials):
    """
    Generate insights from financial data
    
    Args:
        core_financials: Dict with financial data
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    revenue = core_financials.get("revenue", 0)
    expenses = core_financials.get("expenses", 0)
    profit = core_financials.get("profit", 0)
    growth_rate = core_financials.get("growth_rate", 0)
    
    if revenue == 0:
        return insights
    
    # Margin analysis
    margin = (profit / revenue) * 100 if revenue > 0 else 0
    
    if margin < 10:
        insights.append(("📉 **Low profit margins (<10%)** are limiting overall financial performance and valuation potential.", "high"))
    elif margin < 20:
        insights.append(("📊 **Moderate margins (10-20%)** provide room for improvement through cost optimization or pricing adjustments.", "medium"))
    elif margin >= 30:
        insights.append(("💎 **Strong profit margins (≥30%)** indicate healthy unit economics and pricing power.", "positive"))
    
    # Profitability
    if profit > 0:
        insights.append(("✅ **Positive profitability** unlocks earnings-based valuation methods and improves funding eligibility.", "positive"))
    elif profit < 0:
        insights.append(("⚠️ **Current losses** limit valuation options and may require path-to-profitability clarity for funding.", "high"))
    
    # Growth trajectory
    if growth_rate > 0.15:
        insights.append(("🚀 **Strong growth trajectory (>15%/month)** supports expansion plans and increases investor appeal.", "positive"))
    elif growth_rate > 0.05:
        insights.append(("📈 **Moderate growth (5-15%/month)** indicates healthy momentum with room for acceleration.", "medium"))
    elif growth_rate < 0:
        insights.append(("📉 **Negative growth** requires immediate attention to reverse declining revenue trends.", "high"))
    
    # Cost structure
    if expenses > 0:
        expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
        
        if expense_ratio > 90:
            insights.append(("⚠️ **High expense ratio (>90%)** leaves minimal room for profit and limits financial flexibility.", "high"))
        elif expense_ratio < 70:
            insights.append(("✅ **Efficient cost structure (<70% of revenue)** provides strong operational leverage.", "positive"))
    
    # Revenue scale
    if revenue < 100000:
        insights.append(("📊 **Limited revenue scale** may constrain current valuation and funding options.", "medium"))
    elif revenue > 1000000:
        insights.append(("💰 **Strong revenue base (>$1M/month)** provides solid foundation for growth and valuation.", "positive"))
    
    return insights


def generate_valuation_insights(valuation_range, core_financials):
    """
    Generate insights from valuation data
    
    Args:
        valuation_range: Tuple of (low, high) or None
        core_financials: Dict with financial data
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    if not valuation_range:
        return insights
    
    low, high = valuation_range
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    
    # Valuation exists
    midpoint = (low + high) / 2
    insights.append((f"💎 **Estimated business value: ${low:,.0f} - ${high:,.0f}** (midpoint: ${midpoint:,.0f})", "positive"))
    
    # Valuation driver analysis
    if profit <= 0 and revenue > 0:
        insights.append(("📊 **Valuation currently driven by revenue multiples** rather than profitability. Path to profit will increase value.", "medium"))
    elif profit > 0 and revenue > 0:
        insights.append(("✅ **Valuation benefits from both revenue and profitability**, providing stronger investor confidence.", "positive"))
    
    # Value improvement potential
    margin = (profit / revenue) * 100 if revenue > 0 else 0
    if margin > 0 and margin < 20:
        potential_increase = (high * 0.20)  # 20% margin improvement scenario
        insights.append((f"📈 **Margin improvement opportunity**: Increasing profit margin by 20% could add ~${potential_increase:,.0f} to valuation.", "medium"))
    
    return insights


def generate_loc_insights(loc_data, core_financials):
    """
    Generate insights from LOC analyzer data
    
    Args:
        loc_data: Dict with LOC recommendation or None
        core_financials: Dict with financial data
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    if not loc_data:
        return insights
    
    revenue = core_financials.get("revenue", 0)
    
    recommended_loc = loc_data.get("recommended_loc", 0)
    eligibility = loc_data.get("eligibility", "Unknown")
    
    if recommended_loc > 0:
        # LOC relative to revenue
        if revenue > 0:
            loc_ratio = (recommended_loc / revenue)
            
            if loc_ratio > 1.5:
                insights.append(("⚠️ **High working capital need** (>1.5x monthly revenue) suggests cash flow strain or inventory intensity.", "high"))
            elif loc_ratio > 0.75:
                insights.append(("💳 **Moderate working capital need** (0.75-1.5x revenue) is typical for growing businesses.", "medium"))
            else:
                insights.append(("✅ **Manageable working capital need** (<0.75x revenue) indicates efficient cash conversion.", "positive"))
        
        # Eligibility
        if eligibility == "Strong":
            insights.append((f"🏦 **Strong LOC eligibility** with recommended line of ${recommended_loc:,.0f} provides growth flexibility.", "positive"))
        elif eligibility == "Moderate":
            insights.append((f"💳 **Moderate LOC eligibility** suggests ${recommended_loc:,.0f} line is accessible with standard terms.", "medium"))
        elif eligibility == "Limited":
            insights.append(("⚠️ **Limited LOC eligibility** may require alternative financing or improved financial metrics.", "high"))
    
    return insights


def generate_project_insights(project_eval):
    """
    Generate insights from project evaluation
    
    Args:
        project_eval: Dict with project evaluation or None
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    if not project_eval:
        return insights
    
    priority = project_eval.get("priority", "")
    score = project_eval.get("score", 0)
    quadrant = project_eval.get("quadrant", "")
    project_name = project_eval.get("project_name", "Current project")
    
    # Priority-based insights
    if priority == "High Priority":
        insights.append((f"🎯 **{project_name} is high priority** (score: {score:.0f}/100) and should be pursued now.", "high"))
    elif priority == "Medium Priority":
        insights.append((f"⚖️ **{project_name} shows promise** (score: {score:.0f}/100) but requires careful planning.", "medium"))
    elif priority == "Low Priority":
        insights.append((f"⏸️ **{project_name} is low priority** (score: {score:.0f}/100) - consider deferring or refining.", "medium"))
    
    # Quadrant insights
    if quadrant == "Do Now":
        insights.append(("💎 **Project positioned in 'Do Now' quadrant** - high impact with low effort makes this an excellent opportunity.", "positive"))
    elif quadrant == "Avoid":
        insights.append(("⚠️ **Project in 'Avoid' quadrant** - high effort with low impact suggests ROI concerns.", "high"))
    
    return insights


def generate_idea_insights(idea_context):
    """
    Generate insights from idea screener
    
    Args:
        idea_context: Dict with idea evaluation or None
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    if not idea_context:
        return insights
    
    viability_score = idea_context.get("viability_score", 0)
    classification = idea_context.get("classification", "")
    idea_title = idea_context.get("idea_title", "Business concept")
    
    if classification == "Strong Opportunity":
        insights.append((f"💡 **{idea_title} shows strong viability** ({viability_score:.0f}/100) and is ready for detailed modeling.", "positive"))
    elif classification == "Promising but Needs Clarification":
        insights.append((f"💡 **{idea_title} is promising** ({viability_score:.0f}/100) but needs refinement before scaling.", "medium"))
    elif viability_score < 50:
        insights.append((f"⚠️ **{idea_title} needs strengthening** ({viability_score:.0f}/100) before significant investment.", "high"))
    
    return insights


def generate_cross_module_insights(core_financials, valuation_range, loc_data, project_eval, idea_context):
    """
    Generate insights that span multiple modules
    
    Args:
        core_financials: Financial data
        valuation_range: Valuation data
        loc_data: LOC data
        project_eval: Project evaluation
        idea_context: Idea context
    
    Returns:
        list: Tuples of (insight_text, priority)
    """
    insights = []
    
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    growth_rate = core_financials.get("growth_rate", 0)
    
    # Growth + Funding readiness
    if growth_rate > 0.10 and profit > 0:
        insights.append(("🚀 **Growth + profitability combination** positions business well for funding or acquisition conversations.", "positive"))
    
    # Valuation + Project alignment
    if valuation_range and project_eval:
        if project_eval.get("priority") == "High Priority":
            insights.append(("🎯 **High-priority project with established valuation** enables clear ROI analysis for initiative.", "positive"))
    
    # Idea + Financial readiness
    if idea_context and revenue > 0:
        if idea_context.get("viability_score", 0) >= 70:
            insights.append(("💡 **Strong idea viability with existing revenue base** suggests expansion opportunity.", "positive"))
    
    # Cash flow + Growth tension
    if loc_data and growth_rate > 0.15:
        if loc_data.get("recommended_loc", 0) > revenue * 1.2:
            insights.append(("⚠️ **High growth with significant working capital needs** - ensure adequate financing to support expansion.", "high"))
    
    # Profitability + Valuation gap
    if profit <= 0 and valuation_range:
        insights.append(("📊 **Path to profitability is critical** - current valuation is revenue-based and will strengthen with positive earnings.", "high"))
    
    return insights


def categorize_insights(all_insights):
    """
    Categorize insights into groups
    
    Args:
        all_insights: List of (insight_text, priority) tuples
    
    Returns:
        dict: Categorized insights
    """
    categories = {
        "financial": [],
        "valuation": [],
        "cash_flow": [],
        "funding": [],
        "strategy": []
    }
    
    for insight, priority in all_insights:
        insight_lower = insight.lower()
        
        # Categorization logic
        if any(word in insight_lower for word in ["margin", "profit", "revenue", "cost", "expense", "growth"]):
            categories["financial"].append((insight, priority))
        elif any(word in insight_lower for word in ["valuation", "value", "worth"]):
            categories["valuation"].append((insight, priority))
        elif any(word in insight_lower for word in ["loc", "working capital", "cash flow", "liquidity"]):
            categories["cash_flow"].append((insight, priority))
        elif any(word in insight_lower for word in ["funding", "financing", "eligibility", "investor"]):
            categories["funding"].append((insight, priority))
        elif any(word in insight_lower for word in ["project", "idea", "priority", "opportunity"]):
            categories["strategy"].append((insight, priority))
        else:
            # Default to financial
            categories["financial"].append((insight, priority))
    
    return categories


def generate_summary_takeaways(categorized_insights, core_financials):
    """
    Generate 3-5 key takeaways
    
    Args:
        categorized_insights: Dict of categorized insights
        core_financials: Financial data
    
    Returns:
        list: Summary takeaway strings
    """
    takeaways = []
    
    # Find highest priority insights across categories
    high_priority_insights = []
    for category, insights in categorized_insights.items():
        for insight, priority in insights:
            if priority == "high":
                high_priority_insights.append(insight)
    
    # Add top high-priority insights
    if high_priority_insights:
        takeaways.append(f"**Biggest Risk:** {high_priority_insights[0].replace('⚠️', '').replace('📉', '').strip()}")
    
    # Find positive insights (opportunities)
    positive_insights = []
    for category, insights in categorized_insights.items():
        for insight, priority in insights:
            if priority == "positive":
                positive_insights.append(insight)
    
    if positive_insights:
        takeaways.append(f"**Biggest Opportunity:** {positive_insights[0].replace('💎', '').replace('🚀', '').replace('✅', '').strip()}")
    
    # Financial focus
    profit = core_financials.get("profit", 0)
    revenue = core_financials.get("revenue", 0)
    margin = (profit / revenue) * 100 if revenue > 0 else 0
    
    if margin < 15:
        takeaways.append("**Recommended Focus:** Improve profit margins through cost optimization or pricing adjustments")
    elif profit > 0 and revenue > 0:
        takeaways.append("**Recommended Focus:** Leverage profitability to pursue growth initiatives and funding opportunities")
    
    # Ensure 3-5 takeaways
    if len(takeaways) < 3:
        takeaways.append("**Platform Status:** Continue building financial data to unlock deeper insights")
    
    return takeaways[:5]


def generate_recommended_actions(categorized_insights, core_financials, valuation_range, loc_data, project_eval):
    """
    Generate recommended next steps
    
    Args:
        categorized_insights: Dict of categorized insights
        core_financials: Financial data
        valuation_range: Valuation data
        loc_data: LOC data
        project_eval: Project evaluation
    
    Returns:
        list: Action recommendation strings
    """
    actions = []
    
    revenue = core_financials.get("revenue", 0)
    profit = core_financials.get("profit", 0)
    margin = (profit / revenue) * 100 if revenue > 0 else 0
    
    # Margin improvement
    if margin < 15 and margin > 0:
        actions.append("📊 **Improve profit margins** - Analyze cost structure and pricing to increase profitability")
    
    # Profitability path
    if profit <= 0:
        actions.append("💰 **Establish path to profitability** - Critical for valuation strength and funding eligibility")
    
    # LOC action
    if loc_data and loc_data.get("eligibility") in ["Strong", "Moderate"]:
        actions.append("💳 **Secure line of credit** - Strong eligibility suggests now is good time to establish LOC")
    
    # Project action
    if project_eval and project_eval.get("priority") == "High Priority":
        actions.append(f"🎯 **Prioritize {project_eval.get('project_name', 'current project')}** - High score indicates strong opportunity")
    
    # Valuation action
    if not valuation_range and revenue > 0:
        actions.append("💎 **Calculate business valuation** - Financial data is ready for valuation analysis")
    
    # Growth action
    growth_rate = core_financials.get("growth_rate", 0)
    if growth_rate > 0.10 and profit > 0:
        actions.append("🚀 **Explore funding options** - Growth + profitability combination supports expansion capital")
    
    # Ensure at least 3 actions
    if len(actions) < 3:
        actions.append("📈 **Continue financial modeling** - Build more detailed projections to unlock additional insights")
    
    return actions[:6]


def check_data_availability(core_financials, valuation_range, loc_data, project_eval, idea_context):
    """
    Check which data sources are available
    
    Returns:
        dict: Availability status
    """
    return {
        "financial": core_financials.get("revenue", 0) > 0,
        "valuation": valuation_range is not None,
        "loc": loc_data is not None,
        "project": project_eval is not None,
        "idea": idea_context is not None,
        "any_data": any([
            core_financials.get("revenue", 0) > 0,
            valuation_range is not None,
            loc_data is not None,
            project_eval is not None,
            idea_context is not None
        ])
    }
