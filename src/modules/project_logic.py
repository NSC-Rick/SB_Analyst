"""
North Star Unified Shell - Project Evaluator Logic
Project scoring and decision engine
"""


def calculate_project_score(inputs):
    """
    Calculate weighted project score from evaluation dimensions
    
    Args:
        inputs: Dict with dimension ratings (1-5 scale)
    
    Returns:
        float: Project score (0-100)
    """
    financial = inputs.get("financial_rating", 3)
    alignment = inputs.get("alignment_rating", 3)
    capacity = inputs.get("capacity_rating", 3)
    effort = inputs.get("effort_rating", 3)
    risk = inputs.get("risk_rating", 3)
    
    # Weighted calculation
    # Effort and risk are inverted (lower is better)
    score = (
        financial * 0.30 +
        alignment * 0.25 +
        capacity * 0.20 +
        (6 - effort) * 0.15 +
        (6 - risk) * 0.10
    )
    
    # Convert to 0-100 scale
    final_score = score * 20
    
    return round(final_score, 1)


def classify_priority(score):
    """
    Classify project priority based on score
    
    Args:
        score: Project score (0-100)
    
    Returns:
        str: Priority classification
    """
    if score >= 75:
        return "High Priority"
    elif score >= 50:
        return "Medium Priority"
    else:
        return "Low Priority"


def generate_recommendation(score, priority, inputs):
    """
    Generate recommendation based on score and inputs
    
    Args:
        score: Project score
        priority: Priority classification
        inputs: Input ratings
    
    Returns:
        str: Recommendation text
    """
    financial = inputs.get("financial_rating", 3)
    effort = inputs.get("effort_rating", 3)
    risk = inputs.get("risk_rating", 3)
    capacity = inputs.get("capacity_rating", 3)
    
    if priority == "High Priority":
        if effort <= 2 and financial >= 4:
            return "🚀 **Strong project — pursue now.** High impact with manageable effort makes this an excellent opportunity."
        else:
            return "🚀 **Strong project — pursue now.** This initiative shows solid fundamentals across key dimensions."
    
    elif priority == "Medium Priority":
        if effort >= 4:
            return "⚠️ **Good opportunity — plan carefully.** High effort level requires thorough planning and resource allocation."
        elif risk >= 4:
            return "⚠️ **Good opportunity — plan carefully.** Risk level suggests careful mitigation strategies before proceeding."
        elif capacity <= 2:
            return "⚠️ **Good opportunity — plan carefully.** Current capacity constraints may require timing adjustments."
        else:
            return "⚠️ **Good opportunity — plan carefully.** Solid potential with some areas requiring attention."
    
    else:  # Low Priority
        if effort >= 4 and financial <= 2:
            return "⏸️ **High effort or risk — consider delaying.** Low financial impact doesn't justify the effort required."
        elif risk >= 4:
            return "⏸️ **High effort or risk — consider delaying.** Risk level is significant relative to potential benefits."
        else:
            return "⏸️ **Consider delaying or refining.** Current assessment suggests other priorities may be more valuable."


def generate_insights(inputs):
    """
    Generate rule-based insights from evaluation
    
    Args:
        inputs: Input ratings
    
    Returns:
        list: Insight strings
    """
    insights = []
    
    financial = inputs.get("financial_rating", 3)
    alignment = inputs.get("alignment_rating", 3)
    capacity = inputs.get("capacity_rating", 3)
    effort = inputs.get("effort_rating", 3)
    risk = inputs.get("risk_rating", 3)
    
    # High impact, low effort (sweet spot)
    if financial >= 4 and effort <= 2:
        insights.append("💎 **High impact with low effort** — strong opportunity for quick wins.")
    
    # Strong alignment
    if alignment >= 4:
        insights.append("🎯 **Strong strategic alignment** — supports core business direction.")
    
    # High risk
    if risk >= 4:
        insights.append("⚠️ **High risk level** — consider mitigation strategies before proceeding.")
    
    # Limited capacity
    if capacity <= 2:
        insights.append("⏰ **Limited capacity** may delay execution or require resource reallocation.")
    
    # High effort
    if effort >= 4:
        insights.append("🏋️ **High effort required** — ensure adequate time and resources are available.")
    
    # Good financial + good capacity
    if financial >= 4 and capacity >= 4:
        insights.append("✅ **Strong financial potential with available capacity** — well-positioned for execution.")
    
    # Low financial + high effort
    if financial <= 2 and effort >= 4:
        insights.append("📉 **Low financial return for high effort** — ROI may not justify investment.")
    
    # Balanced project
    if all(3 <= rating <= 4 for rating in [financial, alignment, capacity]) and effort <= 3 and risk <= 3:
        insights.append("⚖️ **Well-balanced project** — solid fundamentals across all dimensions.")
    
    return insights[:4]  # Return top 4


def get_matrix_quadrant(financial, effort):
    """
    Determine which quadrant a project falls into
    
    Args:
        financial: Financial impact rating (1-5)
        effort: Effort rating (1-5)
    
    Returns:
        str: Quadrant name
    """
    high_impact = financial >= 3.5
    low_effort = effort <= 2.5
    
    if high_impact and low_effort:
        return "Do Now"
    elif high_impact and not low_effort:
        return "Plan"
    elif not high_impact and low_effort:
        return "Optional"
    else:
        return "Avoid"


def get_dimension_label(dimension_key):
    """
    Get display label for dimension
    
    Args:
        dimension_key: Dimension identifier
    
    Returns:
        str: Display label
    """
    labels = {
        "financial_impact": "Financial Impact",
        "strategic_alignment": "Strategic Alignment",
        "effort_complexity": "Effort / Complexity",
        "risk_level": "Risk Level",
        "capacity_readiness": "Capacity / Readiness"
    }
    return labels.get(dimension_key, dimension_key)


def get_dimension_description(dimension_key):
    """
    Get description for dimension
    
    Args:
        dimension_key: Dimension identifier
    
    Returns:
        str: Dimension description
    """
    descriptions = {
        "financial_impact": "Expected revenue increase, cost savings, or ROI potential",
        "strategic_alignment": "Alignment with business goals and core direction",
        "effort_complexity": "Time required and operational complexity",
        "risk_level": "Uncertainty, dependencies, and potential obstacles",
        "capacity_readiness": "Team capacity and capital availability"
    }
    return descriptions.get(dimension_key, "")


def get_rating_guidance(dimension_key):
    """
    Get guidance for rating a dimension
    
    Args:
        dimension_key: Dimension identifier
    
    Returns:
        dict: Rating guidance
    """
    guidance = {
        "financial_impact": {
            1: "Minimal financial impact or unclear ROI",
            3: "Moderate financial benefit expected",
            5: "Significant revenue increase or cost savings"
        },
        "strategic_alignment": {
            1: "Misaligned with business goals",
            3: "Somewhat aligned with strategy",
            5: "Perfectly aligned with core direction"
        },
        "effort_complexity": {
            1: "Minimal time and low complexity",
            3: "Moderate effort and complexity",
            5: "Extensive time and high complexity"
        },
        "risk_level": {
            1: "Low uncertainty and few dependencies",
            3: "Moderate risk and manageable dependencies",
            5: "High uncertainty and significant obstacles"
        },
        "capacity_readiness": {
            1: "Insufficient capacity or capital",
            3: "Adequate capacity with some constraints",
            5: "Full capacity and resources available"
        }
    }
    return guidance.get(dimension_key, {})


def create_project_evaluation(inputs, score, priority, recommendation, insights):
    """
    Create project evaluation object for session state
    
    Args:
        inputs: User input data
        score: Project score
        priority: Priority classification
        recommendation: Recommendation text
        insights: List of insights
    
    Returns:
        dict: Project evaluation for session state
    """
    return {
        "project_name": inputs.get("project_name", "Untitled Project"),
        "project_description": inputs.get("project_description", ""),
        "score": score,
        "priority": priority,
        "recommendation": recommendation,
        "insights": insights,
        "financial": inputs.get("financial_rating", 3),
        "alignment": inputs.get("alignment_rating", 3),
        "capacity": inputs.get("capacity_rating", 3),
        "effort": inputs.get("effort_rating", 3),
        "risk": inputs.get("risk_rating", 3),
        "quadrant": get_matrix_quadrant(
            inputs.get("financial_rating", 3),
            inputs.get("effort_rating", 3)
        ),
        "source_module": "project_evaluator"
    }
