"""
North Star Unified Shell - Financial Modeler Pro Module
Advanced financial modeling with expanded inputs and detailed analysis
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.state.financial_state import (
    get_core_financials,
    sync_from_pro,
    get_sync_status
)


def render_financial_modeler_pro():
    """Render the Financial Modeler Pro module"""
    
    st.markdown("## 💎 Financial Modeler Pro")
    st.markdown("*Advanced financial modeling with multi-stream revenue, detailed cost structure, and comprehensive projections*")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📊 Inputs", "📈 Analysis", "💡 Insights"])
    
    with tab1:
        render_pro_inputs()
    
    with tab2:
        render_pro_analysis()
    
    with tab3:
        render_pro_insights()


def render_pro_inputs():
    """Render the expanded inputs section for Pro"""
    
    st.markdown("### 🎯 Advanced Business Financial Inputs")
    st.caption("Build detailed financial projections with multiple revenue streams and granular cost modeling")
    
    sync_status = get_sync_status()
    if sync_status["has_data"] and sync_status["source_module"] == "financial_modeler_lite":
        st.caption("💰 *Using baseline from Financial Modeler Lite*")
    
    st.divider()
    
    revenue_section()
    
    st.divider()
    
    costs_section()
    
    st.divider()
    
    labor_section()
    
    st.divider()
    
    growth_assumptions_section()
    
    st.divider()
    
    if st.button("🔄 Run Pro Financial Model", type="primary", use_container_width=True):
        if validate_pro_inputs():
            sync_from_pro(
                st.session_state.pro_revenue_streams,
                st.session_state.pro_costs,
                st.session_state.pro_labor,
                st.session_state.pro_assumptions
            )
        st.success("✓ Pro model updated successfully")
        st.rerun()


def revenue_section():
    """Revenue inputs with multiple streams"""
    
    st.markdown("#### 💰 Revenue Streams")
    
    num_streams = st.number_input(
        "Number of Revenue Streams",
        min_value=1,
        max_value=5,
        value=2,
        help="Model up to 5 different revenue sources"
    )
    
    if "pro_revenue_streams" not in st.session_state:
        st.session_state.pro_revenue_streams = []
    
    streams = []
    
    for i in range(num_streams):
        with st.expander(f"Revenue Stream {i+1}", expanded=(i == 0)):
            col1, col2 = st.columns(2)
            
            with col1:
                stream_name = st.text_input(
                    "Stream Name",
                    value=f"Product/Service {i+1}",
                    key=f"stream_name_{i}"
                )
                
                price = st.number_input(
                    "Average Price ($)",
                    min_value=0.0,
                    value=100.0,
                    step=10.0,
                    key=f"price_{i}",
                    help="Average price per unit/transaction"
                )
            
            with col2:
                volume = st.number_input(
                    "Monthly Volume (units)",
                    min_value=0,
                    value=50,
                    step=10,
                    key=f"volume_{i}",
                    help="Number of units sold per month"
                )
                
                growth = st.slider(
                    "Monthly Growth Rate (%)",
                    min_value=-10.0,
                    max_value=30.0,
                    value=5.0,
                    step=0.5,
                    key=f"growth_{i}"
                )
            
            monthly_revenue = price * volume
            st.metric("Monthly Revenue", f"${monthly_revenue:,.0f}")
            
            streams.append({
                "name": stream_name,
                "price": price,
                "volume": volume,
                "growth": growth / 100,
                "monthly_revenue": monthly_revenue
            })
    
    st.session_state.pro_revenue_streams = streams
    
    total_revenue = sum(s["monthly_revenue"] for s in streams)
    st.success(f"**Total Monthly Revenue:** ${total_revenue:,.0f}")


def costs_section():
    """Cost structure inputs"""
    
    st.markdown("#### 💸 Cost Structure")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variable Costs**")
        
        cogs_percent = st.slider(
            "Cost of Goods Sold (% of revenue)",
            min_value=0,
            max_value=100,
            value=35,
            step=5,
            help="Direct costs to produce/deliver product or service"
        )
        
        other_variable_percent = st.slider(
            "Other Variable Costs (% of revenue)",
            min_value=0,
            max_value=50,
            value=10,
            step=5,
            help="Sales commissions, transaction fees, etc."
        )
    
    with col2:
        st.markdown("**Fixed Costs**")
        
        rent = st.number_input(
            "Rent / Facilities ($)",
            min_value=0,
            value=3000,
            step=500
        )
        
        utilities = st.number_input(
            "Utilities & Services ($)",
            min_value=0,
            value=500,
            step=100
        )
        
        insurance = st.number_input(
            "Insurance ($)",
            min_value=0,
            value=500,
            step=100
        )
        
        marketing = st.number_input(
            "Marketing & Advertising ($)",
            min_value=0,
            value=2000,
            step=500
        )
        
        other_fixed = st.number_input(
            "Other Fixed Costs ($)",
            min_value=0,
            value=1000,
            step=500,
            help="Software, subscriptions, professional fees, etc."
        )
    
    if "pro_costs" not in st.session_state:
        st.session_state.pro_costs = {}
    
    st.session_state.pro_costs = {
        "cogs_percent": cogs_percent / 100,
        "other_variable_percent": other_variable_percent / 100,
        "rent": rent,
        "utilities": utilities,
        "insurance": insurance,
        "marketing": marketing,
        "other_fixed": other_fixed,
        "total_fixed": rent + utilities + insurance + marketing + other_fixed
    }
    
    st.info(f"**Total Fixed Costs:** ${st.session_state.pro_costs['total_fixed']:,.0f}/month")


def labor_section():
    """Labor/payroll inputs"""
    
    st.markdown("#### 👥 Labor & Payroll")
    
    labor_method = st.radio(
        "Payroll Entry Method",
        ["Simple Total", "By Role"],
        horizontal=True
    )
    
    if labor_method == "Simple Total":
        total_payroll = st.number_input(
            "Total Monthly Payroll ($)",
            min_value=0,
            value=15000,
            step=1000,
            help="Total monthly payroll including owner compensation"
        )
        
        labor_data = {
            "method": "simple",
            "total_payroll": total_payroll,
            "roles": []
        }
    
    else:
        st.caption("Define key roles and compensation")
        
        num_roles = st.number_input(
            "Number of Role Categories",
            min_value=1,
            max_value=5,
            value=2
        )
        
        roles = []
        total_payroll = 0
        
        for i in range(num_roles):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                role_name = st.text_input(
                    "Role/Category",
                    value=f"Role {i+1}",
                    key=f"role_name_{i}"
                )
            
            with col2:
                headcount = st.number_input(
                    "Headcount",
                    min_value=0,
                    value=1,
                    key=f"headcount_{i}"
                )
            
            with col3:
                avg_salary = st.number_input(
                    "Avg Monthly Pay ($)",
                    min_value=0,
                    value=5000,
                    step=500,
                    key=f"salary_{i}"
                )
            
            role_total = headcount * avg_salary
            total_payroll += role_total
            
            roles.append({
                "name": role_name,
                "headcount": headcount,
                "avg_salary": avg_salary,
                "total": role_total
            })
        
        labor_data = {
            "method": "by_role",
            "total_payroll": total_payroll,
            "roles": roles
        }
    
    st.session_state.pro_labor = labor_data
    st.success(f"**Total Monthly Payroll:** ${total_payroll:,.0f}")


def growth_assumptions_section():
    """Growth and projection assumptions"""
    
    st.markdown("#### 📈 Growth & Projection Assumptions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        projection_months = st.selectbox(
            "Projection Period",
            options=[6, 12, 24, 36],
            index=1,
            help="How many months to project forward"
        )
        
        view_mode = st.radio(
            "View Mode",
            ["Monthly", "Annual"],
            horizontal=True
        )
    
    with col2:
        sensitivity_analysis = st.checkbox(
            "Include Sensitivity Analysis",
            value=False,
            help="Show best/base/worst case scenarios"
        )
        
        if sensitivity_analysis:
            sensitivity_range = st.slider(
                "Sensitivity Range (±%)",
                min_value=5,
                max_value=30,
                value=15,
                step=5
            )
        else:
            sensitivity_range = 0
    
    if "pro_assumptions" not in st.session_state:
        st.session_state.pro_assumptions = {}
    
    st.session_state.pro_assumptions = {
        "projection_months": projection_months,
        "view_mode": view_mode,
        "sensitivity_analysis": sensitivity_analysis,
        "sensitivity_range": sensitivity_range / 100 if sensitivity_analysis else 0
    }


def render_pro_analysis():
    """Render the analysis section with projections and charts"""
    
    if not validate_pro_inputs():
        st.info("👈 Please configure inputs in the **Inputs** tab to see analysis")
        return
    
    st.markdown("### 📊 Financial Projections & Analysis")
    
    projections = calculate_pro_projections()
    
    render_key_metrics(projections)
    
    st.divider()
    
    render_projection_charts(projections)
    
    st.divider()
    
    render_detailed_projections_table(projections)
    
    if st.session_state.pro_assumptions.get("sensitivity_analysis"):
        st.divider()
        render_sensitivity_analysis(projections)


def validate_pro_inputs():
    """Check if required Pro inputs are available"""
    return (
        "pro_revenue_streams" in st.session_state and
        "pro_costs" in st.session_state and
        "pro_labor" in st.session_state and
        "pro_assumptions" in st.session_state
    )


def calculate_pro_projections():
    """Calculate detailed projections based on Pro inputs"""
    
    streams = st.session_state.pro_revenue_streams
    costs = st.session_state.pro_costs
    labor = st.session_state.pro_labor
    assumptions = st.session_state.pro_assumptions
    
    months = assumptions["projection_months"]
    
    projections = []
    
    for month in range(1, months + 1):
        month_revenue = 0
        
        for stream in streams:
            stream_revenue = stream["monthly_revenue"] * ((1 + stream["growth"]) ** (month - 1))
            month_revenue += stream_revenue
        
        cogs = month_revenue * costs["cogs_percent"]
        other_variable = month_revenue * costs["other_variable_percent"]
        total_variable = cogs + other_variable
        
        total_fixed = costs["total_fixed"]
        payroll = labor["total_payroll"]
        
        total_expenses = total_variable + total_fixed + payroll
        
        profit = month_revenue - total_expenses
        margin = (profit / month_revenue * 100) if month_revenue > 0 else 0
        
        projections.append({
            "month": month,
            "revenue": month_revenue,
            "cogs": cogs,
            "other_variable": other_variable,
            "total_variable": total_variable,
            "fixed_costs": total_fixed,
            "payroll": payroll,
            "total_expenses": total_expenses,
            "profit": profit,
            "margin": margin
        })
    
    return projections


def render_key_metrics(projections):
    """Render key financial metrics"""
    
    current = projections[0]
    final = projections[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Monthly Revenue",
            f"${current['revenue']:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Current Monthly Profit",
            f"${current['profit']:,.0f}",
            delta=f"{current['margin']:.1f}% margin"
        )
    
    with col3:
        revenue_growth = ((final['revenue'] / current['revenue'] - 1) * 100)
        st.metric(
            f"Projected Revenue (Month {len(projections)})",
            f"${final['revenue']:,.0f}",
            delta=f"+{revenue_growth:.1f}%"
        )
    
    with col4:
        st.metric(
            f"Projected Profit (Month {len(projections)})",
            f"${final['profit']:,.0f}",
            delta=f"{final['margin']:.1f}% margin"
        )


def render_projection_charts(projections):
    """Render projection charts"""
    
    st.markdown("### 📈 Revenue & Profitability Trends")
    
    df = pd.DataFrame(projections)
    
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Revenue & Profit Projection', 'Profit Margin Trend'),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['month'],
            y=df['revenue'],
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['month'],
            y=df['profit'],
            name='Profit',
            line=dict(color='#2ca02c', width=3),
            mode='lines+markers'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['month'],
            y=df['margin'],
            name='Profit Margin %',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            fill='tozeroy'
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Month", row=2, col=1)
    fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
    fig.update_yaxes(title_text="Margin (%)", row=2, col=1)
    
    fig.update_layout(height=600, showlegend=True, hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_projections_table(projections):
    """Render detailed projections table"""
    
    st.markdown("### 📋 Detailed Monthly Projections")
    
    df = pd.DataFrame(projections)
    
    display_df = df.copy()
    display_df['Month'] = display_df['month']
    display_df['Revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
    display_df['Total Expenses'] = display_df['total_expenses'].apply(lambda x: f"${x:,.0f}")
    display_df['Profit'] = display_df['profit'].apply(lambda x: f"${x:,.0f}")
    display_df['Margin %'] = display_df['margin'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        display_df[['Month', 'Revenue', 'Total Expenses', 'Profit', 'Margin %']],
        use_container_width=True,
        hide_index=True
    )
    
    with st.expander("📊 View Detailed Cost Breakdown"):
        breakdown_df = df.copy()
        breakdown_df['Month'] = breakdown_df['month']
        breakdown_df['COGS'] = breakdown_df['cogs'].apply(lambda x: f"${x:,.0f}")
        breakdown_df['Variable'] = breakdown_df['other_variable'].apply(lambda x: f"${x:,.0f}")
        breakdown_df['Fixed'] = breakdown_df['fixed_costs'].apply(lambda x: f"${x:,.0f}")
        breakdown_df['Payroll'] = breakdown_df['payroll'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(
            breakdown_df[['Month', 'COGS', 'Variable', 'Fixed', 'Payroll']],
            use_container_width=True,
            hide_index=True
        )


def render_sensitivity_analysis(projections):
    """Render sensitivity analysis"""
    
    st.markdown("### 🎯 Sensitivity Analysis")
    st.caption("Best case, base case, and worst case scenarios")
    
    sensitivity = st.session_state.pro_assumptions["sensitivity_range"]
    
    final = projections[-1]
    
    best_revenue = final['revenue'] * (1 + sensitivity)
    worst_revenue = final['revenue'] * (1 - sensitivity)
    
    best_profit = final['profit'] * (1 + sensitivity)
    worst_profit = final['profit'] * (1 - sensitivity)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📉 Worst Case")
        st.metric("Revenue", f"${worst_revenue:,.0f}")
        st.metric("Profit", f"${worst_profit:,.0f}")
        st.caption(f"-{sensitivity*100:.0f}% scenario")
    
    with col2:
        st.markdown("#### 📊 Base Case")
        st.metric("Revenue", f"${final['revenue']:,.0f}")
        st.metric("Profit", f"${final['profit']:,.0f}")
        st.caption("Current projection")
    
    with col3:
        st.markdown("#### 📈 Best Case")
        st.metric("Revenue", f"${best_revenue:,.0f}")
        st.metric("Profit", f"${best_profit:,.0f}")
        st.caption(f"+{sensitivity*100:.0f}% scenario")


def render_pro_insights():
    """Render insights and recommendations for Pro"""
    
    if not validate_pro_inputs():
        st.info("👈 Please configure inputs and run the model to see insights")
        return
    
    st.markdown("### 💡 Advanced Insights & Recommendations")
    
    projections = calculate_pro_projections()
    
    render_revenue_stream_analysis()
    
    st.divider()
    
    render_cost_structure_analysis()
    
    st.divider()
    
    render_profitability_insights(projections)
    
    st.divider()
    
    render_strategic_recommendations(projections)


def render_revenue_stream_analysis():
    """Analyze revenue stream composition"""
    
    st.markdown("#### 💰 Revenue Stream Analysis")
    
    streams = st.session_state.pro_revenue_streams
    
    total_revenue = sum(s["monthly_revenue"] for s in streams)
    
    for stream in streams:
        contribution = (stream["monthly_revenue"] / total_revenue * 100) if total_revenue > 0 else 0
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{stream['name']}**")
        
        with col2:
            st.write(f"${stream['monthly_revenue']:,.0f}")
        
        with col3:
            st.write(f"{contribution:.1f}%")
    
    if len(streams) > 1:
        max_stream = max(streams, key=lambda x: x["monthly_revenue"])
        max_contribution = (max_stream["monthly_revenue"] / total_revenue * 100)
        
        if max_contribution > 70:
            st.warning(f"⚠️ High concentration: {max_stream['name']} represents {max_contribution:.0f}% of revenue. Consider diversification.")
        else:
            st.success("✓ Revenue streams show healthy diversification")


def render_cost_structure_analysis():
    """Analyze cost structure"""
    
    st.markdown("#### 💸 Cost Structure Analysis")
    
    costs = st.session_state.pro_costs
    labor = st.session_state.pro_labor
    
    streams = st.session_state.pro_revenue_streams
    total_revenue = sum(s["monthly_revenue"] for s in streams)
    
    total_variable_percent = costs["cogs_percent"] + costs["other_variable_percent"]
    fixed_percent = (costs["total_fixed"] / total_revenue * 100) if total_revenue > 0 else 0
    labor_percent = (labor["total_payroll"] / total_revenue * 100) if total_revenue > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Variable Costs", f"{total_variable_percent*100:.0f}%", "of revenue")
    
    with col2:
        st.metric("Fixed Costs", f"{fixed_percent:.0f}%", "of revenue")
    
    with col3:
        st.metric("Labor Costs", f"{labor_percent:.0f}%", "of revenue")
    
    if total_variable_percent > 0.6:
        st.warning("⚠️ High variable costs may limit scalability. Explore ways to reduce COGS or improve pricing.")
    
    if fixed_percent > 40:
        st.warning("⚠️ High fixed cost burden. Consider variable cost alternatives or revenue growth to improve leverage.")


def render_profitability_insights(projections):
    """Render profitability insights"""
    
    st.markdown("#### 📊 Profitability Analysis")
    
    current = projections[0]
    final = projections[-1]
    
    avg_margin = sum(p["margin"] for p in projections) / len(projections)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Current Margin", f"{current['margin']:.1f}%")
        st.metric("Projected Margin", f"{final['margin']:.1f}%")
    
    with col2:
        st.metric("Average Margin", f"{avg_margin:.1f}%")
        
        if final['margin'] > current['margin']:
            improvement = final['margin'] - current['margin']
            st.success(f"✓ Margin improving by {improvement:.1f} percentage points")
        elif final['margin'] < current['margin']:
            decline = current['margin'] - final['margin']
            st.warning(f"⚠️ Margin declining by {decline:.1f} percentage points")
    
    if avg_margin > 20:
        st.success("💎 Strong profitability - well-positioned for growth and investment")
    elif avg_margin > 10:
        st.info("📊 Moderate profitability - focus on margin improvement opportunities")
    else:
        st.warning("⚠️ Low margins - prioritize cost reduction and pricing optimization")


def render_strategic_recommendations(projections):
    """Render strategic recommendations"""
    
    st.markdown("#### 🎯 Strategic Recommendations")
    
    recommendations = []
    
    streams = st.session_state.pro_revenue_streams
    costs = st.session_state.pro_costs
    labor = st.session_state.pro_labor
    
    total_revenue = sum(s["monthly_revenue"] for s in streams)
    total_variable_percent = costs["cogs_percent"] + costs["other_variable_percent"]
    
    if len(streams) == 1:
        recommendations.append("💡 Consider adding additional revenue streams to reduce concentration risk")
    
    if total_variable_percent > 0.5:
        recommendations.append("💡 High variable costs detected - explore supplier negotiations or pricing adjustments")
    
    avg_growth = sum(s["growth"] for s in streams) / len(streams)
    if avg_growth < 0.03:
        recommendations.append("💡 Low growth projections - identify opportunities to accelerate revenue expansion")
    
    current = projections[0]
    if current['margin'] < 15:
        recommendations.append("💡 Improve profitability through operational efficiency or premium pricing strategies")
    
    if labor["total_payroll"] / total_revenue > 0.4:
        recommendations.append("💡 Labor costs are high relative to revenue - consider productivity improvements or automation")
    
    if not recommendations:
        recommendations.append("✓ Financial model shows solid fundamentals - maintain current trajectory")
        recommendations.append("💡 Explore Financial Modeler Pro's sensitivity analysis to stress-test assumptions")
    
    for rec in recommendations:
        st.info(rec)
    
    st.divider()
    
    st.markdown("#### 🚀 Next Steps")
    st.write("**Recommended actions based on your Pro model:**")
    st.markdown("- Use **Value Engine** to estimate business valuation based on these projections")
    st.markdown("- Explore **Funding Engine** to model capital needs and financing options")
    st.markdown("- Return to **Inputs** tab to model different scenarios and growth strategies")
