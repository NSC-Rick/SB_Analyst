"""
North Star Unified Shell - UI Design System
Global styles, typography, and component patterns
"""
import streamlit as st


def apply_global_styles():
    """
    Apply global CSS design system across the platform
    Creates consistent typography, spacing, and component styling
    """
    st.markdown("""
    <style>
    
    /* ===== GLOBAL TYPOGRAPHY ===== */
    html, body, [class*="css"]  {
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
        line-height: 1.5;
    }
    
    h1 { 
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #1a1a1a;
    }
    
    h2 { 
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #2a2a2a;
    }
    
    h3 { 
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
        color: #333333;
    }
    
    h4 { 
        font-size: 1.0rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #444444;
    }
    
    p {
        margin-bottom: 0.8rem;
        color: #555555;
    }
    
    /* ===== CONTENT WIDTH & SPACING ===== */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }
    
    /* ===== CARD SYSTEM ===== */
    .ns-card {
        background: #ffffff;
        border: 1px solid #e6e9ef;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease;
    }
    
    .ns-card:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    
    .ns-card-compact {
        background: #ffffff;
        border: 1px solid #e6e9ef;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    
    /* ===== HEADER BAND (Command Strip) ===== */
    .ns-header {
        background: linear-gradient(135deg, #f7f9fb 0%, #f0f3f7 100%);
        border: 1px solid #e1e5ea;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    .ns-header h4 {
        margin-bottom: 0.2rem;
        font-size: 0.9rem;
        color: #555;
    }
    
    /* ===== SECTION SPACING ===== */
    .ns-section {
        margin-top: 12px;
        margin-bottom: 24px;
    }
    
    .ns-section-tight {
        margin-top: 8px;
        margin-bottom: 16px;
    }
    
    /* ===== KPI METRICS ===== */
    .ns-metric {
        font-size: 0.9rem;
        font-weight: 500;
        color: #333;
    }
    
    .ns-metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        line-height: 1.2;
    }
    
    .ns-metric-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== BUTTON CLEANUP ===== */
    .stButton > button {
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* ===== ALERT TIGHTENING ===== */
    .stAlert {
        padding: 10px 12px !important;
        font-size: 0.85rem;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    
    /* ===== INPUT CLEANUP ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        font-size: 0.9rem;
        border-radius: 6px;
    }
    
    /* ===== DIVIDER STYLING ===== */
    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: none;
        border-top: 1px solid #e6e9ef;
    }
    
    /* ===== SIDEBAR REFINEMENT ===== */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    .css-1d391kg .stButton > button {
        font-size: 0.85rem;
    }
    
    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 8px;
    }
    
    /* ===== DATAFRAME STYLING ===== */
    .dataframe {
        font-size: 0.85rem;
        border-radius: 8px;
    }
    
    /* ===== CAPTION STYLING ===== */
    .stCaption {
        font-size: 0.8rem;
        color: #666;
        line-height: 1.4;
    }
    
    /* ===== MARKDOWN SPACING ===== */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* ===== COLUMN SPACING ===== */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* ===== SUCCESS/WARNING/ERROR REFINEMENT ===== */
    .stSuccess {
        background-color: #f0f9f4;
        border-left: 4px solid #10b981;
    }
    
    .stWarning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
    }
    
    .stError {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
    }
    
    .stInfo {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
    }
    
    /* ===== METRIC CONTAINER ===== */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #666;
    }
    
    /* ===== TABS STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 0.9rem;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px 6px 0 0;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div > div {
        border-radius: 10px;
    }
    
    /* ===== RESPONSIVE ADJUSTMENTS ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .ns-card {
            padding: 12px 14px;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)


def render_header_band(title, status=None, alert=None, stats=None):
    """
    Render a header command strip with status, alerts, and quick stats
    
    Args:
        title: Main title text
        status: Status message (optional)
        alert: Alert message (optional)
        stats: Quick stats text (optional)
    """
    st.markdown('<div class="ns-header">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    
    with cols[0]:
        st.markdown(f"#### {title}")
        if status:
            st.success(status)
    
    with cols[1]:
        if alert:
            st.markdown("#### 🔔 Alerts")
            st.info(alert)
    
    with cols[2]:
        if stats:
            st.markdown("#### 📈 Quick Stats")
            st.write(stats)
    
    st.markdown('</div>', unsafe_allow_html=True)


def card_start():
    """Start a card section"""
    st.markdown('<div class="ns-card">', unsafe_allow_html=True)


def card_end():
    """End a card section"""
    st.markdown('</div>', unsafe_allow_html=True)


def card_compact_start():
    """Start a compact card section"""
    st.markdown('<div class="ns-card-compact">', unsafe_allow_html=True)


def card_compact_end():
    """End a compact card section"""
    st.markdown('</div>', unsafe_allow_html=True)


def section_start():
    """Start a section group"""
    st.markdown('<div class="ns-section">', unsafe_allow_html=True)


def section_end():
    """End a section group"""
    st.markdown('</div>', unsafe_allow_html=True)


def render_metric_card(label, value, delta=None, help_text=None):
    """
    Render a styled metric card
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change indicator (optional)
        help_text: Help text (optional)
    """
    card_start()
    if delta:
        st.metric(label=label, value=value, delta=delta, help=help_text)
    else:
        st.metric(label=label, value=value, help=help_text)
    card_end()


def render_kpi_row(metrics):
    """
    Render a row of KPI metrics
    
    Args:
        metrics: List of dicts with 'label', 'value', 'delta' (optional)
    """
    cols = st.columns(len(metrics))
    
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            if 'delta' in metric:
                st.metric(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric.get('delta')
                )
            else:
                st.metric(
                    label=metric['label'],
                    value=metric['value']
                )
