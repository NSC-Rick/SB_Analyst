"""
North Star Unified Shell - Idea Screener Logic
Business concept evaluation and scoring engine
"""


def calculate_category_scores(inputs):
    """
    Calculate scores for each evaluation category
    
    Args:
        inputs: Dict with category ratings (1-5 scale)
    
    Returns:
        dict: Category scores (0-100 scale)
    """
    # Convert 1-5 scale to 0-100 scale
    def scale_to_100(rating):
        return ((rating - 1) / 4) * 100
    
    return {
        "market_opportunity": scale_to_100(inputs.get("market_rating", 3)),
        "revenue_potential": scale_to_100(inputs.get("revenue_rating", 3)),
        "cost_feasibility": scale_to_100(inputs.get("cost_rating", 3)),
        "execution_readiness": scale_to_100(inputs.get("execution_rating", 3)),
        "risk_level": scale_to_100(inputs.get("risk_rating", 3))
    }


def calculate_overall_viability(category_scores):
    """
    Calculate overall viability score from category scores
    
    Args:
        category_scores: Dict with category scores (0-100)
    
    Returns:
        float: Overall viability score (0-100)
    """
    # Weighted average - risk is inverse (lower risk = better)
    weights = {
        "market_opportunity": 0.25,
        "revenue_potential": 0.25,
        "cost_feasibility": 0.20,
        "execution_readiness": 0.20,
        "risk_level": 0.10  # Lower weight, and will be inverted
    }
    
    # Invert risk score (high risk rating = low viability contribution)
    adjusted_scores = category_scores.copy()
    adjusted_scores["risk_level"] = 100 - adjusted_scores["risk_level"]
    
    weighted_sum = sum(adjusted_scores[cat] * weights[cat] for cat in weights)
    
    return round(weighted_sum, 1)


def classify_viability(overall_score):
    """
    Classify viability into bands
    
    Args:
        overall_score: Overall viability score (0-100)
    
    Returns:
        str: Classification band
    """
    if overall_score >= 70:
        return "Strong Opportunity"
    elif overall_score >= 50:
        return "Promising but Needs Clarification"
    else:
        return "Early Stage / High Uncertainty"


def generate_recommendation(overall_score, category_scores, classification):
    """
    Generate practical recommendation based on scores
    
    Args:
        overall_score: Overall viability score
        category_scores: Dict with category scores
        classification: Viability classification
    
    Returns:
        str: Recommendation text
    """
    if classification == "Strong Opportunity":
        return "This idea appears strong enough to move into financial modeling. The concept shows solid fundamentals across key dimensions."
    
    elif classification == "Promising but Needs Clarification":
        # Identify weakest areas
        weak_areas = []
        if category_scores["revenue_potential"] < 50:
            weak_areas.append("revenue model")
        if category_scores["cost_feasibility"] < 50:
            weak_areas.append("cost assumptions")
        if category_scores["execution_readiness"] < 50:
            weak_areas.append("execution capacity")
        
        if weak_areas:
            areas_text = " and ".join(weak_areas)
            return f"This concept shows promise, but {areas_text} clarity should be improved before detailed modeling."
        else:
            return "This concept shows promise. Consider refining key assumptions before moving into detailed financial modeling."
    
    else:
        return "This idea currently carries high uncertainty and may need refinement before detailed modeling. Focus on strengthening core assumptions and reducing key risks."


def identify_strengths(category_scores):
    """
    Identify strengths based on high-scoring categories
    
    Args:
        category_scores: Dict with category scores
    
    Returns:
        list: Strength observations
    """
    strengths = []
    
    if category_scores["market_opportunity"] >= 70:
        strengths.append("💎 Strong market opportunity with clear target customer and differentiation")
    
    if category_scores["revenue_potential"] >= 70:
        strengths.append("💰 Solid revenue model with realistic pricing and earning potential")
    
    if category_scores["cost_feasibility"] >= 70:
        strengths.append("✅ Well-understood cost structure and operational feasibility")
    
    if category_scores["execution_readiness"] >= 70:
        strengths.append("🚀 Strong execution readiness with relevant capability and commitment")
    
    # Combined strengths
    if (category_scores["market_opportunity"] >= 70 and 
        category_scores["execution_readiness"] >= 70):
        strengths.append("🎯 Strong alignment between market opportunity and execution readiness")
    
    if (category_scores["revenue_potential"] >= 70 and 
        category_scores["cost_feasibility"] >= 70):
        strengths.append("📊 Balanced financial model with strong revenue and cost clarity")
    
    return strengths[:3]  # Return top 3


def identify_watchouts(category_scores):
    """
    Identify watchouts based on low-scoring categories
    
    Args:
        category_scores: Dict with category scores
    
    Returns:
        list: Watchout observations
    """
    watchouts = []
    
    if category_scores["market_opportunity"] < 50:
        watchouts.append("⚠️ Market opportunity needs clearer definition - target customer and differentiation should be strengthened")
    
    if category_scores["revenue_potential"] < 50:
        watchouts.append("⚠️ Revenue model may need more clarity before detailed forecasting")
    
    if category_scores["cost_feasibility"] < 50:
        watchouts.append("⚠️ Startup or operating cost assumptions may need refinement")
    
    if category_scores["execution_readiness"] < 50:
        watchouts.append("⚠️ Execution capacity or capability may need to be strengthened")
    
    if category_scores["risk_level"] > 70:  # High risk rating
        watchouts.append("⚠️ Key dependencies or uncertainties may need to be reduced before launch")
    
    # Combined watchouts
    if (category_scores["revenue_potential"] < 50 and 
        category_scores["cost_feasibility"] < 50):
        watchouts.append("⚠️ Financial assumptions need significant clarification across revenue and costs")
    
    return watchouts[:3]  # Return top 3


def create_idea_context(inputs, category_scores, overall_score, classification, recommendation, strengths, watchouts):
    """
    Create idea context object for session state storage
    
    Args:
        inputs: User input data
        category_scores: Category scores
        overall_score: Overall viability score
        classification: Viability classification
        recommendation: Recommendation text
        strengths: List of strengths
        watchouts: List of watchouts
    
    Returns:
        dict: Idea context for session state
    """
    return {
        "idea_title": inputs.get("idea_title", "Untitled Idea"),
        "idea_description": inputs.get("idea_description", ""),
        "target_customer": inputs.get("target_customer", ""),
        "location": inputs.get("location", ""),
        "revenue_approach": inputs.get("revenue_approach", ""),
        "viability_score": overall_score,
        "classification": classification,
        "category_scores": category_scores,
        "recommendation": recommendation,
        "strengths": strengths,
        "watchouts": watchouts,
        "source_module": "idea_screener"
    }


def get_category_label(category_key):
    """
    Get display label for category key
    
    Args:
        category_key: Category identifier
    
    Returns:
        str: Display label
    """
    labels = {
        "market_opportunity": "Market Opportunity",
        "revenue_potential": "Revenue Potential",
        "cost_feasibility": "Cost / Feasibility",
        "execution_readiness": "Execution Readiness",
        "risk_level": "Risk Level"
    }
    return labels.get(category_key, category_key)


def get_category_description(category_key):
    """
    Get description for category
    
    Args:
        category_key: Category identifier
    
    Returns:
        str: Category description
    """
    descriptions = {
        "market_opportunity": "Target customer clarity, demand strength, differentiation",
        "revenue_potential": "Pricing thought-through, realistic revenue model, earning potential",
        "cost_feasibility": "Cost understanding, operational practicality, financial realism",
        "execution_readiness": "Relevant experience, time/energy commitment, execution capacity",
        "risk_level": "Assumption uncertainty, competition, barriers and dependencies"
    }
    return descriptions.get(category_key, "")


def get_rating_guidance(category_key):
    """
    Get guidance for rating a category
    
    Args:
        category_key: Category identifier
    
    Returns:
        dict: Rating guidance with scale descriptions
    """
    guidance = {
        "market_opportunity": {
            1: "Unclear target customer, weak demand signal, no differentiation",
            3: "Some customer clarity, moderate demand, basic differentiation",
            5: "Crystal clear customer, strong demand, significant differentiation"
        },
        "revenue_potential": {
            1: "No pricing clarity, unrealistic model, limited potential",
            3: "Basic pricing concept, plausible model, moderate potential",
            5: "Well-thought pricing, realistic model, strong earning potential"
        },
        "cost_feasibility": {
            1: "Costs unclear, operationally difficult, financially unrealistic",
            3: "Costs somewhat understood, operationally feasible, financially plausible",
            5: "Costs well-understood, operationally practical, financially realistic"
        },
        "execution_readiness": {
            1: "No relevant experience, limited capacity, low commitment",
            3: "Some relevant experience, moderate capacity, reasonable commitment",
            5: "Strong relevant experience, high capacity, full commitment"
        },
        "risk_level": {
            1: "Low uncertainty, weak competition, few barriers",
            3: "Moderate uncertainty, some competition, manageable barriers",
            5: "High uncertainty, strong competition, significant barriers"
        }
    }
    return guidance.get(category_key, {})
