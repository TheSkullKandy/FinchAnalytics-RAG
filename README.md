# LLM Stock Analyst

An intelligent stock valuation chatbot powered by LLMs that provides comprehensive financial analysis using DCF, PEG, and P/E valuation methods.

## 🚀 Features

- **Intelligent Chat Interface**: Natural language queries about stock valuation
- **Multiple Valuation Models**: DCF (Discounted Cash Flow), PEG (Price/Earnings to Growth), P/E (Price/Earnings)
- **Real-time Data Retrieval**: SEC filings, Yahoo Finance, FRED economic data
- **Power BI Integration**: Automated data pushing to Power BI dashboards
- **Modern UI**: Streamlit-based frontend with interactive dashboards

## 🏗️ Architecture

- **Backend**: FastAPI with Python
- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-4
- **Data Sources**: SEC, Yahoo Finance, FRED
- **Analytics**: Power BI integration

## 📁 Project Structure

```
llm-stock-analyst/
├── backend/                 # FastAPI backend
│   ├── main.py             # FastAPI app entry point
│   ├── routers/            # API endpoints
│   ├── services/           # Business logic
│   ├── models/             # Pydantic schemas
│   ├── data/               # Temporary data storage
│   ├── utils/              # Helper functions
│   └── requirements.txt    # Python dependencies
├── frontend/               # Streamlit frontend
│   ├── app.py             # Main Streamlit app
│   ├── pages/             # Multi-page app
│   ├── components/        # Custom UI components
│   └── assets/            # Static files
├── .env                   # Environment variables
├── start.sh              # Startup script
└── README.md             # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- OpenAI API key
- Power BI API credentials (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd llm-stock-analyst
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd ../frontend
   pip install streamlit
   ```

5. **Run the application**
   ```bash
   # From project root
   chmod +x start.sh
   ./start.sh
   ```

## 🚀 Usage

1. **Start the application**: Run `./start.sh` from the project root
2. **Access the frontend**: Open http://localhost:8501 in your browser
3. **API documentation**: Visit http://localhost:8000/docs for FastAPI docs

## 📊 API Endpoints

- `POST /chat` - Handle user queries
- `POST /valuation` - Perform stock valuation analysis
- `POST /powerbi` - Push data to Power BI

## 🔧 Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
streamlit run app.py --server.port 8501
```

## 📝 TODO

- [ ] Implement DCF valuation logic
- [ ] Add PEG and P/E calculations
- [ ] Integrate SEC data retrieval
- [ ] Set up Power BI API integration
- [ ] Add error handling and logging
- [ ] Implement caching for API responses
- [ ] Add unit tests
- [ ] Deploy to production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 