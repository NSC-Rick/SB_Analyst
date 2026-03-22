"""
LOC Analyzer - Cash Trough Engine UI Module
Line of credit analysis and working capital planning
"""
import streamlit as st
import plotly.graph_objects as go
from src.modules.loc_logic import (
    project_cash_flow,
    identify_cash_trough,
    calculate_loc_recommendation,
    generate_loc_insights,
    calculate_working_capital_metrics,
    simulate_loc_usage
)
from src.state.financial_state import (
    get_core_financials,
    has_financial_data,
    get_sync_status
)


def render_loc_analyzer():
    """Main render function for LOC Analyzer module"""
    
    st.markdown("## 💳 LOC Analyzer (Cash Trough Engine)")
    st.markdown("*Identify cash flow gaps and determine working capital requirements*")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💡 Insights", "📋 Details"])
    
    with tab1:
        render_analysis_tab()
    
    with tab2:
        render_insights_tab()
    
    with tab3:
        render_details_tab()


def render_analysis_tab():
    """Render the main analysis tab with inputs and results"""
    
    st.markdown("### 💰 Cash Flow Inputs")
    
    input_data = render_input_section()
    
    if input_data:
        st.divider()
        
        cash_flow_data = project_cash_flow(
            starting_cash=input_data["starting_cash"],
            monthly_revenue=input_data["monthly_revenue"],
            monthly_expenses=input_data["monthly_expenses"],
            months=input_data["projection_months"],
            revenue_growth=input_data["revenue_growth"],
            expense_growth=input_data["expense_growth"]
        )
        
        trough_data = identify_cash_trough(cash_flow_data["cash_balance"])
        
        loc_data = calculate_loc_recommendation(
            lowest_cash=trough_data["lowest_cash"],
            safety_buffer=input_data["safety_buffer"],
            stress_buffer=input_data["stress_buffer"]
        )
        
        if "loc_analysis" not in st.session_state:
            st.session_state.loc_analysis = {}
        
        st.session_state.loc_analysis = {
            "cash_flow": cash_flow_data,
            "trough": trough_data,
            "loc": loc_data,
            "inputs": input_data
        }
        
        render_loc_recommendation(loc_data, trough_data)
        
        st.divider()
        
        render_cash_flow_chart(cash_flow_data, trough_data, loc_data)
        
        st.divider()
        
        render_loc_simulation(cash_flow_data, loc_data)


def render_input_section():
    """Render input section with data source options"""
    
    st.markdown("#### 📥 Data Source")
    
    sync_status = get_sync_status()
    
    if has_financial_data():
        default_source = "Use Shared Financial Data"
    else:
        default_source = "Manual Entry"
    
    data_source_options = ["Use Shared Financial Data", "Manual Entry"]
    default_index = data_source_options.index(default_source)
    
    data_source = st.radio(
        "Select Input Method",
        data_source_options,
        index=default_index,
        horizontal=True
    )
    
    if data_source == "Use Shared Financial Data":
        input_data = pull_from_shared_state()
        if not input_data:
            st.warning("⚠️ No shared financial data found. Please use Manual Entry or complete a Financial Modeler first.")
            return None
    else:
        input_data = manual_entry_inputs()
    
    return input_data


def pull_from_shared_state():
    """Pull data from shared financial state"""
    
    if not has_financial_data():
        return None
    
    core = get_core_financials()
    sync_status = get_sync_status()
    
    monthly_revenue = core.get("revenue", 0)
    monthly_expenses = core.get("expenses", 0)
    
    if monthly_revenue == 0 and monthly_expenses == 0:
        return None
    
    source_name = sync_status.get("source_module", "Unknown")
    if source_name == "financial_modeler_lite":
        st.success(f"✓ Data loaded from Financial Modeler Lite")
    elif source_name == "financial_modeler_pro":
        st.success(f"✓ Data loaded from Financial Modeler Pro")
    else:
        st.success(f"✓ Data loaded from shared financial state")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Monthly Revenue", f"${monthly_revenue:,.0f}")
        st.metric("Monthly Expenses", f"${monthly_expenses:,.0f}")
    
    with col2:
        net_monthly = monthly_revenue - monthly_expenses
        st.metric("Net Monthly Cash Flow", f"${net_monthly:,.0f}")
    
    st.divider()
    
    default_starting_cash = int(core.get("starting_cash", 50000)) if core.get("starting_cash", 0) > 0 else 50000
    starting_cash = st.number_input(
        "Starting Cash Balance ($)",
        min_value=0,
        value=default_starting_cash,
        step=5000,
        help="Initial cash on hand"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_months = core.get("projection_months", 12)
        default_index = [6, 12, 18, 24].index(default_months) if default_months in [6, 12, 18, 24] else 1
        projection_months = st.selectbox(
            "Projection Period (Months)",
            options=[6, 12, 18, 24],
            index=default_index
        )
        
        default_growth = core.get("growth_rate", 0.05) * 100
        revenue_growth = st.slider(
            "Revenue Growth Rate (%/month)",
            min_value=-5.0,
            max_value=15.0,
            value=float(default_growth),
            step=0.5
        ) / 100
    
    with col2:
        expense_growth = st.slider(
            "Expense Growth Rate (%/month)",
            min_value=-5.0,
            max_value=15.0,
            value=0.0,
            step=0.5
        ) / 100
        
        safety_buffer = st.slider(
            "Safety Buffer (multiplier)",
            min_value=1.0,
            max_value=2.0,
            value=1.25,
            step=0.05,
            help="Recommended LOC = Base need × Safety buffer"
        )
    
    stress_buffer = 1.5
    
    return {
        "starting_cash": starting_cash,
        "monthly_revenue": monthly_revenue,
        "monthly_expenses": monthly_expenses,
        "projection_months": projection_months,
        "revenue_growth": revenue_growth,
        "expense_growth": expense_growth,
        "safety_buffer": safety_buffer,
        "stress_buffer": stress_buffer
    }


def manual_entry_inputs():
    """Manual entry for cash flow inputs"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        starting_cash = st.number_input(
            "Starting Cash Balance ($)",
            min_value=0,
            value=50000,
            step=5000,
            help="Initial cash on hand"
        )
        
        monthly_revenue = st.number_input(
            "Monthly Revenue ($)",
            min_value=0,
            value=100000,
            step=5000,
            help="Average monthly revenue"
        )
        
        monthly_expenses = st.number_input(
            "Monthly Expenses ($)",
            min_value=0,
            value=85000,
            step=5000,
            help="Average monthly expenses"
        )
    
    with col2:
        projection_months = st.selectbox(
            "Projection Period (Months)",
            options=[6, 12, 18, 24],
            index=1
        )
        
        revenue_growth = st.slider(
            "Revenue Growth Rate (%/month)",
            min_value=-5.0,
            max_value=15.0,
            value=2.0,
            step=0.5,
            help="Expected monthly revenue growth"
        ) / 100
        
        expense_growth = st.slider(
            "Expense Growth Rate (%/month)",
            min_value=-5.0,
            max_value=15.0,
            value=0.0,
            step=0.5,
            help="Expected monthly expense growth"
        ) / 100
    
    safety_buffer = st.slider(
        "Safety Buffer (multiplier)",
        min_value=1.0,
        max_value=2.0,
        value=1.25,
        step=0.05,
        help="Recommended LOC = Base need × Safety buffer"
    )
    
    stress_buffer = 1.5
    
    net_monthly = monthly_revenue - monthly_expenses
    st.info(f"💡 Net Monthly Cash Flow: ${net_monthly:,.0f}")
    
    return {
        "starting_cash": starting_cash,
        "monthly_revenue": monthly_revenue,
        "monthly_expenses": monthly_expenses,
        "projection_months": projection_months,
        "revenue_growth": revenue_growth,
        "expense_growth": expense_growth,
        "safety_buffer": safety_buffer,
        "stress_buffer": stress_buffer
    }


def render_loc_recommendation(loc_data, trough_data):
    """Render LOC recommendation metrics"""
    
    st.markdown("### 💳 Line of Credit Recommendation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Recommended LOC",
            f"${loc_data['recommended_loc']:,.0f}",
            help="Recommended line of credit with safety buffer"
        )
    
    with col2:
        st.metric(
            "Lowest Cash Position",
            f"${trough_data['lowest_cash']:,.0f}",
            delta="Cash Trough" if trough_data['lowest_cash'] < 0 else "Positive"
        )
    
    with col3:
        st.metric(
            "Month of Trough",
            f"Month {trough_data['trough_month']}",
            help="When cash reaches lowest point"
        )
    
    with col4:
        st.metric(
            "Stress LOC",
            f"${loc_data['stress_loc']:,.0f}",
            help="LOC for worst-case scenario (50% buffer)"
        )
    
    if loc_data["needs_loc"]:
        st.warning(f"⚠️ **Working Capital Required**: This business needs a line of credit to cover cash flow gaps.")
    else:
        st.success(f"✅ **No LOC Required**: Business maintains positive cash balance throughout projection.")


def render_cash_flow_chart(cash_flow_data, trough_data, loc_data):
    """Render cash flow visualization"""
    
    st.markdown("### 📈 Cash Balance Over Time")
    
    months = cash_flow_data["months"]
    cash_balance = cash_flow_data["cash_balance"]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months,
        y=cash_balance,
        mode='lines+markers',
        name='Cash Balance',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="Zero Line",
        annotation_position="right"
    )
    
    trough_month = trough_data["trough_month"]
    trough_value = trough_data["lowest_cash"]
    
    fig.add_trace(go.Scatter(
        x=[trough_month],
        y=[trough_value],
        mode='markers',
        name='Cash Trough',
        marker=dict(
            size=15,
            color='red',
            symbol='x',
            line=dict(width=2, color='darkred')
        )
    ))
    
    if loc_data["recommended_loc"] > 0:
        fig.add_hline(
            y=-loc_data["recommended_loc"],
            line_dash="dot",
            line_color="orange",
            annotation_text=f"Recommended LOC: ${loc_data['recommended_loc']:,.0f}",
            annotation_position="left"
        )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Cash Balance ($)",
        hovermode='x unified',
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_loc_simulation(cash_flow_data, loc_data):
    """Render LOC usage simulation"""
    
    if loc_data["recommended_loc"] == 0:
        return
    
    st.markdown("### 💰 LOC Usage Simulation")
    
    simulation = simulate_loc_usage(
        cash_balance=cash_flow_data["cash_balance"],
        loc_amount=loc_data["recommended_loc"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Maximum LOC Used",
            f"${simulation['max_loc_used']:,.0f}"
        )
    
    with col2:
        st.metric(
            "Peak Utilization",
            f"{simulation['loc_utilization']:.1f}%"
        )
    
    fig = go.Figure()
    
    months = cash_flow_data["months"]
    
    fig.add_trace(go.Scatter(
        x=months,
        y=simulation["remaining_cash"],
        mode='lines',
        name='Cash with LOC',
        line=dict(color='green', width=2),
        fill='tozeroy'
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=simulation["loc_usage"],
        mode='lines',
        name='LOC Drawn',
        line=dict(color='orange', width=2, dash='dash')
    ))
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_insights_tab():
    """Render insights and recommendations"""
    
    if "loc_analysis" not in st.session_state or not st.session_state.loc_analysis:
        st.info("👈 Run the analysis in the **Analysis** tab to see insights")
        return
    
    analysis = st.session_state.loc_analysis
    
    st.markdown("### 💡 Cash Flow Insights")
    
    insights = generate_loc_insights(
        cash_flow_data=analysis["cash_flow"],
        trough_data=analysis["trough"],
        loc_data=analysis["loc"],
        monthly_revenue=analysis["inputs"]["monthly_revenue"]
    )
    
    for insight in insights:
        st.info(insight)
    
    st.divider()
    
    st.markdown("### 🎯 Recommendations")
    
    if analysis["loc"]["needs_loc"]:
        st.markdown(f"""
        **Immediate Actions:**
        - Establish a line of credit of at least **${analysis['loc']['recommended_loc']:,.0f}**
        - Negotiate favorable terms (interest rate, draw fees, covenants)
        - Set up before Month {analysis['trough']['trough_month']} when cash trough occurs
        
        **Strategic Considerations:**
        - Review timing of revenue collection (accelerate if possible)
        - Negotiate extended payment terms with vendors
        - Consider deposit or prepayment models to improve cash timing
        - Build cash reserves during positive months to reduce LOC dependency
        """)
    else:
        st.markdown("""
        **Cash Management Best Practices:**
        - Maintain current positive cash flow trajectory
        - Build cash reserves for unexpected expenses
        - Consider establishing a small LOC as safety net
        - Monitor cash flow monthly to catch early warning signs
        """)
    
    st.divider()
    
    st.markdown("### 🔗 Integration with Funding Strategy")
    
    if st.button("📋 Add LOC to Funding Plan", type="primary", use_container_width=True):
        if "funding_plan" not in st.session_state:
            st.session_state.funding_plan = {}
        
        st.session_state.funding_plan["loc"] = {
            "amount": analysis["loc"]["recommended_loc"],
            "purpose": "Working capital / Cash flow timing",
            "timing": f"Before Month {analysis['trough']['trough_month']}",
            "type": "Line of Credit"
        }
        
        st.success("✓ LOC added to funding plan! Access via Funding Engine module.")


def render_details_tab():
    """Render detailed monthly breakdown"""
    
    if "loc_analysis" not in st.session_state or not st.session_state.loc_analysis:
        st.info("👈 Run the analysis in the **Analysis** tab to see details")
        return
    
    analysis = st.session_state.loc_analysis
    cash_flow = analysis["cash_flow"]
    
    st.markdown("### 📋 Monthly Cash Flow Breakdown")
    
    import pandas as pd
    
    months = cash_flow["months"][1:]
    inflows = cash_flow["inflows"]
    outflows = cash_flow["outflows"]
    balances = cash_flow["cash_balance"][1:]
    
    net_flows = [inflows[i] - outflows[i] for i in range(len(inflows))]
    
    df = pd.DataFrame({
        "Month": months,
        "Cash Inflow": inflows,
        "Cash Outflow": outflows,
        "Net Cash Flow": net_flows,
        "Ending Balance": balances
    })
    
    df["Cash Inflow"] = df["Cash Inflow"].apply(lambda x: f"${x:,.0f}")
    df["Cash Outflow"] = df["Cash Outflow"].apply(lambda x: f"${x:,.0f}")
    df["Net Cash Flow"] = df["Net Cash Flow"].apply(lambda x: f"${x:,.0f}")
    df["Ending Balance"] = df["Ending Balance"].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.markdown("### 📊 Working Capital Metrics")
    
    wc_metrics = calculate_working_capital_metrics(
        cash_flow_data=cash_flow,
        monthly_revenue=analysis["inputs"]["monthly_revenue"],
        monthly_expenses=analysis["inputs"]["monthly_expenses"]
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Cash Balance", f"${wc_metrics['avg_cash']:,.0f}")
        st.metric("Maximum Cash", f"${wc_metrics['max_cash']:,.0f}")
    
    with col2:
        st.metric("Minimum Cash", f"${wc_metrics['min_cash']:,.0f}")
        st.metric("Cash Volatility", f"${wc_metrics['cash_volatility']:,.0f}")
    
    with col3:
        st.metric("Months of Runway", f"{wc_metrics['months_of_runway']:.1f}")
