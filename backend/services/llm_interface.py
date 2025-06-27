"""
LLM interface service for handling OpenAI GPT-4 calls
"""

import os
from typing import Dict, Any, Optional, List
from loguru import logger

# TODO: Import LangChain components when implementing
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import HumanMessage, SystemMessage

class LLMInterface:
    """
    Interface for communicating with OpenAI's GPT-4 model
    """
    
    def __init__(self):
        """Initialize LLM interface with OpenAI client"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        
        if not self.api_key:
            logger.warning("OpenAI API key not found in environment variables")
            self.client = None
        else:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
                logger.info(f"LLMInterface initialized with model: {self.model}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    async def generate_response(
        self,
        user_message: str,
        stock_symbol: Optional[str] = None,
        financial_data: Optional[Dict[str, Any]] = None,
        market_context: Optional[Dict[str, Any]] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a response using GPT-4 based on user query and financial data
        
        Args:
            user_message: User's question about stock valuation
            stock_symbol: Stock symbol being analyzed
            financial_data: Financial data for the stock
            market_context: Market and economic context
            additional_context: Any additional context
            
        Returns:
            Generated response from GPT-4
        """
        try:
            if not self.client:
                return "I'm sorry, but I'm currently unable to access the AI model. Please check your API configuration by setting the OPENAI_API_KEY environment variable."
            
            # Construct the prompt
            prompt = self._construct_prompt(
                user_message, stock_symbol, financial_data, market_context, additional_context
            )
            
            # Generate response using OpenAI
            response = await self._call_openai(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    async def analyze_valuation_data(
        self,
        stock_data: Dict[str, Any],
        valuation_results: List[Dict[str, Any]],
        market_context: Dict[str, Any]
    ) -> str:
        """
        Generate analysis of valuation results using LLM
        
        Args:
            stock_data: Stock information and metrics
            valuation_results: Results from different valuation methods
            market_context: Market context and economic indicators
            
        Returns:
            Analysis of the valuation results
        """
        try:
            if not self.client:
                return "Unable to generate valuation analysis. Please configure your OpenAI API key."
            
            prompt = self._construct_valuation_analysis_prompt(
                stock_data, valuation_results, market_context
            )
            
            response = await self._call_openai(prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error analyzing valuation data: {str(e)}")
            return "Unable to generate valuation analysis at this time."
    
    async def extract_stock_symbol(self, message: str) -> Optional[str]:
        """
        Extract stock symbol from user message using LLM
        
        Args:
            message: User's message
            
        Returns:
            Extracted stock symbol or None
        """
        try:
            if not self.client:
                # Fallback to simple regex extraction
                return self._extract_stock_symbol_simple(message)
            
            prompt = f"""
            Extract the stock symbol from the following message. 
            Return only the stock symbol (1-5 uppercase letters) or 'NONE' if no stock symbol is found.
            
            Message: {message}
            
            Stock symbol:"""
            
            response = await self._call_openai(prompt)
            
            # Clean up response
            symbol = response.strip().upper()
            if symbol == "NONE" or len(symbol) > 5:
                return None
            
            return symbol
            
        except Exception as e:
            logger.error(f"Error extracting stock symbol: {str(e)}")
            return self._extract_stock_symbol_simple(message)
    
    def _extract_stock_symbol_simple(self, message: str) -> Optional[str]:
        """
        Simple regex-based stock symbol extraction as fallback
        """
        import re
        pattern = r'\b[A-Z]{1,5}\b'
        matches = re.findall(pattern, message.upper())
        
        # Filter out common words that might match
        common_words = {'THE', 'AND', 'FOR', 'ARE', 'YOU', 'ALL', 'NEW', 'TOP'}
        symbols = [match for match in matches if match not in common_words]
        
        return symbols[0] if symbols else None
    
    def _construct_prompt(
        self,
        user_message: str,
        stock_symbol: Optional[str],
        financial_data: Optional[Dict[str, Any]],
        market_context: Optional[Dict[str, Any]],
        additional_context: Optional[Dict[str, Any]]
    ) -> str:
        """
        Construct a comprehensive prompt for the LLM
        """
        system_prompt = """You are an expert financial analyst specializing in stock valuation. 
        You provide clear, accurate, and helpful responses about stock analysis and valuation.
        
        Guidelines:
        - Be precise and professional in your analysis
        - Use financial data when available to support your conclusions
        - Explain complex concepts in simple terms
        - Always mention limitations and uncertainties in your analysis
        - Provide actionable insights when possible
        - Cite data sources when relevant"""
        
        context_parts = []
        
        if stock_symbol:
            context_parts.append(f"Stock Symbol: {stock_symbol}")
        
        if financial_data:
            context_parts.append("Financial Data:")
            context_parts.append(f"- Current Price: ${financial_data.get('current_price', 'N/A')}")
            context_parts.append(f"- Market Cap: ${financial_data.get('market_cap', 'N/A'):,.0f}" if financial_data.get('market_cap') else "- Market Cap: N/A")
            context_parts.append(f"- P/E Ratio: {financial_data.get('pe_ratio', 'N/A')}")
            context_parts.append(f"- PEG Ratio: {financial_data.get('peg_ratio', 'N/A')}")
            context_parts.append(f"- Sector: {financial_data.get('sector', 'N/A')}")
            context_parts.append(f"- Industry: {financial_data.get('industry', 'N/A')}")
        
        if market_context:
            context_parts.append("Market Context:")
            if market_context.get('economic_indicators'):
                indicators = market_context['economic_indicators']
                context_parts.append(f"- GDP Growth: {indicators.get('gdp_growth', 'N/A')}%")
                context_parts.append(f"- Unemployment Rate: {indicators.get('unemployment_rate', 'N/A')}%")
                context_parts.append(f"- Inflation Rate: {indicators.get('inflation_rate', 'N/A')}%")
                context_parts.append(f"- Fed Funds Rate: {indicators.get('fed_funds_rate', 'N/A')}%")
        
        if additional_context:
            context_parts.append("Additional Context:")
            for key, value in additional_context.items():
                context_parts.append(f"- {key}: {value}")
        
        context = "\n".join(context_parts) if context_parts else "No additional context available."
        
        full_prompt = f"""{system_prompt}

Context:
{context}

User Question: {user_message}

Please provide a comprehensive and helpful response:"""
        
        return full_prompt
    
    def _construct_valuation_analysis_prompt(
        self,
        stock_data: Dict[str, Any],
        valuation_results: List[Dict[str, Any]],
        market_context: Dict[str, Any]
    ) -> str:
        """
        Construct prompt for valuation analysis
        """
        system_prompt = """You are an expert financial analyst. Analyze the provided valuation results 
        and provide a comprehensive summary with insights and recommendations."""
        
        # Format valuation results
        valuation_summary = []
        for result in valuation_results:
            method = result.get('method', 'Unknown')
            estimated_value = result.get('estimated_value', 0)
            confidence_interval = result.get('confidence_interval', [0, 0])
            
            valuation_summary.append(f"""
{method.upper()} Valuation:
- Estimated Value: ${estimated_value:.2f}
- Confidence Interval: ${confidence_interval[0]:.2f} - ${confidence_interval[1]:.2f}
- Assumptions: {result.get('assumptions', {})}""")
        
        prompt = f"""{system_prompt}

Stock Information:
- Symbol: {stock_data.get('symbol', 'N/A')}
- Company: {stock_data.get('company_name', 'N/A')}
- Current Price: ${stock_data.get('current_price', 'N/A')}
- Sector: {stock_data.get('sector', 'N/A')}

Valuation Results:
{chr(10).join(valuation_summary)}

Market Context:
- Market Volatility: {market_context.get('market_volatility', 'N/A')}
- Economic Indicators: {market_context.get('economic_indicators', {})}

Please provide a comprehensive analysis including:
1. Summary of valuation results
2. Comparison between different methods
3. Key factors influencing the valuations
4. Investment recommendation
5. Risk considerations"""
        
        return prompt
    
    async def _call_openai(self, prompt: str) -> str:
        """
        Make API call to OpenAI
        """
        try:
            if not self.client:
                raise Exception("OpenAI client not initialized")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful financial analyst assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for more consistent financial analysis
                top_p=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    async def validate_financial_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean financial data using LLM
        
        TODO: Implement data validation logic
        """
        try:
            # TODO: Implement comprehensive data validation
            # - Check for missing critical fields
            # - Validate data ranges
            # - Flag potential data quality issues
            
            validation_result = {
                "is_valid": True,
                "issues": [],
                "confidence": 0.9
            }
            
            # Basic validation checks
            if not data.get('current_price') or data['current_price'] <= 0:
                validation_result["is_valid"] = False
                validation_result["issues"].append("Invalid or missing current price")
            
            if not data.get('market_cap') or data['market_cap'] <= 0:
                validation_result["issues"].append("Missing market capitalization")
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating financial data: {str(e)}")
            return {"is_valid": False, "issues": [str(e)], "confidence": 0.0} 