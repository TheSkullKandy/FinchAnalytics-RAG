"""
Pydantic schemas for LLM Stock Analyst API
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ErrorResponse(BaseModel):
    """Standard error response schema"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., description="User's question about stock valuation")
    stock_symbol: Optional[str] = Field(None, description="Stock symbol (e.g., AAPL)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    response: str = Field(..., description="AI-generated response")
    stock_symbol: Optional[str] = Field(None, description="Stock symbol if identified")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    sources: List[str] = Field(default_factory=list, description="Data sources used")
    timestamp: datetime = Field(default_factory=datetime.now)

class ValuationMethod(str, Enum):
    """Supported valuation methods"""
    DCF = "dcf"
    PEG = "peg"
    PE = "pe"
    COMPARATIVE = "comparative"

class ValuationRequest(BaseModel):
    """Request schema for valuation endpoint"""
    stock_symbol: str = Field(..., description="Stock symbol to analyze")
    valuation_methods: List[ValuationMethod] = Field(
        default=[ValuationMethod.DCF, ValuationMethod.PEG, ValuationMethod.PE],
        description="Valuation methods to apply"
    )
    assumptions: Optional[Dict[str, Any]] = Field(None, description="Custom assumptions")

class FinancialMetrics(BaseModel):
    """Financial metrics for a stock"""
    current_price: float
    market_cap: float
    pe_ratio: Optional[float]
    peg_ratio: Optional[float]
    price_to_book: Optional[float]
    debt_to_equity: Optional[float]
    revenue_growth: Optional[float]
    earnings_growth: Optional[float]
    free_cash_flow: Optional[float]

class ValuationResult(BaseModel):
    """Individual valuation result"""
    method: ValuationMethod
    estimated_value: float
    confidence_interval: tuple[float, float]
    assumptions: Dict[str, Any]
    calculation_details: Dict[str, Any]

class ValuationResponse(BaseModel):
    """Response schema for valuation endpoint"""
    stock_symbol: str
    current_price: float
    financial_metrics: FinancialMetrics
    valuations: List[ValuationResult]
    recommendation: str
    risk_factors: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

class PowerBIRequest(BaseModel):
    """Request schema for Power BI integration"""
    dataset_name: str = Field(..., description="Power BI dataset name")
    data: Dict[str, Any] = Field(..., description="Data to push to Power BI")
    table_name: Optional[str] = Field(None, description="Target table name")

class PowerBIResponse(BaseModel):
    """Response schema for Power BI integration"""
    success: bool
    message: str
    dataset_id: Optional[str] = None
    rows_added: Optional[int] = None

class StockInfo(BaseModel):
    """Basic stock information"""
    symbol: str
    company_name: str
    sector: Optional[str]
    industry: Optional[str]
    exchange: str
    country: str

class DataSource(BaseModel):
    """Data source information"""
    name: str
    url: str
    last_updated: datetime
    reliability_score: float

class AnalysisContext(BaseModel):
    """Context for analysis"""
    market_conditions: Dict[str, Any]
    economic_indicators: Dict[str, Any]
    sector_performance: Dict[str, Any]
    data_sources: List[DataSource] 