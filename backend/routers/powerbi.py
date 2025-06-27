"""
Power BI router for data integration with Power BI dashboards
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from typing import Dict, Any

from models.schemas import PowerBIRequest, PowerBIResponse
from services.powerbi_service import PowerBIService

router = APIRouter()

# Initialize Power BI service
powerbi_service = PowerBIService()

@router.post("/powerbi/push", response_model=PowerBIResponse)
async def push_to_powerbi(request: PowerBIRequest):
    """
    Push data to Power BI dataset
    
    This endpoint sends financial data and analysis results to Power BI
    for visualization and dashboard updates.
    """
    try:
        logger.info(f"Pushing data to Power BI dataset: {request.dataset_name}")
        
        # Validate data format
        if not request.data:
            raise HTTPException(
                status_code=400,
                detail="Data cannot be empty"
            )
        
        # Push data to Power BI
        result = await powerbi_service.push_data(
            dataset_name=request.dataset_name,
            data=request.data,
            table_name=request.table_name
        )
        
        return PowerBIResponse(
            success=result['success'],
            message=result['message'],
            dataset_id=result.get('dataset_id'),
            rows_added=result.get('rows_added')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pushing data to Power BI: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to push data to Power BI: {str(e)}"
        )

@router.post("/powerbi/valuation-report")
async def push_valuation_report(valuation_data: Dict[str, Any]):
    """
    Push valuation analysis results to Power BI
    
    This endpoint formats and pushes comprehensive valuation reports
    including multiple valuation methods and recommendations.
    """
    try:
        logger.info("Pushing valuation report to Power BI")
        
        # Format valuation data for Power BI
        formatted_data = format_valuation_for_powerbi(valuation_data)
        
        # Push to Power BI
        result = await powerbi_service.push_valuation_report(formatted_data)
        
        return PowerBIResponse(
            success=result['success'],
            message=result['message'],
            dataset_id=result.get('dataset_id'),
            rows_added=result.get('rows_added')
        )
        
    except Exception as e:
        logger.error(f"Error pushing valuation report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to push valuation report: {str(e)}"
        )

@router.get("/powerbi/datasets")
async def list_datasets():
    """
    List available Power BI datasets
    
    TODO: Implement Power BI dataset listing
    """
    try:
        datasets = await powerbi_service.list_datasets()
        return {
            "datasets": datasets,
            "count": len(datasets)
        }
    except Exception as e:
        logger.error(f"Error listing Power BI datasets: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list datasets: {str(e)}"
        )

@router.get("/powerbi/status")
async def get_powerbi_status():
    """
    Check Power BI service status and connectivity
    """
    try:
        status = await powerbi_service.check_status()
        return {
            "status": "connected" if status else "disconnected",
            "service": "Power BI",
            "timestamp": "2024-01-01T00:00:00Z"  # TODO: Use actual timestamp
        }
    except Exception as e:
        logger.error(f"Error checking Power BI status: {str(e)}")
        return {
            "status": "error",
            "service": "Power BI",
            "error": str(e)
        }

def format_valuation_for_powerbi(valuation_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format valuation data for Power BI consumption
    
    TODO: Implement proper data formatting
    - Flatten nested structures
    - Convert to tabular format
    - Add metadata and timestamps
    """
    formatted = {
        "timestamp": "2024-01-01T00:00:00Z",  # TODO: Use actual timestamp
        "stock_symbol": valuation_data.get("stock_symbol"),
        "current_price": valuation_data.get("current_price"),
        "recommendation": valuation_data.get("recommendation"),
        "risk_factors": ", ".join(valuation_data.get("risk_factors", [])),
        "valuation_methods": []
    }
    
    # Format individual valuation methods
    for valuation in valuation_data.get("valuations", []):
        formatted["valuation_methods"].append({
            "method": valuation.get("method"),
            "estimated_value": valuation.get("estimated_value"),
            "confidence_lower": valuation.get("confidence_interval", [0, 0])[0],
            "confidence_upper": valuation.get("confidence_interval", [0, 0])[1]
        })
    
    return formatted 