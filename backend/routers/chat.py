"""
Chat router for handling user queries about stock valuation
"""

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from typing import Optional

from models.schemas import ChatRequest, ChatResponse, ErrorResponse
from services.llm_interface import LLMInterface
from services.retriever import DataRetriever

router = APIRouter()

# Initialize services
llm_interface = LLMInterface()
data_retriever = DataRetriever()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_analyst(request: ChatRequest):
    """
    Handle user queries about stock valuation
    
    This endpoint processes natural language questions about stocks and returns
    intelligent responses using LLM analysis and financial data retrieval.
    """
    try:
        logger.info(f"Processing chat request: {request.message}")
        
        # Extract stock symbol from message if not provided
        stock_symbol = request.stock_symbol
        if not stock_symbol:
            # TODO: Implement stock symbol extraction from message
            stock_symbol = extract_stock_symbol(request.message)
        
        # Retrieve relevant financial data
        if stock_symbol:
            financial_data = await data_retriever.get_stock_data(stock_symbol)
            market_context = await data_retriever.get_market_context()
        else:
            financial_data = None
            market_context = None
        
        # Generate response using LLM
        response = await llm_interface.generate_response(
            user_message=request.message,
            stock_symbol=stock_symbol,
            financial_data=financial_data,
            market_context=market_context,
            additional_context=request.context
        )
        
        # Determine confidence score
        confidence = calculate_confidence(response, financial_data)
        
        # Get data sources used
        sources = get_data_sources(financial_data, market_context)
        
        return ChatResponse(
            response=response,
            stock_symbol=stock_symbol,
            confidence=confidence,
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )

@router.get("/chat/history")
async def get_chat_history(limit: int = 10):
    """
    Get recent chat history (placeholder for future implementation)
    """
    # TODO: Implement chat history storage and retrieval
    return {
        "message": "Chat history feature not yet implemented",
        "limit": limit
    }

def extract_stock_symbol(message: str) -> Optional[str]:
    """
    Extract stock symbol from user message
    
    TODO: Implement more sophisticated stock symbol extraction
    - Use regex patterns for common stock symbol formats
    - Integrate with company name to symbol mapping
    - Handle ambiguous cases
    """
    # Simple regex for stock symbols (1-5 uppercase letters)
    import re
    pattern = r'\b[A-Z]{1,5}\b'
    matches = re.findall(pattern, message.upper())
    
    # Filter out common words that might match
    common_words = {'THE', 'AND', 'FOR', 'ARE', 'YOU', 'ALL', 'NEW', 'TOP'}
    symbols = [match for match in matches if match not in common_words]
    
    return symbols[0] if symbols else None

def calculate_confidence(response: str, financial_data: Optional[dict]) -> float:
    """
    Calculate confidence score for the response
    
    TODO: Implement more sophisticated confidence calculation
    - Analyze response quality indicators
    - Consider data availability and freshness
    - Factor in model uncertainty
    """
    base_confidence = 0.7
    
    if financial_data:
        base_confidence += 0.2
    
    # Simple heuristics for confidence adjustment
    if "I don't have enough information" in response.lower():
        base_confidence -= 0.3
    elif "based on the data" in response.lower():
        base_confidence += 0.1
    
    return min(max(base_confidence, 0.0), 1.0)

def get_data_sources(financial_data: Optional[dict], market_context: Optional[dict]) -> list[str]:
    """
    Get list of data sources used in the analysis
    """
    sources = []
    
    if financial_data:
        sources.extend(financial_data.get('sources', []))
    
    if market_context:
        sources.extend(market_context.get('sources', []))
    
    return list(set(sources))  # Remove duplicates 