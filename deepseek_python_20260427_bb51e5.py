import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Quantum Finance Analytics | Stock Performance",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para look futurista y formal
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0f142e 100%);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px;
    }
    
    /* Metric cards */
    .stMetric {
        background: rgba(16, 20, 46, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .stMetric label {
        color: #8892b0 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dataframes */
    .dataframe {
        background: rgba(16, 20, 46, 0.6);
        color: #ccd6f6;
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 8px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(10, 14, 39, 0.95);
        border-right: 1px solid rgba(0, 212, 255, 0.3);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #00d4ff 0%, #0066ff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
    }
    
    /* Select boxes */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(16, 20, 46, 0.8);
        border-color: rgba(0, 212, 255, 0.5);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(16, 20, 46, 0.5);
        border-radius: 8px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #8892b0;
        font-family: monospace;
        font-size: 16px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00d4ff;
        border-bottom: 2px solid #00d4ff;
    }
    
    /* Info boxes */
    .stAlert {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<h1 style='text-align: center; margin-bottom: 0;'>
    ⚡ QUANTUM FINANCE ANALYTICS ⚡
</h1>
<p style='text-align: center; color: #667; margin-top: 0; font-size: 14px;'>
    Advanced Stock Performance Intelligence System
</p>
<hr style='border: 1px solid rgba(0,212,255,0.3); margin-bottom: 30px;'>
""", unsafe_allow_html=True)

# Sidebar - Configuración
with st.sidebar:
    st.markdown("### 🎛️ SYSTEM CONTROLS")
    
    # Input para símbolo de acción
    ticker = st.text_input(
        "ASSET SYMBOL",
        value="AAPL",
        help="Enter stock symbol (e.g., AAPL, MSFT, GOOGL, TSLA)"
    ).upper()
    
    # Selección de período
    period = st.selectbox(
        "TIMEFRAME",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3,
        format_func=lambda x: {
            "1mo": "1 Month", "3mo": "3 Months", "6mo": "6 Months",
            "1y": "1 Year", "2y": "2 Years", "5y": "5 Years"
        }[x]
    )
    
    st.markdown("---")
    st.markdown("### 📊 METRICS CONFIG")
    
    # Comparación con benchmark
    benchmark = st.selectbox(
        "BENCHMARK",
        options=["^GSPC", "^IXIC", "^DJI", "None"],
        format_func=lambda x: {
            "^GSPC": "S&P 500", "^IXIC": "NASDAQ", "^DJI": "Dow Jones", "None": "No Benchmark"
        }[x]
    )
    
    st.markdown("---")
    st.markdown("### 📈 TECHNICAL INDICATORS")
    
    show_ma = st.checkbox("Moving Averages", value=True)
    show_rsi = st.checkbox("RSI Indicator", value=False)
    
    st.markdown("---")
    st.markdown("""
    <p style='font-size: 11px; text-align: center; color: #667;'>
        ⚡ Powered by Yahoo Finance<br>
        📡 Real-time data processing
    </p>
    """, unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data(ttl=3600)
def load_data(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        # Información de la empresa
        info = stock.info
        
        return data, info
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# Cargar datos
if ticker:
    with st.spinner("🔄 Processing quantum data streams..."):
        data, info = load_data(ticker, period)
        
    if data is not None and not data.empty:
        
        # Métricas principales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        current_price = data['Close'].iloc[-1]
        price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
        price_change_pct = (price_change / data['Close'].iloc[-2]) * 100
        volume = data['Volume'].iloc[-1]
        avg_volume = data['Volume'].mean()
        
        # Calcular máximos y mínimos
        max_price = data['High'].max()
        min_price = data['Low'].min()
        
        with col1:
            st.metric(
                label="🔮 CURRENT PRICE",
                value=f"${current_price:.2f}",
                delta=f"{price_change_pct:.2f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                label="📊 VOLUME",
                value=f"{volume:,}",
                delta=f"{((volume/avg_volume)-1)*100:.1f}% vs Avg",
                delta_color="off"
            )
        
        with col3:
            st.metric(
                label="📈 PERIOD HIGH",
                value=f"${max_price:.2f}"
            )
        
        with col4:
            st.metric(
                label="📉 PERIOD LOW",
                value=f"${min_price:.2f}"
            )
        
        with col5:
            try:
                market_cap = info.get('marketCap', 0)
                if market_cap > 0:
                    st.metric(
                        label="🏦 MARKET CAP",
                        value=f"${market_cap/1e9:.2f}B"
                    )
                else:
                    st.metric(label="🏦 MARKET CAP", value="N/A")
            except:
                st.metric(label="🏦 MARKET CAP", value="N/A")
        
        st.markdown("---")
        
        # Gráfico de precios principal
        st.markdown("### 📈 PRICE DYNAMICS")
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price Action',
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff3366'
        ))
        
        # Moving Averages
        if show_ma:
            ma20 = data['Close'].rolling(window=20).mean()
            ma50 = data['Close'].rolling(window=50).mean()
            
            fig.add_trace(go.Scatter(
                x=data.index, y=ma20,
                name='MA 20',
                line=dict(color='#00d4ff', width=1.5, dash='dash')
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index, y=ma50,
                name='MA 50',
                line=dict(color='#ffa500', width=1.5, dash='dash')
            ))
        
        fig.update_layout(
            template='plotly_dark',
            title=f'{ticker} - Quantum Price Analysis',
            yaxis_title='Price (USD)',
            xaxis_title='Date',
            height=500,
            paper_bgcolor='rgba(16, 20, 46, 0.6)',
            plot_bgcolor='rgba(16, 20, 46, 0.3)',
            font=dict(family="Courier New, monospace", size=12, color="#ccd6f6"),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabs para análisis adicional
        tab1, tab2, tab3, tab4 = st.tabs(["📊 STATISTICS", "📉 RETURNS", "📈 TECHNICALS", "ℹ️ INFORMATION"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📐 Statistical Metrics")
                returns = data['Close'].pct_change().dropna()
                
                stats_df = pd.DataFrame({
                    'Metric': ['Volatility (Annualized)', 'Sharpe Ratio (approx)', 'Max Drawdown', 'Skewness', 'Kurtosis'],
                    'Value': [
                        f"{returns.std() * np.sqrt(252) * 100:.2f}%",
                        f"{returns.mean() / returns.std() * np.sqrt(252):.2f}",
                        f"{((data['Close'].cummax() - data['Close']) / data['Close'].cummax()).max() * 100:.2f}%",
                        f"{returns.skew():.3f}",
                        f"{returns.kurtosis():.3f}"
                    ]
                })
                
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("#### 📊 Performance Summary")
                cumulative_return = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
                
                perf_df = pd.DataFrame({
                    'Metric': ['Cumulative Return', 'Average Daily Return', 'Best Day', 'Worst Day', 'Positive Days (%)'],
                    'Value': [
                        f"{cumulative_return:.2f}%",
                        f"{returns.mean() * 100:.3f}%",
                        f"{returns.max() * 100:.2f}%",
                        f"{returns.min() * 100:.2f}%",
                        f"{(returns > 0).sum() / len(returns) * 100:.1f}%"
                    ]
                })
                
                st.dataframe(perf_df, use_container_width=True, hide_index=True)
        
        with tab2:
            st.markdown("#### 📊 Return Distribution Analysis")
            
            # Histograma de returns
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=returns * 100,
                nbinsx=50,
                marker_color='#00d4ff',
                opacity=0.7,
                name='Daily Returns'
            ))
            
            fig_hist.update_layout(
                template='plotly_dark',
                title='Daily Returns Distribution',
                xaxis_title='Return (%)',
                yaxis_title='Frequency',
                height=400,
                paper_bgcolor='rgba(16, 20, 46, 0.6)',
                plot_bgcolor='rgba(16, 20, 46, 0.3)'
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Tabla de returns por período
            st.markdown("#### 📅 Period Returns")
            returns_periods = {
                'Week': returns.iloc[-5:].sum() * 100,
                'Month': returns.iloc[-21:].sum() * 100,
                'Quarter': returns.iloc[-63:].sum() * 100,
                'YTD': returns[returns.index >= datetime(datetime.now().year, 1, 1)].sum() * 100
            }
            
            period_returns_df = pd.DataFrame(list(returns_periods.items()), columns=['Period', 'Return (%)'])
            st.dataframe(period_returns_df, use_container_width=True, hide_index=True)
        
        with tab3:
            if show_rsi:
                # Calcular RSI
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(
                    x=data.index, y=rsi,
                    name='RSI 14',
                    line=dict(color='#00d4ff', width=2)
                ))
                
                # Añadir bandas de sobrecompra/sobreventa
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                
                fig_rsi.update_layout(
                    template='plotly_dark',
                    title='Relative Strength Index (RSI)',
                    yaxis_title='RSI Value',
                    height=400,
                    paper_bgcolor='rgba(16, 20, 46, 0.6)',
                    plot_bgcolor='rgba(16, 20, 46, 0.3)'
                )
                
                st.plotly_chart(fig_rsi, use_container_width=True)
            else:
                st.info("📊 Enable RSI Indicator in sidebar controls to display technical analysis")
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏢 Company Profile")
                company_info = {
                    'Name': info.get('longName', 'N/A'),
                    'Sector': info.get('sector', 'N/A'),
                    'Industry': info.get('industry', 'N/A'),
                    'Country': info.get('country', 'N/A'),
                    'Website': info.get('website', 'N/A')
                }
                
                for key, value in company_info.items():
                    st.markdown(f"**{key}:** {value}")
            
            with col2:
                st.markdown("#### 💰 Valuation Metrics")
                valuation = {
                    'P/E Ratio': f"{info.get('trailingPE', 'N/A')}",
                    'P/B Ratio': f"{info.get('priceToBook', 'N/A')}",
                    'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else 'N/A',
                    'Beta': f"{info.get('beta', 'N/A')}",
                    '52W High': f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
                    '52W Low': f"${info.get('fiftyTwoWeekLow', 'N/A')}"
                }
                
                for key, value in valuation.items():
                    st.markdown(f"**{key}:** {value}")
    
    else:
        st.error(f"❌ Unable to load data for symbol '{ticker}'. Please check the symbol and try again.")
        
else:
    st.warning("⚠️ Please enter a stock symbol to begin analysis")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #667; font-size: 12px;'>
    ⚡ Quantum Finance Analytics System v1.0 | Data delayed by 15-20 minutes | Not financial advice
</p>
""", unsafe_allow_html=True)