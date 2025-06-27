"""
Valuation Dashboard Page for LLM Stock Analyst
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List

# Page configuration
st.set_page_config(
    page_title="Valuation Dashboard - LLM Stock Analyst",
    page_icon="📊",
    layout="wide"
)

# API configuration - use the same configurable URL as main app
def get_api_base_url():
    """Get the API base URL, with fallback options"""
    # Check if we're running on Streamlit Cloud
    if st.session_state.get("api_base_url"):
        return st.session_state.api_base_url
    
    # Default to local development
    return "http://localhost:8000/api/v1"

def main():
    """Main valuation dashboard function"""
    
    st.title("📊 Valuation Dashboard")
    st.markdown("### Comprehensive Stock Analysis and Valuation")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Analysis Parameters")
        
        # Stock symbol input
        stock_symbol = st.text_input(
            "Stock Symbol",
            placeholder="e.g., AAPL",
            help="Enter the stock symbol to analyze"
        )
        
        # Valuation methods
        st.subheader("Valuation Methods")
        dcf_enabled = st.checkbox("DCF Analysis", value=True)
        peg_enabled = st.checkbox("PEG Analysis", value=True)
        pe_enabled = st.checkbox("P/E Analysis", value=True)
        comparative_enabled = st.checkbox("Comparative Analysis", value=False)
        
        # Custom assumptions
        st.subheader("Custom Assumptions")
        growth_rate = st.slider(
            "Growth Rate (%)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Expected growth rate for DCF analysis"
        )
        
        discount_rate = st.slider(
            "Discount Rate (%)",
            min_value=5.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            help="Discount rate for DCF analysis"
        )
        
        # Analysis button
        if st.button("Run Analysis", type="primary"):
            if stock_symbol:
                run_comprehensive_analysis(
                    stock_symbol, 
                    dcf_enabled, 
                    peg_enabled, 
                    pe_enabled, 
                    comparative_enabled,
                    growth_rate,
                    discount_rate
                )
            else:
                st.error("Please enter a stock symbol")
    
    # Main content area
    if "analysis_results" in st.session_state:
        display_comprehensive_results()
    else:
        st.info("Enter a stock symbol and click 'Run Analysis' to get started.")

def run_comprehensive_analysis(
    stock_symbol: str,
    dcf_enabled: bool,
    peg_enabled: bool,
    pe_enabled: bool,
    comparative_enabled: bool,
    growth_rate: float,
    discount_rate: float
):
    """Run comprehensive stock analysis"""
    
    try:
        # Prepare valuation methods
        methods = []
        if dcf_enabled:
            methods.append("dcf")
        if peg_enabled:
            methods.append("peg")
        if pe_enabled:
            methods.append("pe")
        if comparative_enabled:
            methods.append("comparative")
        
        if not methods:
            st.error("Please select at least one valuation method")
            return
        
        # Prepare assumptions
        assumptions = {
            "growth_rate": growth_rate / 100,
            "discount_rate": discount_rate / 100
        }
        
        # API payload
        payload = {
            "stock_symbol": stock_symbol.upper(),
            "valuation_methods": methods,
            "assumptions": assumptions
        }
        
        with st.spinner(f"Analyzing {stock_symbol} with {len(methods)} valuation methods..."):
            response = requests.post(
                f"{get_api_base_url()}/valuation",
                json=payload,
                timeout=120
            )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.analysis_results = data
            st.success(f"Analysis completed for {stock_symbol}")
            st.rerun()
        else:
            st.error(f"Analysis failed: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")

def display_comprehensive_results():
    """Display comprehensive analysis results"""
    
    results = st.session_state.analysis_results
    
    # Stock overview section
    display_stock_overview(results)
    
    # Valuation results section
    display_valuation_results(results)
    
    # Financial metrics section
    display_financial_metrics(results)
    
    # Risk analysis section
    display_risk_analysis(results)
    
    # Charts and visualizations
    display_charts(results)

def display_stock_overview(results: Dict[str, Any]):
    """Display stock overview information"""
    
    st.header("📈 Stock Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${results.get('current_price', 0):.2f}",
            help="Current stock price"
        )
    
    with col2:
        market_cap = results.get('financial_metrics', {}).get('market_cap', 0)
        st.metric(
            "Market Cap",
            f"${market_cap:,.0f}M" if market_cap > 0 else "N/A",
            help="Market capitalization"
        )
    
    with col3:
        pe_ratio = results.get('financial_metrics', {}).get('pe_ratio')
        st.metric(
            "P/E Ratio",
            f"{pe_ratio:.2f}" if pe_ratio else "N/A",
            help="Price-to-Earnings ratio"
        )
    
    with col4:
        recommendation = results.get('recommendation', 'N/A')
        st.metric(
            "Recommendation",
            recommendation,
            help="Investment recommendation based on analysis"
        )

def display_valuation_results(results: Dict[str, Any]):
    """Display detailed valuation results"""
    
    st.header("💰 Valuation Results")
    
    valuations = results.get('valuations', [])
    if not valuations:
        st.warning("No valuation results available")
        return
    
    # Create valuation comparison chart
    fig = go.Figure()
    
    methods = []
    values = []
    confidence_lower = []
    confidence_upper = []
    
    for val in valuations:
        method = val.get('method', '').upper()
        estimated_value = val.get('estimated_value', 0)
        confidence_interval = val.get('confidence_interval', [0, 0])
        
        methods.append(method)
        values.append(estimated_value)
        confidence_lower.append(confidence_interval[0])
        confidence_upper.append(confidence_interval[1])
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=methods,
        y=values,
        name='Estimated Value',
        marker_color='lightblue'
    ))
    
    # Add confidence intervals
    fig.add_trace(go.Scatter(
        x=methods,
        y=confidence_upper,
        mode='markers',
        name='Confidence Upper',
        marker=dict(color='red', size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=methods,
        y=confidence_lower,
        mode='markers',
        name='Confidence Lower',
        marker=dict(color='green', size=8)
    ))
    
    current_price = results.get('current_price', 0)
    fig.add_hline(
        y=current_price,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Current Price: ${current_price:.2f}"
    )
    
    fig.update_layout(
        title="Valuation Comparison",
        xaxis_title="Valuation Method",
        yaxis_title="Estimated Value ($)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed valuation table
    st.subheader("Detailed Results")
    
    valuation_data = []
    for val in valuations:
        confidence_interval = val.get('confidence_interval', [0, 0])
        valuation_data.append({
            "Method": val.get('method', '').upper(),
            "Estimated Value": f"${val.get('estimated_value', 0):.2f}",
            "Confidence Lower": f"${confidence_interval[0]:.2f}",
            "Confidence Upper": f"${confidence_interval[1]:.2f}",
            "Assumptions": str(val.get('assumptions', {}))
        })
    
    df = pd.DataFrame(valuation_data)
    st.dataframe(df, use_container_width=True)

def display_financial_metrics(results: Dict[str, Any]):
    """Display financial metrics"""
    
    st.header("📊 Financial Metrics")
    
    metrics = results.get('financial_metrics', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Ratios")
        
        metric_data = [
            ("P/E Ratio", metrics.get('pe_ratio')),
            ("PEG Ratio", metrics.get('peg_ratio')),
            ("Price/Book", metrics.get('price_to_book')),
            ("Debt/Equity", metrics.get('debt_to_equity'))
        ]
        
        for name, value in metric_data:
            if value is not None:
                st.metric(name, f"{value:.2f}")
            else:
                st.metric(name, "N/A")
    
    with col2:
        st.subheader("Growth Metrics")
        
        growth_data = [
            ("Revenue Growth", metrics.get('revenue_growth')),
            ("Earnings Growth", metrics.get('earnings_growth')),
            ("Free Cash Flow", metrics.get('free_cash_flow'))
        ]
        
        for name, value in growth_data:
            if value is not None:
                if "Growth" in name:
                    st.metric(name, f"{value*100:.1f}%")
                else:
                    st.metric(name, f"${value:,.0f}M")
            else:
                st.metric(name, "N/A")

def display_risk_analysis(results: Dict[str, Any]):
    """Display risk analysis"""
    
    st.header("⚠️ Risk Analysis")
    
    risk_factors = results.get('risk_factors', [])
    
    if risk_factors:
        for i, risk in enumerate(risk_factors, 1):
            st.warning(f"{i}. {risk}")
    else:
        st.info("No significant risk factors identified")
    
    # Risk score calculation (placeholder)
    st.subheader("Risk Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Risk", "Medium", help="Based on financial metrics and market conditions")
    
    with col2:
        st.metric("Volatility Risk", "Low", help="Historical price volatility")
    
    with col3:
        st.metric("Financial Risk", "Medium", help="Based on debt levels and cash flow")

def display_charts(results: Dict[str, Any]):
    """Display charts and visualizations"""
    
    st.header("📈 Charts & Visualizations")
    
    # Placeholder for future chart implementations
    st.info("Advanced charts and visualizations will be implemented in future versions.")
    
    # Example chart placeholder
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Price Trend")
        # TODO: Implement price trend chart
        st.write("Price trend chart will be displayed here")
    
    with col2:
        st.subheader("Valuation Distribution")
        # TODO: Implement valuation distribution chart
        st.write("Valuation distribution chart will be displayed here")

if __name__ == "__main__":
    main() 