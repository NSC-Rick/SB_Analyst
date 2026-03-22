"""
North Star Unified Shell - Entity Assistant Logic
Business entity structure recommendation engine
"""


def get_entity_recommendation(inputs):
    """
    Determine recommended business entity based on user inputs
    
    Args:
        inputs: dict with revenue, risk_level, hiring_plans, investor_intent, growth_ambition
    
    Returns:
        dict with entity, reasoning, considerations
    """
    revenue = inputs.get("revenue", 0)
    risk_level = inputs.get("risk_level", "medium")
    hiring_plans = inputs.get("hiring_plans", False)
    investor_intent = inputs.get("investor_intent", False)
    growth_ambition = inputs.get("growth_ambition", "lifestyle")
    
    # Decision tree logic
    if investor_intent:
        entity = "C-Corporation"
        reasoning = [
            "Investor-friendly structure with unlimited shareholders",
            "Preferred by venture capital and institutional investors",
            "Clear equity structure and stock classes",
            "Easier to raise capital and issue stock options"
        ]
        considerations = [
            "Double taxation (corporate + personal)",
            "More complex compliance and reporting",
            "Higher formation and maintenance costs",
            "Board of directors requirements"
        ]
    
    elif risk_level == "high":
        entity = "LLC (Limited Liability Company)"
        reasoning = [
            "Strong liability protection for high-risk business",
            "Separates personal assets from business liabilities",
            "Flexible management structure",
            "Pass-through taxation (avoids double taxation)"
        ]
        considerations = [
            "Self-employment taxes on all profits",
            "May need operating agreement",
            "State-specific regulations vary",
            "Consider S-Corp election for tax savings"
        ]
    
    elif revenue < 100000:
        if risk_level == "low":
            entity = "Sole Proprietorship"
            reasoning = [
                "Simplest and lowest-cost structure",
                "Easy to set up and maintain",
                "Complete control over business",
                "Minimal compliance requirements"
            ]
            considerations = [
                "No liability protection (personal assets at risk)",
                "Harder to raise capital",
                "Business ends if owner dies",
                "Consider LLC as business grows"
            ]
        else:
            entity = "LLC (Limited Liability Company)"
            reasoning = [
                "Liability protection at reasonable cost",
                "Simple formation and maintenance",
                "Pass-through taxation",
                "Professional image for clients"
            ]
            considerations = [
                "Annual fees and filings required",
                "Self-employment taxes apply",
                "May need operating agreement",
                "State-specific requirements"
            ]
    
    elif revenue >= 100000 or hiring_plans:
        entity = "LLC with S-Corp Election"
        reasoning = [
            "Liability protection of LLC",
            "Tax savings through reasonable salary + distributions",
            "Reduces self-employment tax burden",
            "Maintains flexibility of LLC"
        ]
        considerations = [
            "Must run payroll for owner(s)",
            "Reasonable salary requirement (IRS scrutiny)",
            "More complex tax filing (1120-S)",
            "Payroll tax and compliance costs"
        ]
    
    elif growth_ambition == "high-growth":
        entity = "C-Corporation"
        reasoning = [
            "Best structure for rapid scaling",
            "Easier to attract investors and employees",
            "Can issue stock options and equity",
            "Professional structure for partnerships"
        ]
        considerations = [
            "Double taxation on profits",
            "Higher compliance costs",
            "Board and shareholder requirements",
            "More complex to operate"
        ]
    
    else:
        entity = "LLC (Limited Liability Company)"
        reasoning = [
            "Balanced structure for most small businesses",
            "Liability protection with tax flexibility",
            "Can elect S-Corp status later if beneficial",
            "Simpler than corporation, safer than sole proprietorship"
        ]
        considerations = [
            "Annual state fees required",
            "Operating agreement recommended",
            "Self-employment taxes on profits",
            "May need professional tax advice"
        ]
    
    return {
        "entity": entity,
        "reasoning": reasoning,
        "considerations": considerations
    }


def get_entity_comparison():
    """
    Get comparison table of all entity types
    
    Returns:
        dict: Entity type -> characteristics
    """
    return {
        "Sole Proprietorship": {
            "liability": "❌ None - Personal assets at risk",
            "taxation": "Pass-through (Schedule C)",
            "complexity": "⭐ Very Simple",
            "cost": "💰 $0-50",
            "best_for": "Low-risk, solo, under $50K revenue"
        },
        "LLC": {
            "liability": "✅ Full Protection",
            "taxation": "Pass-through (default) or S-Corp election",
            "complexity": "⭐⭐ Simple",
            "cost": "💰💰 $100-800/year",
            "best_for": "Most small businesses, any risk level"
        },
        "S-Corporation": {
            "liability": "✅ Full Protection",
            "taxation": "Pass-through with payroll",
            "complexity": "⭐⭐⭐ Moderate",
            "cost": "💰💰💰 $500-2000/year",
            "best_for": "$50K+ revenue, hiring employees"
        },
        "C-Corporation": {
            "liability": "✅ Full Protection",
            "taxation": "Double taxation",
            "complexity": "⭐⭐⭐⭐ Complex",
            "cost": "💰💰💰💰 $1000-5000+/year",
            "best_for": "Seeking investors, high growth"
        }
    }


def get_next_steps(entity):
    """
    Get actionable next steps for chosen entity
    
    Args:
        entity: Recommended entity type
    
    Returns:
        list: Next steps to take
    """
    if entity == "Sole Proprietorship":
        return [
            "1. Obtain business licenses (city/county)",
            "2. Register DBA (Doing Business As) if using business name",
            "3. Get EIN from IRS (optional but recommended)",
            "4. Open business bank account",
            "5. Set up accounting system",
            "6. Get business insurance"
        ]
    
    elif "LLC" in entity:
        return [
            "1. File Articles of Organization with your state",
            "2. Get EIN from IRS",
            "3. Create Operating Agreement",
            "4. Open business bank account",
            "5. Register for state taxes if applicable",
            "6. Get business insurance",
            "7. Consider S-Corp election if revenue > $50K"
        ]
    
    elif "S-Corp" in entity or entity == "S-Corporation":
        return [
            "1. Form LLC or Corporation with your state",
            "2. Get EIN from IRS",
            "3. File Form 2553 for S-Corp election",
            "4. Set up payroll system",
            "5. Determine reasonable salary",
            "6. Open business bank account",
            "7. Hire accountant/bookkeeper"
        ]
    
    elif "C-Corp" in entity or entity == "C-Corporation":
        return [
            "1. File Articles of Incorporation with your state",
            "2. Get EIN from IRS",
            "3. Create corporate bylaws",
            "4. Issue stock certificates",
            "5. Hold organizational board meeting",
            "6. Open business bank account",
            "7. Set up corporate record keeping",
            "8. Hire corporate attorney and accountant"
        ]
    
    else:
        return [
            "1. Consult with business attorney",
            "2. Consult with tax professional",
            "3. File formation documents with state",
            "4. Get EIN from IRS",
            "5. Open business bank account"
        ]


def get_tax_implications(entity, revenue):
    """
    Get tax implications for entity type
    
    Args:
        entity: Entity type
        revenue: Expected annual revenue
    
    Returns:
        dict: Tax information
    """
    if entity == "Sole Proprietorship":
        return {
            "federal": "Schedule C (Form 1040)",
            "self_employment": "15.3% on all net profit",
            "estimated_taxes": "Quarterly payments required",
            "deductions": "Standard business deductions",
            "savings_opportunity": "Limited - all profit taxed"
        }
    
    elif "LLC" in entity and "S-Corp" not in entity:
        return {
            "federal": "Schedule C (Form 1040) or Partnership return",
            "self_employment": "15.3% on all net profit",
            "estimated_taxes": "Quarterly payments required",
            "deductions": "Standard business deductions",
            "savings_opportunity": "Consider S-Corp election if profit > $40K"
        }
    
    elif "S-Corp" in entity:
        potential_savings = 0
        if revenue > 100000:
            profit = revenue * 0.3  # Assume 30% margin
            salary = min(profit * 0.6, 100000)  # 60% as salary
            distributions = profit - salary
            potential_savings = distributions * 0.153  # SE tax saved
        
        return {
            "federal": "Form 1120-S",
            "self_employment": "Only on salary portion (not distributions)",
            "estimated_taxes": "Payroll taxes + quarterly on distributions",
            "deductions": "Business deductions + payroll costs",
            "savings_opportunity": f"Potential ${potential_savings:,.0f}/year in SE tax savings"
        }
    
    elif "C-Corp" in entity:
        return {
            "federal": "Form 1120",
            "self_employment": "N/A (W-2 employee)",
            "estimated_taxes": "Corporate tax + personal tax on salary/dividends",
            "deductions": "Corporate deductions + fringe benefits",
            "savings_opportunity": "Retain earnings at lower corporate rate (21%)"
        }
    
    else:
        return {
            "federal": "Varies by entity",
            "self_employment": "Consult tax professional",
            "estimated_taxes": "Likely required",
            "deductions": "Standard business deductions",
            "savings_opportunity": "Consult CPA for optimization"
        }


def create_entity_context(inputs, recommendation):
    """
    Create entity context for downstream modules
    
    Args:
        inputs: User inputs
        recommendation: Entity recommendation result
    
    Returns:
        dict: Entity context
    """
    return {
        "entity_type": recommendation["entity"],
        "revenue_expectation": inputs.get("revenue", 0),
        "risk_level": inputs.get("risk_level", "medium"),
        "growth_ambition": inputs.get("growth_ambition", "lifestyle"),
        "investor_intent": inputs.get("investor_intent", False),
        "hiring_plans": inputs.get("hiring_plans", False),
        "recommendation_reasoning": recommendation["reasoning"],
        "considerations": recommendation["considerations"]
    }
