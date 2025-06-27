"""
Valuation engine service containing DCF, PEG, and P/E valuation logic
"""

import numpy as np
from typing import Dict, Any, Optional, Tuple
from loguru import logger
from datetime import datetime

from models.schemas import ValuationResult, ValuationMethod

class ValuationEngine:
    """
    Engine for performing various stock valuation methods
    """
    
    def __init__(self):
        """Initialize valuation engine"""
        logger.info("ValuationEngine initialized")
    
    async def dcf_valuation(
        self, 
        stock_data: Dict[str, Any], 
        market_context: Dict[str, Any],
        assumptions: Optional[Dict[str, Any]] = None
    ) -> ValuationResult:
        """
        Perform Discounted Cash Flow (DCF) valuation
        
        DCF values a stock based on the present value of its future cash flows.
        This is one of the most comprehensive valuation methods.
        """
        try:
            logger.info("Performing DCF valuation")
            
            # Extract required data
            free_cash_flow = stock_data.get('free_cash_flow', 0)
            current_price = stock_data.get('current_price', 0)
            
            # Get assumptions or use defaults
            growth_rate = assumptions.get('growth_rate', 0.05) if assumptions else 0.05
            discount_rate = assumptions.get('discount_rate', 0.10) if assumptions else 0.10
            terminal_growth = assumptions.get('terminal_growth', 0.02) if assumptions else 0.02
            projection_years = assumptions.get('projection_years', 5) if assumptions else 5
            
            # Calculate projected cash flows
            projected_cash_flows = self._project_cash_flows(
                free_cash_flow, growth_rate, projection_years
            )
            
            # Calculate terminal value
            terminal_value = self._calculate_terminal_value(
                projected_cash_flows[-1], terminal_growth, discount_rate
            )
            
            # Discount all cash flows to present value
            present_value_cash_flows = self._discount_cash_flows(
                projected_cash_flows, discount_rate
            )
            present_value_terminal = terminal_value / ((1 + discount_rate) ** projection_years)
            
            # Calculate total enterprise value
            enterprise_value = sum(present_value_cash_flows) + present_value_terminal
            
            # Adjust for debt and cash to get equity value
            debt = stock_data.get('total_debt', 0)
            cash = stock_data.get('total_cash', 0)
            equity_value = enterprise_value - debt + cash
            
            # Calculate per-share value
            shares_outstanding = stock_data.get('shares_outstanding', 1)
            estimated_value = equity_value / shares_outstanding if shares_outstanding > 0 else equity_value
            
            # Calculate confidence interval
            confidence_interval = self._calculate_dcf_confidence_interval(
                estimated_value, growth_rate, discount_rate
            )
            
            return ValuationResult(
                method=ValuationMethod.DCF,
                estimated_value=estimated_value,
                confidence_interval=confidence_interval,
                assumptions={
                    "growth_rate": growth_rate,
                    "discount_rate": discount_rate,
                    "terminal_growth": terminal_growth,
                    "projection_years": projection_years
                },
                calculation_details={
                    "free_cash_flow": free_cash_flow,
                    "enterprise_value": enterprise_value,
                    "equity_value": equity_value,
                    "projected_cash_flows": projected_cash_flows,
                    "terminal_value": terminal_value
                }
            )
            
        except Exception as e:
            logger.error(f"Error in DCF valuation: {str(e)}")
            raise
    
    async def peg_valuation(
        self, 
        stock_data: Dict[str, Any], 
        market_context: Dict[str, Any],
        assumptions: Optional[Dict[str, Any]] = None
    ) -> ValuationResult:
        """
        Perform Price/Earnings to Growth (PEG) valuation
        
        PEG ratio compares a stock's P/E ratio to its earnings growth rate.
        A PEG ratio of 1.0 is considered fair value.
        """
        try:
            logger.info("Performing PEG valuation")
            
            # Extract required data
            pe_ratio = stock_data.get('pe_ratio')
            earnings_growth = stock_data.get('earnings_growth')
            current_price = stock_data.get('current_price', 0)
            
            if not pe_ratio or not earnings_growth:
                raise ValueError("P/E ratio and earnings growth rate required for PEG valuation")
            
            # Calculate PEG ratio
            peg_ratio = pe_ratio / (earnings_growth * 100)  # Convert growth to decimal
            
            # Calculate fair value based on PEG
            # If PEG = 1.0 is fair value, then fair P/E = growth rate
            fair_pe_ratio = earnings_growth * 100
            estimated_value = fair_pe_ratio * stock_data.get('eps', current_price / pe_ratio)
            
            # Calculate confidence interval
            confidence_interval = self._calculate_peg_confidence_interval(
                estimated_value, peg_ratio
            )
            
            return ValuationResult(
                method=ValuationMethod.PEG,
                estimated_value=estimated_value,
                confidence_interval=confidence_interval,
                assumptions={
                    "fair_peg_ratio": 1.0,
                    "growth_rate": earnings_growth
                },
                calculation_details={
                    "peg_ratio": peg_ratio,
                    "pe_ratio": pe_ratio,
                    "earnings_growth": earnings_growth,
                    "fair_pe_ratio": fair_pe_ratio
                }
            )
            
        except Exception as e:
            logger.error(f"Error in PEG valuation: {str(e)}")
            raise
    
    async def pe_valuation(
        self, 
        stock_data: Dict[str, Any], 
        market_context: Dict[str, Any],
        assumptions: Optional[Dict[str, Any]] = None
    ) -> ValuationResult:
        """
        Perform Price/Earnings (P/E) valuation
        
        P/E valuation compares a stock's P/E ratio to industry or market averages.
        """
        try:
            logger.info("Performing P/E valuation")
            
            # Extract required data
            current_pe = stock_data.get('pe_ratio')
            current_price = stock_data.get('current_price', 0)
            eps = stock_data.get('eps', current_price / current_pe if current_pe else 0)
            
            if not current_pe or not eps:
                raise ValueError("P/E ratio and EPS required for P/E valuation")
            
            # Get industry average P/E (placeholder)
            industry_pe = self._get_industry_pe_ratio(stock_data.get('sector', ''))
            
            # Calculate fair value based on industry P/E
            estimated_value = industry_pe * eps
            
            # Calculate confidence interval
            confidence_interval = self._calculate_pe_confidence_interval(
                estimated_value, current_pe, industry_pe
            )
            
            return ValuationResult(
                method=ValuationMethod.PE,
                estimated_value=estimated_value,
                confidence_interval=confidence_interval,
                assumptions={
                    "industry_pe_ratio": industry_pe,
                    "valuation_method": "industry_comparison"
                },
                calculation_details={
                    "current_pe": current_pe,
                    "industry_pe": industry_pe,
                    "eps": eps,
                    "pe_difference": current_pe - industry_pe
                }
            )
            
        except Exception as e:
            logger.error(f"Error in P/E valuation: {str(e)}")
            raise
    
    async def comparative_valuation(
        self, 
        stock_data: Dict[str, Any], 
        market_context: Dict[str, Any],
        assumptions: Optional[Dict[str, Any]] = None
    ) -> ValuationResult:
        """
        Perform comparative valuation against peer companies
        
        TODO: Implement comprehensive comparative analysis
        """
        try:
            logger.info("Performing comparative valuation")
            
            # TODO: Implement peer company analysis
            # - Find similar companies in the same sector
            # - Compare multiple valuation multiples
            # - Calculate relative valuation
            
            # Placeholder implementation
            current_price = stock_data.get('current_price', 0)
            estimated_value = current_price * 1.1  # 10% premium for now
            
            return ValuationResult(
                method=ValuationMethod.COMPARATIVE,
                estimated_value=estimated_value,
                confidence_interval=(estimated_value * 0.8, estimated_value * 1.2),
                assumptions={
                    "peer_comparison": True,
                    "sector_average": True
                },
                calculation_details={
                    "method": "placeholder",
                    "note": "Comparative valuation not yet implemented"
                }
            )
            
        except Exception as e:
            logger.error(f"Error in comparative valuation: {str(e)}")
            raise
    
    def _project_cash_flows(
        self, 
        initial_fcf: float, 
        growth_rate: float, 
        years: int
    ) -> list[float]:
        """Project future cash flows based on growth rate"""
        cash_flows = []
        for year in range(1, years + 1):
            fcf = initial_fcf * ((1 + growth_rate) ** year)
            cash_flows.append(fcf)
        return cash_flows
    
    def _calculate_terminal_value(
        self, 
        final_fcf: float, 
        terminal_growth: float, 
        discount_rate: float
    ) -> float:
        """Calculate terminal value using Gordon Growth Model"""
        return final_fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
    
    def _discount_cash_flows(
        self, 
        cash_flows: list[float], 
        discount_rate: float
    ) -> list[float]:
        """Discount cash flows to present value"""
        return [cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cash_flows)]
    
    def _calculate_dcf_confidence_interval(
        self, 
        estimated_value: float, 
        growth_rate: float, 
        discount_rate: float
    ) -> Tuple[float, float]:
        """Calculate confidence interval for DCF valuation"""
        # Simple confidence interval based on input uncertainty
        growth_uncertainty = 0.02  # ±2% growth rate uncertainty
        discount_uncertainty = 0.02  # ±2% discount rate uncertainty
        
        lower_bound = estimated_value * 0.8
        upper_bound = estimated_value * 1.2
        
        return (lower_bound, upper_bound)
    
    def _calculate_peg_confidence_interval(
        self, 
        estimated_value: float, 
        peg_ratio: float
    ) -> Tuple[float, float]:
        """Calculate confidence interval for PEG valuation"""
        # Confidence based on how far PEG is from 1.0
        peg_deviation = abs(peg_ratio - 1.0)
        
        if peg_deviation < 0.2:
            confidence_range = 0.1  # ±10%
        elif peg_deviation < 0.5:
            confidence_range = 0.2  # ±20%
        else:
            confidence_range = 0.3  # ±30%
        
        return (
            estimated_value * (1 - confidence_range),
            estimated_value * (1 + confidence_range)
        )
    
    def _calculate_pe_confidence_interval(
        self, 
        estimated_value: float, 
        current_pe: float, 
        industry_pe: float
    ) -> Tuple[float, float]:
        """Calculate confidence interval for P/E valuation"""
        # Confidence based on how close current P/E is to industry P/E
        pe_deviation = abs(current_pe - industry_pe) / industry_pe
        
        if pe_deviation < 0.1:
            confidence_range = 0.1  # ±10%
        elif pe_deviation < 0.3:
            confidence_range = 0.2  # ±20%
        else:
            confidence_range = 0.3  # ±30%
        
        return (
            estimated_value * (1 - confidence_range),
            estimated_value * (1 + confidence_range)
        )
    
    def _get_industry_pe_ratio(self, sector: str) -> float:
        """Get industry average P/E ratio for a given sector"""
        # TODO: Implement industry P/E ratio lookup
        # For now, return placeholder values
        industry_pe_ratios = {
            "Technology": 25.0,
            "Healthcare": 20.0,
            "Finance": 15.0,
            "Energy": 12.0,
            "Consumer Cyclical": 18.0,
            "Consumer Defensive": 16.0,
            "Industrials": 17.0,
            "Basic Materials": 14.0,
            "Real Estate": 22.0,
            "Communication Services": 23.0,
            "Utilities": 19.0
        }
        
        return industry_pe_ratios.get(sector, 18.0)  # Default to 18.0 