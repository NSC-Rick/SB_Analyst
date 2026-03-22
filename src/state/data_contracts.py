"""
North Star Unified Shell - Data Contracts
Global data schemas and system keys for cross-module consistency
"""

# ===== CORE FINANCIAL SCHEMA =====
CORE_FINANCIALS_SCHEMA = {
    "revenue": float,
    "expenses": float,
    "profit": float,
    "growth_rate": float,
    "projection_months": int,
    "cogs": float,
    "operating_expenses": float,
    "cash_on_hand": float,
}

# ===== VALUATION SCHEMA =====
VALUATION_SCHEMA = {
    "valuation_range": tuple,  # (low, high)
    "primary_method": str,
    "revenue_multiple": float,
    "earnings_multiple": float,
    "confidence_level": str,
}

# ===== LOC RECOMMENDATION SCHEMA =====
LOC_SCHEMA = {
    "recommended_amount": float,
    "utilization_rate": float,
    "monthly_payment": float,
    "purpose": str,
    "risk_level": str,
}

# ===== PROJECT EVALUATION SCHEMA =====
PROJECT_SCHEMA = {
    "overall_score": int,
    "priority_classification": str,
    "market_score": int,
    "financial_score": int,
    "execution_score": int,
    "risk_score": int,
}

# ===== IDEA CONTEXT SCHEMA =====
IDEA_SCHEMA = {
    "idea_title": str,
    "viability_score": int,
    "market_rating": int,
    "revenue_rating": int,
    "competition_rating": int,
    "execution_rating": int,
}

# ===== ENTITY STRUCTURE SCHEMA =====
ENTITY_SCHEMA = {
    "entity_type": str,
    "reasoning": str,
    "tax_implications": dict,
    "next_steps": list,
}

# ===== CAPITAL STACK SCHEMA =====
CAPITAL_STACK_SCHEMA = {
    "total_capital_need": float,
    "equity_amount": float,
    "debt_amount": float,
    "loc_amount": float,
    "structure": dict,
}

# ===== SYSTEM STATE KEYS =====
# All critical keys that should exist in st.session_state
SYSTEM_KEYS = [
    "core_financials",
    "valuation_range",
    "loc_recommendation",
    "project_evaluation",
    "idea_context",
    "entity_structure",
    "capital_stack",
]

# ===== REQUIRED KEYS FOR EACH MODULE =====
MODULE_REQUIREMENTS = {
    "Financial Modeler Lite": {
        "writes": ["core_financials"],
        "reads": [],
    },
    "Financial Modeler Pro": {
        "writes": ["core_financials"],
        "reads": ["core_financials"],
    },
    "Business Valuation": {
        "writes": ["valuation_range"],
        "reads": ["core_financials"],
    },
    "LOC Analyzer": {
        "writes": ["loc_recommendation"],
        "reads": ["core_financials"],
    },
    "Project Evaluator": {
        "writes": ["project_evaluation"],
        "reads": ["core_financials"],  # optional
    },
    "Idea Screener": {
        "writes": ["idea_context"],
        "reads": [],
    },
    "Entity Assistant": {
        "writes": ["entity_structure"],
        "reads": ["idea_context", "core_financials"],  # optional
    },
    "Capital Stack": {
        "writes": ["capital_stack"],
        "reads": ["core_financials", "valuation_range", "loc_recommendation", "project_evaluation"],
    },
    "Insights Engine": {
        "writes": [],
        "reads": ["core_financials", "valuation_range", "loc_recommendation", "project_evaluation", "capital_stack"],
    },
}

# ===== DEFAULT VALUES =====
DEFAULT_CORE_FINANCIALS = {
    "revenue": 0.0,
    "expenses": 0.0,
    "profit": 0.0,
    "growth_rate": 0.0,
    "projection_months": 12,
    "cogs": 0.0,
    "operating_expenses": 0.0,
    "cash_on_hand": 0.0,
}

# ===== DATA INTEGRITY RULES =====
INTEGRITY_RULES = {
    "profit_calculation": "profit = revenue - expenses",
    "growth_rate_range": (-1.0, 5.0),  # -100% to 500%
    "projection_months_range": (1, 60),  # 1 to 60 months
    "valuation_positive": "valuation must be > 0",
    "loc_positive": "loc_amount must be >= 0",
    "score_range": (0, 100),  # All scores 0-100
}

# ===== SYNC STATUS TRACKING =====
SYNC_INDICATORS = {
    "synced": "🔄 Synced with core financial state",
    "partial": "⚠️ Partially synced - some data may be outdated",
    "unsynced": "❌ Not synced - using local data only",
}
