"""
LLM Stock Analyst - Streamlit Frontend Application
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
from typing import Dict, Any, Optional

# Page configuration
st.set_page_config(
    page_title="LLM Stock Analyst",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_stock" not in st.session_state:
    st.session_state.current_stock = None

if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://localhost:8000/api/v1"

# API configuration - can be overridden in settings
def get_api_base_url():
    """Get the API base URL, with fallback options"""
    # Check if we're running on Streamlit Cloud
    if st.session_state.get("api_base_url"):
        return st.session_state.api_base_url
    
    # Default to local development
    return "http://localhost:8000/api/v1"

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📈 LLM Stock Analyst</h1>', unsafe_allow_html=True)
    st.markdown("### Intelligent Stock Valuation Powered by AI")
    
    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a page",
            ["Chat Interface", "Valuation Dashboard", "Settings"]
        )
        
        st.header("Quick Actions")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.button("Check API Status"):
            check_api_status()
    
    # Page routing
    if page == "Chat Interface":
        chat_interface()
    elif page == "Valuation Dashboard":
        valuation_dashboard()
    elif page == "Settings":
        settings_page()

def chat_interface():
    """Chat interface for interacting with the AI analyst"""
    
    st.header("💬 Chat with AI Analyst")
    st.markdown("Ask questions about stock valuation, market analysis, or get investment insights.")
    
    # Stock symbol input
    col1, col2 = st.columns([3, 1])
    with col1:
        stock_symbol = st.text_input(
            "Stock Symbol (optional)",
            placeholder="e.g., AAPL, MSFT, GOOGL",
            value=st.session_state.current_stock or ""
        )
    with col2:
        if st.button("Set Stock"):
            st.session_state.current_stock = stock_symbol.upper()
            st.rerun()
    
    # Chat input
    user_input = st.chat_input("Ask about stock valuation...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Get AI response
        response = get_ai_response(user_input, stock_symbol)
        
        # Add AI response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        
        st.rerun()
    
    # Display chat history
    display_chat_history()

def valuation_dashboard():
    """Valuation dashboard for detailed stock analysis"""
    
    st.header("📊 Valuation Dashboard")
    
    # Stock input
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        stock_symbol = st.text_input(
            "Enter Stock Symbol",
            placeholder="e.g., AAPL",
            value=st.session_state.current_stock or ""
        )
    
    with col2:
        valuation_methods = st.multiselect(
            "Valuation Methods",
            ["DCF", "PEG", "P/E", "Comparative"],
            default=["DCF", "PEG", "P/E"]
        )
    
    with col3:
        if st.button("Analyze Stock", type="primary"):
            if stock_symbol:
                perform_valuation(stock_symbol, valuation_methods)
            else:
                st.error("Please enter a stock symbol")
    
    # Display valuation results if available
    if "valuation_results" in st.session_state:
        display_valuation_results()

def settings_page():
    """Settings and configuration page"""
    
    st.header("⚙️ Settings")
    
    st.subheader("API Configuration")
    
    # API URL configuration
    api_url = st.text_input(
        "Backend API URL",
        value=get_api_base_url(),
        help="URL of the FastAPI backend (e.g., http://localhost:8000/api/v1 or your deployed backend URL)"
    )
    
    # Test API connection
    if st.button("Test API Connection"):
        test_api_connection(api_url)
    
    # Save API URL
    if st.button("Save API URL"):
        st.session_state.api_base_url = api_url
        st.success("API URL saved successfully!")
    
    st.subheader("Application Settings")
    
    # Theme selection
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        help="Choose the application theme"
    )
    
    # Data refresh interval
    refresh_interval = st.slider(
        "Data Refresh Interval (seconds)",
        min_value=30,
        max_value=300,
        value=60,
        step=30
    )
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def get_ai_response(message: str, stock_symbol: Optional[str] = None) -> str:
    """Get response from AI analyst"""
    
    try:
        payload = {
            "message": message,
            "stock_symbol": stock_symbol.upper() if stock_symbol else None
        }
        
        response = requests.post(
            f"{get_api_base_url()}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "Sorry, I couldn't generate a response.")
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Connection error: {str(e)}"

def perform_valuation(stock_symbol: str, methods: list):
    """Perform stock valuation analysis"""
    
    try:
        # Convert method names to API format
        method_mapping = {
            "DCF": "dcf",
            "PEG": "peg", 
            "P/E": "pe",
            "Comparative": "comparative"
        }
        
        api_methods = [method_mapping.get(method, method.lower()) for method in methods]
        
        payload = {
            "stock_symbol": stock_symbol.upper(),
            "valuation_methods": api_methods
        }
        
        with st.spinner(f"Analyzing {stock_symbol}..."):
            response = requests.post(
                f"{get_api_base_url()}/valuation",
                json=payload,
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.valuation_results = data
            st.success(f"Analysis completed for {stock_symbol}")
        else:
            st.error(f"Valuation failed: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")

def display_chat_history():
    """Display chat history"""
    
    if not st.session_state.chat_history:
        st.info("Start a conversation by asking about stock valuation!")
        return
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["content"]}
                <br><small>{message["timestamp"].strftime("%H:%M")}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>AI Analyst:</strong> {message["content"]}
                <br><small>{message["timestamp"].strftime("%H:%M")}</small>
            </div>
            """, unsafe_allow_html=True)

def display_valuation_results():
    """Display valuation analysis results"""
    
    results = st.session_state.valuation_results
    
    # Stock overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Current Price",
            f"${results.get('current_price', 0):.2f}"
        )
    
    with col2:
        st.metric(
            "Market Cap",
            f"${results.get('financial_metrics', {}).get('market_cap', 0):,.0f}M"
        )
    
    with col3:
        st.metric(
            "P/E Ratio",
            f"{results.get('financial_metrics', {}).get('pe_ratio', 'N/A')}"
        )
    
    with col4:
        st.metric(
            "Recommendation",
            results.get('recommendation', 'N/A')
        )
    
    # Valuation results
    st.subheader("Valuation Results")
    
    valuations = results.get('valuations', [])
    if valuations:
        valuation_data = []
        for val in valuations:
            valuation_data.append({
                "Method": val.get('method', '').upper(),
                "Estimated Value": f"${val.get('estimated_value', 0):.2f}",
                "Confidence": f"${val.get('confidence_interval', [0, 0])[0]:.2f} - ${val.get('confidence_interval', [0, 0])[1]:.2f}"
            })
        
        df = pd.DataFrame(valuation_data)
        st.dataframe(df, use_container_width=True)
    
    # Risk factors
    risk_factors = results.get('risk_factors', [])
    if risk_factors:
        st.subheader("Risk Factors")
        for risk in risk_factors:
            st.warning(f"⚠️ {risk}")

def check_api_status():
    """Check API status"""
    
    try:
        response = requests.get(f"{get_api_base_url().replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ API Connected")
        else:
            st.sidebar.error("❌ API Error")
    except:
        st.sidebar.error("❌ API Unavailable")

def test_api_connection(api_url: str):
    """Test API connection"""
    
    try:
        response = requests.get(f"{api_url.replace('/api/v1', '')}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ API connection successful!")
        else:
            st.error(f"❌ API error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")

if __name__ == "__main__":
    main() 