"""
Valuation Distribution Chart Visualization
Plotly-based probabilistic valuation curve with confidence intervals
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def create_distribution_chart(stats, confidence_intervals, methods, x_values, y_values):
    """
    Create probabilistic distribution curve chart with confidence intervals
    
    Args:
        stats: Distribution statistics (mean, std_dev, etc.)
        confidence_intervals: CI data (68%, 95%)
        methods: Dict of individual method values
        x_values: X-axis values for curve
        y_values: Y-axis values for curve (probability density)
    
    Returns:
        plotly.graph_objects.Figure: Distribution chart
    """
    fig = go.Figure()
    
    mean = stats["mean"]
    ci_68 = confidence_intervals["ci_68"]
    ci_95 = confidence_intervals["ci_95"]
    
    # Add 95% confidence interval (outer shaded area)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        fill='tozeroy',
        fillcolor='rgba(99, 110, 250, 0.1)',
        line=dict(width=0),
        showlegend=True,
        name='95% Confidence',
        hovertemplate='<b>95% Confidence Interval</b><br>Value: $%{x:,.0f}<extra></extra>',
    ))
    
    # Add 68% confidence interval (inner shaded area)
    mask_68 = (x_values >= ci_68["low"]) & (x_values <= ci_68["high"])
    x_68 = x_values[mask_68]
    y_68 = y_values[mask_68]
    
    fig.add_trace(go.Scatter(
        x=x_68,
        y=y_68,
        fill='tozeroy',
        fillcolor='rgba(99, 110, 250, 0.3)',
        line=dict(width=0),
        showlegend=True,
        name='68% Confidence',
        hovertemplate='<b>68% Confidence Interval</b><br>Value: $%{x:,.0f}<extra></extra>',
    ))
    
    # Add main distribution curve
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        line=dict(color='rgb(99, 110, 250)', width=3),
        name='Distribution Curve',
        showlegend=True,
        hovertemplate='<b>Probability Density</b><br>Value: $%{x:,.0f}<br>Density: %{y:.6f}<extra></extra>',
    ))
    
    # Add mean line
    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="rgb(239, 68, 68)",
        annotation_text=f"Mean: ${mean:,.0f}",
        annotation_position="top",
    )
    
    # Add individual method markers
    method_colors = {
        "revenue_method": "rgb(34, 197, 94)",
        "earnings_method": "rgb(251, 146, 60)",
        "asset_method": "rgb(168, 85, 247)",
    }
    
    method_names = {
        "revenue_method": "Revenue Multiple",
        "earnings_method": "Earnings Multiple",
        "asset_method": "Asset-Based",
    }
    
    max_y = max(y_values)
    
    for i, (method_key, value) in enumerate(methods.items()):
        color = method_colors.get(method_key, "rgb(156, 163, 175)")
        name = method_names.get(method_key, method_key)
        
        # Add marker at bottom
        fig.add_trace(go.Scatter(
            x=[value],
            y=[0],
            mode='markers',
            marker=dict(
                size=15,
                color=color,
                symbol='diamond',
                line=dict(color='white', width=2),
            ),
            name=name,
            showlegend=True,
            hovertemplate=f'<b>{name}</b><br>Value: $%{{x:,.0f}}<extra></extra>',
        ))
        
        # Add vertical line for method
        fig.add_vline(
            x=value,
            line_dash="dot",
            line_color=color,
            line_width=1,
            opacity=0.5,
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Valuation Distribution Curve",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'rgb(255, 255, 255)'},
        },
        xaxis_title="Business Valuation ($)",
        yaxis_title="Probability Density",
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgb(255, 255, 255)'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='$,.0f',
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        height=500,
    )
    
    return fig


def create_confidence_summary_chart(confidence_intervals, mean):
    """
    Create horizontal bar chart showing confidence intervals
    
    Args:
        confidence_intervals: CI data
        mean: Mean valuation
    
    Returns:
        plotly.graph_objects.Figure: Confidence summary chart
    """
    ci_68 = confidence_intervals["ci_68"]
    ci_95 = confidence_intervals["ci_95"]
    
    fig = go.Figure()
    
    # 95% interval
    fig.add_trace(go.Bar(
        x=[ci_95["range"]],
        y=["95% Confidence"],
        orientation='h',
        marker=dict(color='rgba(99, 110, 250, 0.3)'),
        text=[f"${ci_95['low']:,.0f} - ${ci_95['high']:,.0f}"],
        textposition='inside',
        hovertemplate='<b>95% Confidence</b><br>Range: $%{text}<extra></extra>',
    ))
    
    # 68% interval
    fig.add_trace(go.Bar(
        x=[ci_68["range"]],
        y=["68% Confidence"],
        orientation='h',
        marker=dict(color='rgba(99, 110, 250, 0.6)'),
        text=[f"${ci_68['low']:,.0f} - ${ci_68['high']:,.0f}"],
        textposition='inside',
        hovertemplate='<b>68% Confidence</b><br>Range: $%{text}<extra></extra>',
    ))
    
    # Mean marker
    fig.add_vline(
        x=mean,
        line_dash="dash",
        line_color="rgb(239, 68, 68)",
        line_width=2,
    )
    
    fig.update_layout(
        title="Confidence Intervals",
        xaxis_title="Valuation Range ($)",
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgb(255, 255, 255)'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='$,.0f',
        ),
        height=200,
    )
    
    return fig


def create_method_comparison_chart(methods):
    """
    Create bar chart comparing individual method values
    
    Args:
        methods: Dict of method values
    
    Returns:
        plotly.graph_objects.Figure: Method comparison chart
    """
    method_names = {
        "revenue_method": "Revenue Multiple",
        "earnings_method": "Earnings Multiple",
        "asset_method": "Asset-Based",
    }
    
    method_colors = {
        "revenue_method": "rgb(34, 197, 94)",
        "earnings_method": "rgb(251, 146, 60)",
        "asset_method": "rgb(168, 85, 247)",
    }
    
    names = [method_names.get(k, k) for k in methods.keys()]
    values = list(methods.values())
    colors = [method_colors.get(k, "rgb(156, 163, 175)") for k in methods.keys()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=names,
        y=values,
        marker=dict(color=colors),
        text=[f"${v:,.0f}" for v in values],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Value: $%{y:,.0f}<extra></extra>',
    ))
    
    # Add mean line
    mean = np.mean(values)
    fig.add_hline(
        y=mean,
        line_dash="dash",
        line_color="rgb(239, 68, 68)",
        annotation_text=f"Mean: ${mean:,.0f}",
        annotation_position="right",
    )
    
    fig.update_layout(
        title="Valuation Method Comparison",
        xaxis_title="Method",
        yaxis_title="Valuation ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgb(255, 255, 255)'),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            tickformat='$,.0f',
        ),
        height=300,
    )
    
    return fig
