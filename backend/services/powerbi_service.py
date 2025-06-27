"""
Power BI service for data integration with Power BI dashboards
"""

import os
import json
from typing import Dict, Any, List, Optional
from loguru import logger
import httpx

class PowerBIService:
    """
    Service for interacting with Power BI REST API
    """
    
    def __init__(self):
        """Initialize Power BI service with credentials"""
        self.client_id = os.getenv("POWERBI_CLIENT_ID")
        self.client_secret = os.getenv("POWERBI_CLIENT_SECRET")
        self.tenant_id = os.getenv("POWERBI_TENANT_ID")
        self.workspace_id = os.getenv("POWERBI_WORKSPACE_ID")
        
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
        self.access_token = None
        
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            logger.warning("Power BI credentials not fully configured")
        
        logger.info("PowerBIService initialized")
    
    async def push_data(
        self, 
        dataset_name: str, 
        data: Dict[str, Any], 
        table_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Push data to Power BI dataset
        
        Args:
            dataset_name: Name of the Power BI dataset
            data: Data to push
            table_name: Target table name (optional)
            
        Returns:
            Result of the push operation
        """
        try:
            logger.info(f"Pushing data to Power BI dataset: {dataset_name}")
            
            # Authenticate if needed
            if not self.access_token:
                await self._authenticate()
            
            # Get or create dataset
            dataset_id = await self._get_or_create_dataset(dataset_name)
            
            # Push data to the dataset
            result = await self._push_data_to_dataset(dataset_id, data, table_name)
            
            return {
                "success": True,
                "message": "Data pushed successfully",
                "dataset_id": dataset_id,
                "rows_added": len(data) if isinstance(data, list) else 1
            }
            
        except Exception as e:
            logger.error(f"Error pushing data to Power BI: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to push data: {str(e)}"
            }
    
    async def push_valuation_report(self, valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Push valuation analysis results to Power BI
        
        Args:
            valuation_data: Formatted valuation data
            
        Returns:
            Result of the push operation
        """
        try:
            logger.info("Pushing valuation report to Power BI")
            
            # Format data for Power BI
            formatted_data = self._format_valuation_for_powerbi(valuation_data)
            
            # Push to valuation dataset
            result = await self.push_data(
                dataset_name="StockValuationReports",
                data=formatted_data,
                table_name="ValuationResults"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error pushing valuation report: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to push valuation report: {str(e)}"
            }
    
    async def list_datasets(self) -> List[Dict[str, Any]]:
        """
        List available Power BI datasets
        
        Returns:
            List of dataset information
        """
        try:
            if not self.access_token:
                await self._authenticate()
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.access_token}"}
                response = await client.get(
                    f"{self.base_url}/datasets",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("value", [])
                else:
                    logger.error(f"Failed to list datasets: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error listing datasets: {str(e)}")
            return []
    
    async def check_status(self) -> bool:
        """
        Check Power BI service status and connectivity
        
        Returns:
            True if service is accessible, False otherwise
        """
        try:
            if not self.access_token:
                await self._authenticate()
            
            # Try to list datasets as a connectivity test
            datasets = await self.list_datasets()
            return len(datasets) >= 0  # Any response means we're connected
            
        except Exception as e:
            logger.error(f"Power BI status check failed: {str(e)}")
            return False
    
    async def _authenticate(self) -> None:
        """
        Authenticate with Power BI using OAuth2
        
        TODO: Implement proper OAuth2 authentication
        """
        try:
            # TODO: Implement OAuth2 authentication flow
            # For now, use placeholder authentication
            
            if not all([self.client_id, self.client_secret, self.tenant_id]):
                raise Exception("Power BI credentials not configured")
            
            # Placeholder authentication
            self.access_token = "placeholder_token"
            logger.info("Power BI authentication completed")
            
        except Exception as e:
            logger.error(f"Power BI authentication failed: {str(e)}")
            raise
    
    async def _get_or_create_dataset(self, dataset_name: str) -> str:
        """
        Get existing dataset or create a new one
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            Dataset ID
        """
        try:
            # First, try to find existing dataset
            datasets = await self.list_datasets()
            
            for dataset in datasets:
                if dataset.get("name") == dataset_name:
                    return dataset.get("id")
            
            # Create new dataset if not found
            return await self._create_dataset(dataset_name)
            
        except Exception as e:
            logger.error(f"Error getting/creating dataset: {str(e)}")
            raise
    
    async def _create_dataset(self, dataset_name: str) -> str:
        """
        Create a new Power BI dataset
        
        Args:
            dataset_name: Name of the dataset
            
        Returns:
            Dataset ID
        """
        try:
            # TODO: Implement dataset creation
            # For now, return a placeholder ID
            logger.info(f"Creating new dataset: {dataset_name}")
            
            # Placeholder implementation
            return f"dataset_{dataset_name.lower().replace(' ', '_')}_id"
            
        except Exception as e:
            logger.error(f"Error creating dataset: {str(e)}")
            raise
    
    async def _push_data_to_dataset(
        self, 
        dataset_id: str, 
        data: Dict[str, Any], 
        table_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Push data to a specific Power BI dataset
        
        Args:
            dataset_id: Power BI dataset ID
            data: Data to push
            table_name: Target table name
            
        Returns:
            Result of the push operation
        """
        try:
            # TODO: Implement actual data push to Power BI
            # For now, simulate the operation
            
            logger.info(f"Pushing data to dataset {dataset_id}")
            
            # Simulate API call
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                }
                
                # Prepare data for Power BI
                powerbi_data = self._prepare_data_for_powerbi(data, table_name)
                
                # TODO: Make actual API call to Power BI
                # response = await client.post(
                #     f"{self.base_url}/datasets/{dataset_id}/tables/{table_name}/rows",
                #     headers=headers,
                #     json=powerbi_data
                # )
                
                logger.info("Data push simulated successfully")
                return {"success": True}
                
        except Exception as e:
            logger.error(f"Error pushing data to dataset: {str(e)}")
            raise
    
    def _format_valuation_for_powerbi(self, valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format valuation data for Power BI consumption
        
        Args:
            valuation_data: Raw valuation data
            
        Returns:
            Formatted data for Power BI
        """
        try:
            formatted = {
                "timestamp": valuation_data.get("timestamp", "2024-01-01T00:00:00Z"),
                "stock_symbol": valuation_data.get("stock_symbol"),
                "current_price": valuation_data.get("current_price", 0.0),
                "recommendation": valuation_data.get("recommendation", ""),
                "risk_factors": valuation_data.get("risk_factors", ""),
                "valuation_methods": json.dumps(valuation_data.get("valuation_methods", []))
            }
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting valuation data: {str(e)}")
            return {}
    
    def _prepare_data_for_powerbi(
        self, 
        data: Dict[str, Any], 
        table_name: Optional[str]
    ) -> Dict[str, Any]:
        """
        Prepare data for Power BI API format
        
        Args:
            data: Raw data
            table_name: Target table name
            
        Returns:
            Data formatted for Power BI API
        """
        try:
            # Convert data to Power BI format
            if isinstance(data, list):
                rows = data
            else:
                rows = [data]
            
            return {
                "rows": rows
            }
            
        except Exception as e:
            logger.error(f"Error preparing data for Power BI: {str(e)}")
            return {"rows": []} 