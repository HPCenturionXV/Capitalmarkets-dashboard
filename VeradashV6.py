import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
import yfinance as yf
import requests
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

# --- Professional Configuration ---
st.set_page_config(
    page_title="Vera Capital Markets",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Professional Styling ---
st.markdown("""
<style>
    /* Professional Color Palette */
    :root {
        --primary-dark: #0a0e27;
        --secondary-dark: #1a1f3a;
        --accent-blue: #1e40af;
        --accent-cyan: #0891b2;
        --success-green: #059669;
        --danger-red: #dc2626;
        --warning-amber: #d97706;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --text-muted: #64748b;
        --border-color: #334155;
        --card-bg: #1e293b;
        --gradient-primary: linear-gradient(135deg, #1e40af, #0891b2);
        --gradient-success: linear-gradient(135deg, #059669, #10b981);
        --gradient-danger: linear-gradient(135deg, #dc2626, #ef4444);
        --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-medium: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-strong: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--primary-dark);
        color: var(--text-primary);
    }
    
    /* Professional Header */
    .institutional-header {
        background: var(--gradient-primary);
        padding: 2.5rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: var(--shadow-strong);
        position: relative;
        overflow: hidden;
    }
    
    .institutional-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .institutional-header h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
    }
    
    .institutional-header .subtitle {
        font-size: 1.25rem;
        margin: 0.75rem 0 0 0;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .institutional-header .tagline {
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.8;
        font-weight: 400;
    }
    
    /* Professional Cards */
    .institutional-card {
        background: var(--card-bg);
        padding: 1.75rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-soft);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .institutional-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .institutional-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        border-color: var(--accent-blue);
    }
    
    /* Market Status Indicator */
    .market-status {
        display: inline-flex;
        align-items: center;
        padding: 0.75rem 1.5rem;
        border-radius: 2rem;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: var(--shadow-soft);
    }
    
    .market-status.open {
        background: var(--gradient-success);
        color: white;
    }
    
    .market-status.closed {
        background: var(--gradient-danger);
        color: white;
    }
    
    .market-status::before {
        content: '●';
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Professional Metrics */
    .metric-professional {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .metric-professional:hover {
        border-color: var(--accent-blue);
        box-shadow: var(--shadow-soft);
    }
    
    .metric-professional .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-professional .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .metric-professional .metric-change {
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .metric-professional .metric-change.positive {
        color: var(--success-green);
    }
    
    .metric-professional .metric-change.negative {
        color: var(--danger-red);
    }
    
    /* Professional Sidebar */
    .professional-sidebar {
        background: linear-gradient(180deg, var(--secondary-dark), var(--primary-dark));
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
        border: 1px solid var(--border-color);
    }
    
    .professional-sidebar h3 {
        color: var(--text-primary);
        font-size: 1.125rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-soft);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-medium);
    }
    
    /* Professional Inputs */
    .stTextInput > div > div > input {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        color: var(--text-primary);
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-blue);
        box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
    }
    
    .stSelectbox > div > div {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
    }
    
    /* Performance Indicators */
    .performance-indicator {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .performance-indicator.positive {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success-green);
        border: 1px solid rgba(5, 150, 105, 0.2);
    }
    
    .performance-indicator.negative {
        background: rgba(220, 38, 38, 0.1);
        color: var(--danger-red);
        border: 1px solid rgba(220, 38, 38, 0.2);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--accent-blue);
        color: white;
        transform: translateY(-1px);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--gradient-primary);
        color: white;
        border-color: var(--accent-blue);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--secondary-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-blue);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-cyan);
    }
    
    /* Professional Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Loading States */
    .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(10, 14, 39, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Professional Helper Functions ---
def get_demo_market_data():
    """Return demo market data when API is unavailable"""
    return {
        'S&P 500': {
            'price': 4500.25,
            'change': 15.75,
            'change_pct': 0.35,
            'volume': 2500000000,
            'ticker': '^GSPC',
            'market_cap': 0,
            'sector': 'Index'
        },
        'Dow Jones': {
            'price': 34500.50,
            'change': -25.30,
            'change_pct': -0.07,
            'volume': 1800000000,
            'ticker': '^DJI',
            'market_cap': 0,
            'sector': 'Index'
        },
        'NASDAQ': {
            'price': 14250.75,
            'change': 45.20,
            'change_pct': 0.32,
            'volume': 3200000000,
            'ticker': '^IXIC',
            'market_cap': 0,
            'sector': 'Index'
        },
        'VIX': {
            'price': 18.25,
            'change': -1.50,
            'change_pct': -7.59,
            'volume': 50000000,
            'ticker': '^VIX',
            'market_cap': 0,
            'sector': 'Volatility'
        }
    }

@st.cache_data(ttl=600)  # 10 minute cache to reduce API calls
def fetch_institutional_data():
    """Fetch institutional-grade market data with rate limiting"""
    try:
        # Reduced indices to avoid rate limiting
        indices = {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI', 
            'NASDAQ': '^IXIC',
            'VIX': '^VIX'
        }
        
        data = {}
        for i, (name, ticker) in enumerate(indices.items()):
            try:
                # Add delay between requests to avoid rate limiting
                if i > 0:
                    time.sleep(0.5)
                
                stock = yf.Ticker(ticker)
                hist = stock.history(period="2d", interval="1d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100
                    
                    # Get additional metrics with error handling
                    try:
                        info = stock.info
                        volume = hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                    except:
                        info = {}
                        volume = 0
                    
                    data[name] = {
                        'price': current_price,
                        'change': change,
                        'change_pct': change_pct,
                        'volume': volume,
                        'ticker': ticker,
                        'market_cap': info.get('marketCap', 0),
                        'sector': info.get('sector', 'N/A')
                    }
            except Exception as e:
                st.warning(f"Could not fetch data for {name}: {str(e)}")
                continue
        return data
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")
        return {}

@st.cache_data(ttl=600)  # 10 minute cache
def fetch_institutional_movers():
    """Fetch institutional-grade market movers with rate limiting"""
    try:
        # Top institutional movers
        movers_data = {
            'gainers': [],
            'losers': []
        }
        
        # Reduced number of stocks to avoid rate limiting
        institutional_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM'
        ]
        
        for i, ticker in enumerate(institutional_stocks):
            try:
                # Add delay between requests to avoid rate limiting
                if i > 0:
                    time.sleep(0.5)
                
                stock = yf.Ticker(ticker)
                hist = stock.history(period="2d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100
                    
                    # Get info with error handling
                    try:
                        info = stock.info
                    except:
                        info = {}
                    
                    stock_data = {
                        'symbol': ticker,
                        'name': info.get('shortName', ticker),
                        'price': current_price,
                        'change': change,
                        'change_pct': change_pct,
                        'market_cap': info.get('marketCap', 0),
                        'sector': info.get('sector', 'N/A')
                    }
                    
                    if change_pct > 0:
                        movers_data['gainers'].append(stock_data)
                    else:
                        movers_data['losers'].append(stock_data)
            except Exception as e:
                st.warning(f"Could not fetch data for {ticker}: {str(e)}")
                continue
        
        # Sort by change percentage
        movers_data['gainers'].sort(key=lambda x: x['change_pct'], reverse=True)
        movers_data['losers'].sort(key=lambda x: x['change_pct'])
        
        return movers_data
    except Exception as e:
        st.error(f"Error fetching movers data: {str(e)}")
        return {'gainers': [], 'losers': []}

@st.cache_data(ttl=300)
def fetch_stock_analysis(ticker, period="1mo"):
    """Fetch comprehensive stock analysis with error handling"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            st.warning(f"No data available for {ticker}")
            return None, None, None
        
        # Get info with error handling
        try:
            info = stock.info
        except Exception as e:
            st.warning(f"Could not fetch company info for {ticker}: {str(e)}")
            info = {}
            
        # Calculate technical indicators
        hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
        hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
        hist['EMA_12'] = hist['Close'].ewm(span=12).mean()
        hist['EMA_26'] = hist['Close'].ewm(span=26).mean()
        hist['MACD'] = hist['EMA_12'] - hist['EMA_26']
        hist['MACD_Signal'] = hist['MACD'].ewm(span=9).mean()
        
        # RSI calculation
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        hist['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        hist['BB_Middle'] = hist['Close'].rolling(window=20).mean()
        bb_std = hist['Close'].rolling(window=20).std()
        hist['BB_Upper'] = hist['BB_Middle'] + (bb_std * 2)
        hist['BB_Lower'] = hist['BB_Middle'] - (bb_std * 2)
        
        return hist, info, {
            'current_price': hist['Close'].iloc[-1],
            'sma_20': hist['SMA_20'].iloc[-1] if not pd.isna(hist['SMA_20'].iloc[-1]) else 0,
            'sma_50': hist['SMA_50'].iloc[-1] if not pd.isna(hist['SMA_50'].iloc[-1]) else 0,
            'rsi': hist['RSI'].iloc[-1] if not pd.isna(hist['RSI'].iloc[-1]) else 50,
            'macd': hist['MACD'].iloc[-1] if not pd.isna(hist['MACD'].iloc[-1]) else 0,
            'bb_upper': hist['BB_Upper'].iloc[-1] if not pd.isna(hist['BB_Upper'].iloc[-1]) else 0,
            'bb_lower': hist['BB_Lower'].iloc[-1] if not pd.isna(hist['BB_Lower'].iloc[-1]) else 0
        }
    except Exception as e:
        st.error(f"Error fetching stock analysis for {ticker}: {str(e)}")
        return None, None, None

def create_institutional_chart(hist, ticker, indicators=None):
    """Create institutional-grade chart"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{ticker} Price Action', 'MACD', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Main price chart
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
        name='OHLC',
        increasing_line_color='#10b981',
        decreasing_line_color='#ef4444'
    ), row=1, col=1)
    
    # Moving averages
    if 'SMA_20' in hist.columns:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['SMA_20'],
            name='SMA 20', line=dict(color='#3b82f6', width=2)
        ), row=1, col=1)
    
    if 'SMA_50' in hist.columns:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['SMA_50'],
            name='SMA 50', line=dict(color='#8b5cf6', width=2)
        ), row=1, col=1)
    
    # Bollinger Bands
    if 'BB_Upper' in hist.columns:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['BB_Upper'],
            name='BB Upper', line=dict(color='#64748b', width=1, dash='dash'),
            showlegend=False
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['BB_Lower'],
            name='BB Lower', line=dict(color='#64748b', width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(100, 116, 139, 0.1)',
            showlegend=False
        ), row=1, col=1)
    
    # MACD
    if 'MACD' in hist.columns:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['MACD'],
            name='MACD', line=dict(color='#3b82f6', width=2)
        ), row=2, col=1)
        
        if 'MACD_Signal' in hist.columns:
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['MACD_Signal'],
                name='Signal', line=dict(color='#ef4444', width=2)
            ), row=2, col=1)
    
    # RSI
    if 'RSI' in hist.columns:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['RSI'],
            name='RSI', line=dict(color='#f59e0b', width=2)
        ), row=3, col=1)
        
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="#10b981", row=3, col=1)
    
    fig.update_layout(
        title=f'{ticker} Institutional Analysis',
        height=800,
        template='plotly_dark',
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

def create_market_overview_chart(market_data):
    """Create professional market overview chart"""
    if not market_data:
        return None
    
    fig = go.Figure()
    
    names = list(market_data.keys())
    changes = [data['change_pct'] for data in market_data.values()]
    prices = [data['price'] for data in market_data.values()]
    
    colors = ['#10b981' if change > 0 else '#ef4444' for change in changes]
    
    fig.add_trace(go.Bar(
        x=names,
        y=changes,
        marker_color=colors,
        text=[f"{change:.2f}%" for change in changes],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>' +
                     'Change: %{y:.2f}%<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title='Market Performance Overview',
        xaxis_title='Indices',
        yaxis_title='Percentage Change (%)',
        template='plotly_dark',
        height=500,
        showlegend=False
    )
    
    return fig

# --- Main Application ---
def main():
    # Professional Header with Enhanced Typography
    st.markdown("""
    <div class="institutional-header" style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif; 
            font-weight: 700; font-size: 3rem; letter-spacing: -0.02em; margin: 0; 
            background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;">
            VERA CAPITAL MARKETS
        </h1>
        <div class="subtitle" style="font-family: 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif; 
             font-weight: 500; font-size: 1.2rem; letter-spacing: 0.01em; margin: 0.5rem 0; 
             color: #94a3b8;">
            Institutional-Grade Financial Analytics Platform
        </div>
        <div class="tagline" style="font-family: 'SF Pro Text', sans-serif; 
             font-weight: 400; font-size: 1rem; letter-spacing: 0.02em; margin: 0.25rem 0; 
             color: #64748b;">
            Professional Trading & Investment Intelligence
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Market Status
    current_time = datetime.now()
    market_open = current_time.hour >= 9 and current_time.hour < 16 and current_time.weekday() < 5
    
    status_class = "open" if market_open else "closed"
    status_text = "Market Open" if market_open else "Market Closed"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="market-status {status_class}">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Trading Controls Bar
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); 
                padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem; 
                box-shadow: 0 8px 32px rgba(0,0,0,0.4); border: 1px solid rgba(59,130,246,0.2);">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3 style="color: #e0e6ed; font-family: 'SF Pro Text', sans-serif; font-size: 1.2rem; 
                       font-weight: 600; margin: 0;">Trading Controls</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Professional Controls Row
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        st.markdown("**Stock Symbol**")
        ticker = st.text_input(
            "Enter stock symbol",
            value=st.session_state.get('ticker', 'AAPL'),
            help="Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)",
            key="ticker_control"
        ).upper()
    
    with col2:
        st.markdown("**Time Period**")
        period = st.selectbox(
            "Select time period",
            options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
            index=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max"].index(st.session_state.get('period', '1y')),
            help="Select the time period for analysis",
            key="period_control"
        )
    
    with col3:
        st.markdown("**Technical Indicators**")
        indicators = st.multiselect(
            "Select indicators",
            options=['SMA_20', 'SMA_50', 'SMA_200', 'EMA_12', 'EMA_26', 'RSI', 'MACD', 'BB'],
            default=st.session_state.get('indicators', ['SMA_20', 'SMA_50', 'RSI', 'MACD']),
            help="Choose technical indicators to display",
            key="indicators_control"
        )
    
    with col4:
        st.markdown("**Actions**")
        if st.button("Refresh Data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    
    # Update session state with current values
    st.session_state.ticker = ticker
    st.session_state.period = period
    st.session_state.indicators = indicators
    
    # Main Content with Tabs
    tab1, tab2, tab3 = st.tabs(["Market Overview", "Market Movers", "Stock Analysis"])
    
    with tab1:
        st.markdown('<div class="section-title">Market Overview</div>', unsafe_allow_html=True)
        
        # Fetch market data
        market_data = fetch_institutional_data()
        
        # If no data available, use demo data
        if not market_data:
            st.warning("⚠️ API rate limit reached. Showing demo data. Please wait a few minutes and refresh.")
            market_data = get_demo_market_data()
        
        if market_data:
            # Market metrics cards in a grid
            cols = st.columns(4)  # 4 columns for better layout
            for i, (name, data) in enumerate(market_data.items()):
                col_idx = i % 4
                with cols[col_idx]:
                    change_class = "positive" if data['change_pct'] > 0 else "negative"
                    st.markdown(f"""
                    <div class="metric-professional">
                        <div class="metric-label">{name}</div>
                        <div class="metric-value">${data['price']:.2f}</div>
                        <div class="metric-change {change_class}">
                            {data['change']:+.2f} ({data['change_pct']:+.2f}%)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Market overview chart
            st.markdown("### Market Performance Chart")
            overview_fig = create_market_overview_chart(market_data)
            if overview_fig:
                st.plotly_chart(overview_fig, use_container_width=True)
        else:
            st.error("Unable to fetch market data. Please try again later.")
    
    with tab2:
        st.markdown('<div class="section-title">Market Movers</div>', unsafe_allow_html=True)
        
        movers_data = fetch_institutional_movers()
        
        col_gainers, col_losers = st.columns(2)
        
        with col_gainers:
            st.markdown("### Top Gainers")
            if movers_data['gainers']:
                for stock in movers_data['gainers'][:8]:  # Show top 8
                    change_class = "positive" if stock['change_pct'] > 0 else "negative"
                    st.markdown(f"""
                    <div class="institutional-card" style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 1.1rem;">{stock['symbol']}</strong><br>
                                <small style="color: var(--text-secondary);">{stock['name'][:35]}...</small><br>
                                <small style="color: var(--text-muted);">{stock['sector']}</small>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.25rem;">${stock['price']:.2f}</div>
                                <span class="performance-indicator {change_class}">
                                    +{stock['change_pct']:.2f}%
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No gainers data available")
        
        with col_losers:
            st.markdown("### Top Losers")
            if movers_data['losers']:
                for stock in movers_data['losers'][:8]:  # Show top 8
                    change_class = "positive" if stock['change_pct'] > 0 else "negative"
                    st.markdown(f"""
                    <div class="institutional-card" style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <strong style="font-size: 1.1rem;">{stock['symbol']}</strong><br>
                                <small style="color: var(--text-secondary);">{stock['name'][:35]}...</small><br>
                                <small style="color: var(--text-muted);">{stock['sector']}</small>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.25rem;">${stock['price']:.2f}</div>
                                <span class="performance-indicator {change_class}">
                                    {stock['change_pct']:.2f}%
                                </span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No losers data available")
    
    with tab3:
        st.markdown('<div class="section-title">Stock Analysis</div>', unsafe_allow_html=True)
        
        if ticker:
            hist, info, technicals = fetch_stock_analysis(ticker, period)
            
            if hist is not None and info is not None:
                # Company Header with Description
                company_name = info.get('longName', info.get('shortName', ticker))
                company_sector = info.get('sector', 'N/A')
                company_industry = info.get('industry', 'N/A')
                company_summary = info.get('longBusinessSummary', 'No description available.')
                
                st.markdown(f"""
                <div class="institutional-card" style="margin-bottom: 2rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                        <div>
                            <h2 style="margin: 0 0 0.5rem 0; color: var(--text-primary); font-size: 2rem;">{company_name}</h2>
                            <div style="color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 0.25rem;">
                                <strong>{ticker}</strong> • {company_sector} • {company_industry}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.25rem;">
                                ${technicals['current_price']:.2f}
                            </div>
                            <div class="metric-change {'positive' if (len(hist) > 1 and technicals['current_price'] > hist['Close'].iloc[-2]) else 'negative'}" style="font-size: 1.1rem;">
                                {technicals['current_price'] - hist['Close'].iloc[-2] if len(hist) > 1 else 0:+.2f} ({(technicals['current_price'] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100 if len(hist) > 1 else 0:+.2f}%)
                            </div>
                        </div>
                    </div>
                    <div style="color: var(--text-secondary); line-height: 1.6; font-size: 0.95rem;">
                        {company_summary[:300]}{'...' if len(company_summary) > 300 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Enhanced Stock metrics in multiple rows
                st.markdown("### Key Financial Metrics")
                
                # First row - Core metrics
                col1, col2, col3, col4 = st.columns(4)
                
                current_price = technicals['current_price']
                prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100
                
                with col1:
                    st.metric("Market Cap", f"${info.get('marketCap', 0):,}" if info.get('marketCap') else 'N/A')
                
                with col2:
                    st.metric("PE Ratio", f"{info.get('trailingPE', 0):.2f}" if info.get('trailingPE') else 'N/A')
                
                with col3:
                    st.metric("Volume", f"{info.get('volume', 0):,}" if info.get('volume') else 'N/A')
                
                with col4:
                    st.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 0):.2f}" if info.get('fiftyTwoWeekHigh') else 'N/A')
                
                # Second row - Additional metrics
                col5, col6, col7, col8 = st.columns(4)
                
                with col5:
                    st.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 0):.2f}" if info.get('fiftyTwoWeekLow') else 'N/A')
                
                with col6:
                    st.metric("Beta", f"{info.get('beta', 0):.2f}" if info.get('beta') else 'N/A')
                
                with col7:
                    st.metric("Dividend Yield", f"{info.get('dividendYield', 0):.2%}" if info.get('dividendYield') else 'N/A')
                
                with col8:
                    st.metric("EPS (TTM)", f"${info.get('trailingEps', 0):.2f}" if info.get('trailingEps') else 'N/A')
                
                # Third row - Advanced metrics
                col9, col10, col11, col12 = st.columns(4)
                
                with col9:
                    st.metric("Forward PE", f"{info.get('forwardPE', 0):.2f}" if info.get('forwardPE') else 'N/A')
                
                with col10:
                    st.metric("Price to Book", f"{info.get('priceToBook', 0):.2f}" if info.get('priceToBook') else 'N/A')
                
                with col11:
                    st.metric("Return on Equity", f"{info.get('returnOnEquity', 0):.2%}" if info.get('returnOnEquity') else 'N/A')
                
                with col12:
                    st.metric("Profit Margin", f"{info.get('profitMargins', 0):.2%}" if info.get('profitMargins') else 'N/A')
                
                # Fourth row - Additional financial data
                col13, col14, col15, col16 = st.columns(4)
                
                with col13:
                    st.metric("Enterprise Value", f"${info.get('enterpriseValue', 0):,}" if info.get('enterpriseValue') else 'N/A')
                
                with col14:
                    st.metric("Book Value", f"${info.get('bookValue', 0):.2f}" if info.get('bookValue') else 'N/A')
                
                with col15:
                    st.metric("Operating Margin", f"{info.get('operatingMargins', 0):.2%}" if info.get('operatingMargins') else 'N/A')
                
                with col16:
                    st.metric("Debt to Equity", f"{info.get('debtToEquity', 0):.2f}" if info.get('debtToEquity') else 'N/A')
                
                # Chart type selection
                col_chart1, col_chart2 = st.columns([1, 3])
                
                with col_chart1:
                    chart_type = st.radio(
                        "Chart Type:",
                        options=["Normal Line", "Technical Analysis"],
                        index=1,
                        help="Choose between simple line chart or advanced technical analysis"
                    )
                
                with col_chart2:
                    st.markdown("### Price Chart")
                
                # Technical indicators
                if technicals and chart_type == "Technical Analysis":
                    st.markdown("### Technical Indicators")
                    
                    col_tech1, col_tech2, col_tech3, col_tech4 = st.columns(4)
                    
                    with col_tech1:
                        st.metric("RSI", f"{technicals['rsi']:.1f}")
                    with col_tech2:
                        st.metric("SMA 20", f"${technicals['sma_20']:.2f}")
                    with col_tech3:
                        st.metric("MACD", f"{technicals['macd']:.3f}")
                    with col_tech4:
                        st.metric("SMA 50", f"${technicals['sma_50']:.2f}")
                
                # Display appropriate chart
                if chart_type == "Normal Line":
                    # Simple line chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=hist.index,
                        y=hist['Close'],
                        mode='lines',
                        name='Close Price',
                        line=dict(color='#3b82f6', width=3)
                    ))
                    
                    fig.update_layout(
                        title=f'{ticker} Price Chart',
                        xaxis_title='Date',
                        yaxis_title='Price (USD)',
                        template='plotly_dark',
                        height=500,
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # Technical analysis chart
                    chart_fig = create_institutional_chart(hist, ticker, indicators)
                    st.plotly_chart(chart_fig, use_container_width=True)
                
                # Performance Analysis Section
                st.markdown("### Performance Analysis")
                
                # Calculate performance metrics
                if len(hist) > 1:
                    # Performance over different periods
                    performance_data = {
                        '1 Day': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100) if len(hist) > 1 else 0,
                        '1 Week': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-7]) / hist['Close'].iloc[-7] * 100) if len(hist) > 7 else 0,
                        '1 Month': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-30]) / hist['Close'].iloc[-30] * 100) if len(hist) > 30 else 0,
                        '3 Months': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-90]) / hist['Close'].iloc[-90] * 100) if len(hist) > 90 else 0,
                        '6 Months': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-180]) / hist['Close'].iloc[-180] * 100) if len(hist) > 180 else 0,
                        '1 Year': ((hist['Close'].iloc[-1] - hist['Close'].iloc[-365]) / hist['Close'].iloc[-365] * 100) if len(hist) > 365 else 0
                    }
                    
                    # Display performance metrics
                    perf_col1, perf_col2, perf_col3, perf_col4, perf_col5, perf_col6 = st.columns(6)
                    
                    with perf_col1:
                        st.metric("1D", f"{performance_data['1 Day']:+.2f}%")
                    with perf_col2:
                        st.metric("1W", f"{performance_data['1 Week']:+.2f}%")
                    with perf_col3:
                        st.metric("1M", f"{performance_data['1 Month']:+.2f}%")
                    with perf_col4:
                        st.metric("3M", f"{performance_data['3 Months']:+.2f}%")
                    with perf_col5:
                        st.metric("6M", f"{performance_data['6 Months']:+.2f}%")
                    with perf_col6:
                        st.metric("1Y", f"{performance_data['1 Year']:+.2f}%")
                
                # Additional Financial Data
                st.markdown("### Additional Financial Data")
                
                col_fin1, col_fin2, col_fin3, col_fin4 = st.columns(4)
                
                with col_fin1:
                    st.metric("Shares Outstanding", f"{info.get('sharesOutstanding', 0):,}" if info.get('sharesOutstanding') else 'N/A')
                
                with col_fin2:
                    st.metric("Float Shares", f"{info.get('floatShares', 0):,}" if info.get('floatShares') else 'N/A')
                
                with col_fin3:
                    st.metric("Short Ratio", f"{info.get('shortRatio', 0):.2f}" if info.get('shortRatio') else 'N/A')
                
                with col_fin4:
                    st.metric("Short Interest", f"{info.get('shortInterest', 0):,}" if info.get('shortInterest') else 'N/A')
                
                # Dividend Information
                st.markdown("### Dividend Information")
                
                col_div1, col_div2, col_div3, col_div4 = st.columns(4)
                
                with col_div1:
                    st.metric("Dividend Rate", f"${info.get('dividendRate', 0):.2f}" if info.get('dividendRate') else 'N/A')
                
                with col_div2:
                    st.metric("Dividend Date", f"{info.get('dividendDate', 'N/A')}" if info.get('dividendDate') else 'N/A')
                
                with col_div3:
                    st.metric("Ex-Dividend Date", f"{info.get('exDividendDate', 'N/A')}" if info.get('exDividendDate') else 'N/A')
                
                with col_div4:
                    st.metric("Payout Ratio", f"{info.get('payoutRatio', 0):.2%}" if info.get('payoutRatio') else 'N/A')
                
                # Analyst Information
                st.markdown("### Analyst Information")
                
                col_analyst1, col_analyst2, col_analyst3, col_analyst4 = st.columns(4)
                
                with col_analyst1:
                    st.metric("Target Price", f"${info.get('targetMeanPrice', 0):.2f}" if info.get('targetMeanPrice') else 'N/A')
                
                with col_analyst2:
                    st.metric("Recommendation", f"{info.get('recommendationKey', 'N/A')}" if info.get('recommendationKey') else 'N/A')
                
                with col_analyst3:
                    st.metric("Number of Analysts", f"{info.get('numberOfAnalystOpinions', 0)}" if info.get('numberOfAnalystOpinions') else 'N/A')
                
                with col_analyst4:
                    st.metric("Price Target High", f"${info.get('targetHighPrice', 0):.2f}" if info.get('targetHighPrice') else 'N/A')
                
                # Trading Information
                st.markdown("### Trading Information")
                
                col_trade1, col_trade2, col_trade3, col_trade4 = st.columns(4)
                
                with col_trade1:
                    st.metric("Day High", f"${info.get('dayHigh', 0):.2f}" if info.get('dayHigh') else 'N/A')
                
                with col_trade2:
                    st.metric("Day Low", f"${info.get('dayLow', 0):.2f}" if info.get('dayLow') else 'N/A')
                
                with col_trade3:
                    st.metric("Previous Close", f"${info.get('previousClose', 0):.2f}" if info.get('previousClose') else 'N/A')
                
                with col_trade4:
                    st.metric("Open", f"${info.get('open', 0):.2f}" if info.get('open') else 'N/A')
                
                # Additional company information
                if info and info.get('longBusinessSummary'):
                    with st.expander("Full Company Information"):
                        st.write(info['longBusinessSummary'])
                
                # Key Statistics
                with st.expander("Key Statistics"):
                    key_stats = {
                        'Sector': info.get('sector', 'N/A'),
                        'Industry': info.get('industry', 'N/A'),
                        'Full Time Employees': f"{info.get('fullTimeEmployees', 0):,}" if info.get('fullTimeEmployees') else 'N/A',
                        'Website': info.get('website', 'N/A'),
                        'City': info.get('city', 'N/A'),
                        'State': info.get('state', 'N/A'),
                        'Country': info.get('country', 'N/A'),
                        'Currency': info.get('currency', 'N/A'),
                        'Exchange': info.get('exchange', 'N/A'),
                        'Quote Type': info.get('quoteType', 'N/A')
                    }
                    
                    for key, value in key_stats.items():
                        st.write(f"**{key}:** {value}")
            else:
                st.error(f"Could not fetch data for {ticker}")
        else:
            st.info("Please enter a stock symbol in the sidebar to begin analysis")
    
    # Professional Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
        <p><strong>💼 Vera Capital Markets</strong> - Institutional-Grade Financial Analytics</p>
        <p>Professional Trading Intelligence • Real-time Market Data • Advanced Analytics</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
