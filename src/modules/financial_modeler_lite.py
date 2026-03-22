"""
North Star Unified Shell - Financial Modeler Lite Module
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src.state.financial_state import (
    get_core_financials,
    sync_from_lite,
    get_sync_status
)


def render_financial_modeler_lite():
    """Render the Financial Modeler Lite module"""
    
    st.markdown("## 💰 Financial Modeler Lite")
    st.markdown("*Core financial analysis and scenario modeling for small businesses*")
    st.caption("🔄 Synced with core financial state")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📊 Model Inputs", "📈 Analysis", "💡 Insights"])
    
    with tab1:
        render_inputs_section()
    
    with tab2:
        render_analysis_section()
    
    with tab3:
        render_insights_section()


def render_inputs_section():
    """Render the inputs section"""
    st.markdown("### Business Financial Inputs")
    
    # Show idea context if available
    if "idea_context" in st.session_state:
        idea_ctx = st.session_state["idea_context"]
        st.info(f"💡 **Idea:** {idea_ctx['idea_title']} | **Viability Score:** {idea_ctx['viability_score']}/100")
    
    st.markdown('<div class="ns-card">', unsafe_allow_html=True)
    
    sync_status = get_sync_status()
    if sync_status["has_data"] and sync_status["source_module"] == "financial_modeler_pro":
        st.caption("💎 *Using values from Financial Modeler Pro*")
    
    core = get_core_financials()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Revenue Assumptions")
        
        default_revenue = int(core.get("revenue", 50000)) if core.get("revenue", 0) > 0 else 50000
        monthly_revenue = st.number_input(
            "Current Monthly Revenue ($)",
            min_value=0,
            value=default_revenue,
            step=1000,
            help="Enter your average monthly revenue"
        )
        
        default_growth = core.get("growth_rate", 0.05) * 100
        revenue_growth = st.slider(
            "Expected Monthly Growth Rate (%)",
            min_value=-10.0,
            max_value=20.0,
            value=float(default_growth),
            step=0.5,
            help="Expected month-over-month revenue growth"
        )
        
        default_months = core.get("projection_months", 12)
        default_index = [3, 6, 12, 24].index(default_months) if default_months in [3, 6, 12, 24] else 2
        projection_months = st.selectbox(
            "Projection Period (Months)",
            options=[3, 6, 12, 24],
            index=default_index,
            help="How far ahead to project"
        )
    
    with col2:
        st.markdown("#### Cost Structure")
        
        cogs_percent = st.slider(
            "Cost of Goods Sold (%)",
            min_value=0,
            max_value=100,
            value=40,
            step=5,
            help="COGS as percentage of revenue"
        )
        
        default_fixed = int(core.get("fixed_costs", 20000)) if core.get("fixed_costs", 0) > 0 else 20000
        fixed_costs = st.number_input(
            "Monthly Fixed Costs ($)",
            min_value=0,
            value=default_fixed,
            step=1000,
            help="Rent, salaries, utilities, etc."
        )
        
        variable_costs_percent = st.slider(
            "Variable Costs (%)",
            min_value=0,
            max_value=50,
            value=15,
            step=5,
            help="Variable costs as percentage of revenue"
        )
    
    if "fm_inputs" not in st.session_state:
        st.session_state.fm_inputs = {}
    
    st.session_state.fm_inputs = {
        "monthly_revenue": monthly_revenue,
        "revenue_growth": revenue_growth / 100,
        "projection_months": projection_months,
        "cogs_percent": cogs_percent / 100,
        "fixed_costs": fixed_costs,
        "variable_costs_percent": variable_costs_percent / 100,
    }
    
    st.divider()
    
    if st.button("🔄 Run Financial Model", type="primary", use_container_width=True):
        sync_from_lite(st.session_state.fm_inputs)
        st.success("✓ Model updated successfully")
        st.rerun()


def render_analysis_section():
    """Render the analysis and charts section"""
    
    if "fm_inputs" not in st.session_state or not st.session_state.fm_inputs:
        st.info("👈 Please configure inputs in the Model Inputs tab to see analysis")
        return
    
    inputs = st.session_state.fm_inputs
    
    df = generate_projection_data(inputs)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Monthly Revenue",
            f"${inputs['monthly_revenue']:,.0f}",
            delta=f"{inputs['revenue_growth']*100:.1f}% growth"
        )
    
    with col2:
        current_profit = calculate_monthly_profit(inputs['monthly_revenue'], inputs)
        st.metric(
            "Current Monthly Profit",
            f"${current_profit:,.0f}",
            delta=f"{(current_profit/inputs['monthly_revenue']*100):.1f}% margin"
        )
    
    with col3:
        final_revenue = df['Revenue'].iloc[-1]
        st.metric(
            f"Projected Revenue (Month {inputs['projection_months']})",
            f"${final_revenue:,.0f}",
            delta=f"{((final_revenue/inputs['monthly_revenue']-1)*100):.1f}% total growth"
        )
    
    with col4:
        final_profit = df['Net Profit'].iloc[-1]
        st.metric(
            f"Projected Profit (Month {inputs['projection_months']})",
            f"${final_profit:,.0f}",
            delta=f"{(final_profit/current_profit-1)*100:.1f}% vs current"
        )
    
    st.divider()
    
    st.markdown("### 📈 Revenue & Profit Projection")
    
    fig = create_projection_chart(df)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 📊 Detailed Projections")
    
    display_df = df.copy()
    for col in ['Revenue', 'COGS', 'Fixed Costs', 'Variable Costs', 'Net Profit']:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_insights_section():
    """Render the insights and recommendations section"""
    
    if "fm_inputs" not in st.session_state or not st.session_state.fm_inputs:
        st.info("👈 Please configure inputs and run the model to see insights")
        return
    
    inputs = st.session_state.fm_inputs
    
    st.markdown("### 💡 Key Insights & Recommendations")
    
    current_profit = calculate_monthly_profit(inputs['monthly_revenue'], inputs)
    profit_margin = (current_profit / inputs['monthly_revenue']) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Financial Health")
        
        if profit_margin > 20:
            st.success("✅ **Strong Profit Margin**")
            st.write(f"Your current profit margin of {profit_margin:.1f}% is healthy.")
        elif profit_margin > 10:
            st.info("ℹ️ **Moderate Profit Margin**")
            st.write(f"Your profit margin of {profit_margin:.1f}% has room for improvement.")
        else:
            st.warning("⚠️ **Low Profit Margin**")
            st.write(f"Your profit margin of {profit_margin:.1f}% may be concerning.")
        
        st.divider()
        
        total_costs_percent = inputs['cogs_percent'] + inputs['variable_costs_percent']
        st.markdown("#### 💰 Cost Structure")
        st.write(f"**Total Variable Costs:** {total_costs_percent*100:.0f}% of revenue")
        st.write(f"**Fixed Costs:** ${inputs['fixed_costs']:,.0f}/month")
        
        if total_costs_percent > 0.7:
            st.warning("High variable costs may limit profitability")
        else:
            st.success("Variable costs are well-controlled")
    
    with col2:
        st.markdown("#### 🎯 Growth Trajectory")
        
        if inputs['revenue_growth'] > 0.05:
            st.success("✅ **Strong Growth Expected**")
            st.write(f"Projected {inputs['revenue_growth']*100:.1f}% monthly growth")
        elif inputs['revenue_growth'] > 0:
            st.info("ℹ️ **Steady Growth Expected**")
            st.write(f"Projected {inputs['revenue_growth']*100:.1f}% monthly growth")
        else:
            st.warning("⚠️ **Declining Revenue Projected**")
            st.write("Consider strategies to reverse the trend")
        
        st.divider()
        
        st.markdown("#### 🔍 Recommendations")
        
        recommendations = generate_recommendations(inputs, profit_margin)
        for rec in recommendations:
            st.write(f"• {rec}")
    
    st.divider()
    
    st.info("💡 **Upgrade to Advisor Mode** for advanced scenario analysis, cash flow modeling, and valuation tools")


def generate_projection_data(inputs):
    """Generate projection data based on inputs"""
    months = []
    revenue = []
    cogs = []
    fixed = []
    variable = []
    profit = []
    
    current_revenue = inputs['monthly_revenue']
    
    for month in range(1, inputs['projection_months'] + 1):
        months.append(f"Month {month}")
        
        month_revenue = current_revenue * ((1 + inputs['revenue_growth']) ** (month - 1))
        revenue.append(month_revenue)
        
        month_cogs = month_revenue * inputs['cogs_percent']
        cogs.append(month_cogs)
        
        fixed.append(inputs['fixed_costs'])
        
        month_variable = month_revenue * inputs['variable_costs_percent']
        variable.append(month_variable)
        
        month_profit = month_revenue - month_cogs - inputs['fixed_costs'] - month_variable
        profit.append(month_profit)
    
    return pd.DataFrame({
        'Month': months,
        'Revenue': revenue,
        'COGS': cogs,
        'Fixed Costs': fixed,
        'Variable Costs': variable,
        'Net Profit': profit
    })


def calculate_monthly_profit(revenue, inputs):
    """Calculate monthly profit"""
    cogs = revenue * inputs['cogs_percent']
    variable = revenue * inputs['variable_costs_percent']
    return revenue - cogs - inputs['fixed_costs'] - variable


def create_projection_chart(df):
    """Create projection chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Month'],
        y=df['Revenue'],
        name='Revenue',
        line=dict(color='#1f77b4', width=3),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Month'],
        y=df['Net Profit'],
        name='Net Profit',
        line=dict(color='#2ca02c', width=3),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Revenue & Profit Projection',
        xaxis_title='Time Period',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def generate_recommendations(inputs, profit_margin):
    """Generate recommendations based on inputs"""
    recommendations = []
    
    if inputs['cogs_percent'] > 0.5:
        recommendations.append("Consider negotiating better supplier terms to reduce COGS")
    
    if profit_margin < 15:
        recommendations.append("Focus on improving profit margins through cost optimization or pricing strategy")
    
    if inputs['revenue_growth'] < 0.03:
        recommendations.append("Explore growth opportunities to accelerate revenue expansion")
    
    if inputs['fixed_costs'] > inputs['monthly_revenue'] * 0.5:
        recommendations.append("High fixed costs relative to revenue - consider operational efficiency improvements")
    
    if not recommendations:
        recommendations.append("Financial model looks healthy - maintain current trajectory")
        recommendations.append("Consider scenario planning for different growth rates")
    
    return recommendations
