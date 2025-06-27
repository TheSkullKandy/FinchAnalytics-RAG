# LLM Stock Analyst - Frontend

The Streamlit-based frontend for the LLM Stock Analyst application, providing an intuitive interface for stock valuation analysis and AI-powered financial insights.

## 🚀 Features

- **Chat Interface**: Natural language interaction with AI analyst
- **Valuation Dashboard**: Comprehensive stock analysis with multiple valuation methods
- **Real-time Data**: Live financial data integration
- **Interactive Charts**: Visual representation of valuation results
- **Responsive Design**: Modern, user-friendly interface

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Streamlit
- Backend API running (FastAPI)

### Installation

1. **Install Streamlit**
   ```bash
   pip install streamlit
   ```

2. **Install additional dependencies**
   ```bash
   pip install requests pandas plotly
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📱 Usage

### Chat Interface

1. **Enter Stock Symbol** (optional)
   - Type a stock symbol (e.g., AAPL, MSFT, GOOGL)
   - Click "Set Stock" to focus analysis on that stock

2. **Ask Questions**
   - Use natural language to ask about stock valuation
   - Examples:
     - "What is the fair value of AAPL?"
     - "Should I invest in Tesla?"
     - "Compare Apple and Microsoft"

3. **View Responses**
   - AI-generated responses with financial analysis
   - Confidence scores and data sources
   - Chat history for reference

### Valuation Dashboard

1. **Enter Stock Symbol**
   - Type the stock symbol to analyze

2. **Select Valuation Methods**
   - DCF (Discounted Cash Flow)
   - PEG (Price/Earnings to Growth)
   - P/E (Price/Earnings)
   - Comparative Analysis

3. **Customize Assumptions**
   - Adjust growth rate for DCF analysis
   - Modify discount rate
   - Set other valuation parameters

4. **Run Analysis**
   - Click "Run Analysis" to perform comprehensive valuation
   - View results in interactive charts and tables

## 🎨 Interface Components

### Main Dashboard
- **Stock Overview**: Current price, market cap, P/E ratio, recommendation
- **Valuation Results**: Comparison of different valuation methods
- **Financial Metrics**: Key ratios and growth indicators
- **Risk Analysis**: Identified risk factors and assessment

### Charts and Visualizations
- **Valuation Comparison**: Bar chart comparing different methods
- **Confidence Intervals**: Range of estimated values
- **Price Trends**: Historical price analysis (future implementation)
- **Risk Distribution**: Risk factor visualization (future implementation)

## ⚙️ Configuration

### API Settings
- **Backend URL**: Configure the FastAPI backend URL
- **Connection Testing**: Verify API connectivity
- **Timeout Settings**: Adjust request timeouts

### Application Settings
- **Theme**: Light or dark mode
- **Data Refresh**: Set automatic refresh intervals
- **Display Options**: Customize chart and table displays

## 🔧 Development

### Project Structure
```
frontend/
├── app.py                 # Main Streamlit application
├── pages/                 # Multi-page app components
│   └── Valuation_Dashboard.py
├── components/            # Custom UI components (future)
├── assets/               # Static files (future)
└── README.md             # This file
```

### Adding New Features

1. **New Pages**
   - Create new files in `pages/` directory
   - Use Streamlit's multi-page app structure

2. **Custom Components**
   - Add reusable components in `components/` directory
   - Import and use in main app or pages

3. **Styling**
   - Modify CSS in the main app
   - Use Streamlit's theming options

### API Integration

The frontend communicates with the backend via REST API:

- **Chat Endpoint**: `POST /api/v1/chat`
- **Valuation Endpoint**: `POST /api/v1/valuation`
- **Health Check**: `GET /health`

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Verify backend is running on correct port
   - Check API URL in settings
   - Ensure CORS is properly configured

2. **Missing Dependencies**
   - Install required packages: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Streamlit Issues**
   - Clear cache: `streamlit cache clear`
   - Restart application
   - Check Streamlit version compatibility

### Debug Mode

Run with debug information:
```bash
streamlit run app.py --logger.level debug
```

## 📊 Data Sources

The frontend displays data from:
- **Yahoo Finance**: Real-time stock data
- **SEC Filings**: Financial statements and reports
- **FRED**: Economic indicators
- **AI Analysis**: LLM-generated insights

## 🔮 Future Enhancements

- [ ] Advanced charting with Plotly
- [ ] Real-time data streaming
- [ ] Portfolio management features
- [ ] Export functionality (PDF, Excel)
- [ ] Mobile-responsive design
- [ ] Dark mode support
- [ ] Custom themes
- [ ] Data caching and optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 