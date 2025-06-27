"""
Valuation router for handling stock valuation analysis
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import List

from models.schemas import (
    ValuationRequest, 
    ValuationResponse, 
    ValuationMethod,
    FinancialMetrics,
    ValuationResult
)
from services.valuation_engine import ValuationEngine
from services.retriever import DataRetriever

router = APIRouter()

# Initialize services
valuation_engine = ValuationEngine()
data_retriever = DataRetriever()

@router.post("/valuation", response_model=ValuationResponse)
async def perform_valuation(request: ValuationRequest):
    """
    Perform comprehensive stock valuation analysis
    
    This endpoint applies multiple valuation methods to a given stock
    and returns detailed analysis with recommendations.
    """
    try:
        logger.info(f"Performing valuation for {request.stock_symbol}")
        
        # Retrieve comprehensive financial data
        stock_data = await data_retriever.get_stock_data(request.stock_symbol)
        market_context = await data_retriever.get_market_context()
        
        if not stock_data:
            raise HTTPException(
                status_code=404,
                detail=f"Could not retrieve data for stock symbol: {request.stock_symbol}"
            )
        
        # Extract financial metrics
        financial_metrics = extract_financial_metrics(stock_data)
        
        # Perform valuations for each requested method
        valuations = []
        for method in request.valuation_methods:
            try:
                valuation_result = await perform_single_valuation(
                    method=method,
                    stock_data=stock_data,
                    market_context=market_context,
                    assumptions=request.assumptions
                )
                valuations.append(valuation_result)
            except Exception as e:
                logger.warning(f"Failed to perform {method} valuation: {str(e)}")
                # Continue with other methods
        
        # Generate recommendation
        recommendation = generate_recommendation(valuations, financial_metrics)
        
        # Identify risk factors
        risk_factors = identify_risk_factors(stock_data, market_context)
        
        return ValuationResponse(
            stock_symbol=request.stock_symbol,
            current_price=financial_metrics.current_price,
            financial_metrics=financial_metrics,
            valuations=valuations,
            recommendation=recommendation,
            risk_factors=risk_factors
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in valuation endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to perform valuation: {str(e)}"
        )

@router.get("/valuation/methods")
async def get_valuation_methods():
    """
    Get available valuation methods and their descriptions
    """
    return {
        "methods": [
            {
                "method": ValuationMethod.DCF,
                "name": "Discounted Cash Flow",
                "description": "Values stock based on future cash flows discounted to present value",
                "complexity": "High",
                "data_requirements": ["Financial statements", "Growth projections", "Discount rate"]
            },
            {
                "method": ValuationMethod.PEG,
                "name": "Price/Earnings to Growth",
                "description": "Compares P/E ratio to earnings growth rate",
                "complexity": "Medium",
                "data_requirements": ["P/E ratio", "Earnings growth rate"]
            },
            {
                "method": ValuationMethod.PE,
                "name": "Price/Earnings",
                "description": "Compares stock price to earnings per share",
                "complexity": "Low",
                "data_requirements": ["Current price", "Earnings per share"]
            },
            {
                "method": ValuationMethod.COMPARATIVE,
                "name": "Comparative Analysis",
                "description": "Compares to similar companies in the same industry",
                "complexity": "Medium",
                "data_requirements": ["Peer company data", "Industry metrics"]
            }
        ]
    }

async def perform_single_valuation(
    method: ValuationMethod,
    stock_data: dict,
    market_context: dict,
    assumptions: dict = None
) -> ValuationResult:
    """
    Perform valuation using a specific method
    """
    if method == ValuationMethod.DCF:
        return await valuation_engine.dcf_valuation(stock_data, market_context, assumptions)
    elif method == ValuationMethod.PEG:
        return await valuation_engine.peg_valuation(stock_data, market_context, assumptions)
    elif method == ValuationMethod.PE:
        return await valuation_engine.pe_valuation(stock_data, market_context, assumptions)
    elif method == ValuationMethod.COMPARATIVE:
        return await valuation_engine.comparative_valuation(stock_data, market_context, assumptions)
    else:
        raise ValueError(f"Unsupported valuation method: {method}")

def extract_financial_metrics(stock_data: dict) -> FinancialMetrics:
    """
    Extract financial metrics from stock data
    
    TODO: Implement proper data extraction and validation
    """
    return FinancialMetrics(
        current_price=stock_data.get('current_price', 0.0),
        market_cap=stock_data.get('market_cap', 0.0),
        pe_ratio=stock_data.get('pe_ratio'),
        peg_ratio=stock_data.get('peg_ratio'),
        price_to_book=stock_data.get('price_to_book'),
        debt_to_equity=stock_data.get('debt_to_equity'),
        revenue_growth=stock_data.get('revenue_growth'),
        earnings_growth=stock_data.get('earnings_growth'),
        free_cash_flow=stock_data.get('free_cash_flow')
    )

def generate_recommendation(valuations: List[ValuationResult], metrics: FinancialMetrics) -> str:
    """
    Generate investment recommendation based on valuation results
    
    TODO: Implement more sophisticated recommendation logic
    - Weight different valuation methods
    - Consider market conditions
    - Factor in risk assessment
    """
    if not valuations:
        return "Insufficient data for recommendation"
    
    # Calculate average estimated value
    avg_value = sum(v.estimated_value for v in valuations) / len(valuations)
    current_price = metrics.current_price
    
    # Simple recommendation logic
    if avg_value > current_price * 1.2:
        return "Strong Buy - Multiple valuation methods suggest significant upside"
    elif avg_value > current_price * 1.05:
        return "Buy - Valuation suggests moderate upside potential"
    elif avg_value < current_price * 0.8:
        return "Sell - Valuation suggests significant downside risk"
    elif avg_value < current_price * 0.95:
        return "Hold - Valuation suggests slight downside risk"
    else:
        return "Hold - Valuation is approximately fair value"

def identify_risk_factors(stock_data: dict, market_context: dict) -> List[str]:
    """
    Identify potential risk factors for the stock
    
    TODO: Implement comprehensive risk assessment
    - Financial risk factors
    - Market risk factors
    - Sector-specific risks
    - Regulatory risks
    """
    risk_factors = []
    
    # Financial risk factors
    if stock_data.get('debt_to_equity', 0) > 1.0:
        risk_factors.append("High debt-to-equity ratio")
    
    if stock_data.get('pe_ratio', 0) > 30:
        risk_factors.append("High P/E ratio may indicate overvaluation")
    
    # Market risk factors
    if market_context.get('market_volatility', 0) > 0.3:
        risk_factors.append("High market volatility")
    
    # Add more risk factor logic here
    
    return risk_factors if risk_factors else ["No significant risk factors identified"] 