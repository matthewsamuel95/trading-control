"""
Business Analyst Agent - Concrete Implementation
Implements fundamental analysis capabilities with proper observability
"""

from __future__ import annotations

import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from agent.agent_contract import (
    AgentInfo,
    AgentResult,
    AgentTask,
    AgentTaskStatus,
    AgentType,
    BaseAgent,
)


class BusinessAnalystAgent(BaseAgent):
    """Business analysis agent implementation"""

    def __init__(self, agent_id: str, observability_client=None):
        super().__init__(agent_id, AgentType.BUSINESS_ANALYST, "Business Analyst")
        self._fundamental_metrics = {
            "pe_ratio": self._calculate_pe_ratio,
            "debt_to_equity": self._calculate_debt_to_equity,
            "roe": self._calculate_roe,
            "revenue_growth": self._calculate_revenue_growth,
            "profit_margin": self._calculate_profit_margin,
            "market_cap": self._calculate_market_cap,
            "dividend_yield": self._calculate_dividend_yield,
        }

    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute business analysis task"""
        start_time = datetime.now()

        try:
            # Add task to current tasks
            self._add_task(task)

            # Extract task data
            symbol = task.input_data.get("symbol")
            financial_data = task.input_data.get("financial_data", {})
            metrics = task.input_data.get("metrics", [])

            # Validate inputs
            if not symbol:
                raise ValueError("Symbol is required")

            # Execute analysis
            if task.task_type == "analyze_fundamentals":
                result_data = await self._analyze_fundamentals(
                    symbol, financial_data, metrics
                )
            elif task.task_type == "valuation":
                result_data = await self._perform_valuation(
                    symbol, financial_data, metrics
                )
            elif task.task_type == "industry_comparison":
                result_data = await self._compare_industry(
                    symbol, financial_data, metrics
                )
            elif task.task_type == "growth_analysis":
                result_data = await self._analyze_growth(
                    symbol, financial_data, metrics
                )
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Create result
            result = AgentResult(
                task_id=task.task_id,
                status=AgentTaskStatus.COMPLETED,
                output_data=result_data,
                error_message=None,
                metrics={
                    "metrics_analyzed": len(metrics),
                    "data_points": len(financial_data),
                    "analysis_type": task.task_type,
                },
                trace_id=None,  # Will be set by observability layer
                tokens_used=self._estimate_tokens_used(result_data),
                cost_usd=self._estimate_cost(result_data),
                execution_time_ms=execution_time,
                started_at=start_time,
                completed_at=datetime.now(),
            )

            # Update metrics
            self._update_metrics(result)

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Create error result
            result = AgentResult(
                task_id=task.task_id,
                status=AgentTaskStatus.FAILED,
                output_data=None,
                error_message=str(e),
                metrics={"error_type": type(e).__name__},
                trace_id=None,
                tokens_used=0,
                cost_usd=0.0,
                execution_time_ms=execution_time,
                started_at=start_time,
                completed_at=datetime.now(),
            )

            # Update metrics
            self._update_metrics(result)

            return result
        finally:
            # Remove task from current tasks
            self._remove_task(task.task_id)

    def get_agent_info(self) -> AgentInfo:
        """Get agent metadata for registration"""
        return AgentInfo(
            agent_id=self.agent_id,
            agent_type=AgentType.BUSINESS_ANALYST,
            name="Business Analyst Agent",
            description="Performs fundamental analysis and business valuation",
            version="1.0.0",
            capabilities=[
                "fundamental_analysis",
                "financial_ratios",
                "valuation_models",
                "industry_comparison",
                "growth_analysis",
                "risk_assessment",
                "earnings_analysis",
                "market_positioning",
            ],
            supported_task_types=[
                "analyze_fundamentals",
                "valuation",
                "industry_comparison",
                "growth_analysis",
            ],
            max_concurrent_tasks=3,
            timeout_seconds=600,
        )

    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types"""
        return [
            "analyze_fundamentals",
            "valuation",
            "industry_comparison",
            "growth_analysis",
        ]

    async def _analyze_fundamentals(
        self, symbol: str, financial_data: Dict[str, Any], metrics: List[str]
    ) -> Dict[str, Any]:
        """Perform comprehensive fundamental analysis"""
        analysis = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "metrics": {},
            "summary": {},
            "recommendations": [],
            "risk_factors": [],
        }

        # Calculate requested metrics
        for metric in metrics:
            if metric in self._fundamental_metrics:
                try:
                    metric_result = self._fundamental_metrics[metric](financial_data)
                    analysis["metrics"][metric] = metric_result
                except Exception as e:
                    analysis["metrics"][metric] = {"error": str(e)}

        # Generate summary
        analysis["summary"] = self._generate_fundamental_summary(analysis["metrics"])

        # Generate recommendations
        analysis["recommendations"] = self._generate_fundamental_recommendations(
            analysis["metrics"]
        )

        # Identify risk factors
        analysis["risk_factors"] = self._identify_fundamental_risks(analysis["metrics"])

        return analysis

    async def _perform_valuation(
        self, symbol: str, financial_data: Dict[str, Any], metrics: List[str]
    ) -> Dict[str, Any]:
        """Perform business valuation"""
        fundamentals = await self._analyze_fundamentals(symbol, financial_data, metrics)

        valuation = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "valuation_methods": {},
            "fair_value_range": {},
            "confidence_score": 0.0,
            "recommendation": "",
            "sensitivity_analysis": {},
        }

        # DCF valuation
        dcf_result = self._calculate_dcf_valuation(financial_data)
        valuation["valuation_methods"]["dcf"] = dcf_result

        # P/E valuation
        pe_result = self._calculate_pe_valuation(
            financial_data, fundamentals["metrics"]
        )
        valuation["valuation_methods"]["pe"] = pe_result

        # Book value valuation
        book_result = self._calculate_book_value_valuation(financial_data)
        valuation["valuation_methods"]["book_value"] = book_result

        # Calculate fair value range
        valuations = [
            v.get("fair_value", 0)
            for v in valuation["valuation_methods"].values()
            if "fair_value" in v
        ]
        if valuations:
            valuation["fair_value_range"] = {
                "min": min(valuations),
                "max": max(valuations),
                "median": sum(valuations) / len(valuations),
            }

        # Calculate confidence score
        valuation["confidence_score"] = self._calculate_valuation_confidence(
            valuation["valuation_methods"]
        )

        # Generate recommendation
        valuation["recommendation"] = self._generate_valuation_recommendation(valuation)

        return valuation

    async def _compare_industry(
        self, symbol: str, financial_data: Dict[str, Any], metrics: List[str]
    ) -> Dict[str, Any]:
        """Compare with industry averages"""
        fundamentals = await self._analyze_fundamentals(symbol, financial_data, metrics)

        comparison = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "industry": financial_data.get("industry", "Unknown"),
            "company_metrics": fundamentals["metrics"],
            "industry_averages": self._get_industry_averages(
                financial_data.get("industry")
            ),
            "comparisons": {},
            "competitive_position": "",
            "outlook": "",
        }

        # Perform comparisons
        industry_avgs = comparison["industry_averages"]
        for metric in metrics:
            if metric in fundamentals["metrics"] and metric in industry_avgs:
                company_val = fundamentals["metrics"][metric]
                industry_val = industry_avgs[metric]

                if isinstance(company_val, (int, float)) and isinstance(
                    industry_val, (int, float)
                ):
                    if industry_val != 0:
                        ratio = company_val / industry_val
                        comparison["comparisons"][metric] = {
                            "company_value": company_val,
                            "industry_average": industry_val,
                            "ratio": ratio,
                            "percentile": self._calculate_percentile(ratio),
                        }

        # Determine competitive position
        comparison["competitive_position"] = self._determine_competitive_position(
            comparison["comparisons"]
        )

        # Generate outlook
        comparison["outlook"] = self._generate_industry_outlook(
            comparison["comparisons"]
        )

        return comparison

    async def _analyze_growth(
        self, symbol: str, financial_data: Dict[str, Any], metrics: List[str]
    ) -> Dict[str, Any]:
        """Analyze growth prospects"""
        fundamentals = await self._analyze_fundamentals(symbol, financial_data, metrics)

        growth_analysis = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "growth_metrics": {},
            "growth_trends": {},
            "projections": {},
            "growth_quality": "",
            "recommendations": [],
        }

        # Calculate growth metrics
        growth_metrics = self._calculate_growth_metrics(financial_data)
        growth_analysis["growth_metrics"] = growth_metrics

        # Analyze growth trends
        growth_analysis["growth_trends"] = self._analyze_growth_trends(growth_metrics)

        # Generate projections
        growth_analysis["projections"] = self._generate_growth_projections(
            growth_metrics
        )

        # Assess growth quality
        growth_analysis["growth_quality"] = self._assess_growth_quality(growth_metrics)

        # Generate recommendations
        growth_analysis["recommendations"] = self._generate_growth_recommendations(
            growth_metrics
        )

        return growth_analysis

    def _calculate_pe_ratio(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate P/E ratio"""
        market_cap = financial_data.get("market_cap", 0)
        net_income = financial_data.get("net_income", 0)
        shares_outstanding = financial_data.get("shares_outstanding", 0)

        if shares_outstanding == 0:
            return {"error": "Shares outstanding data not available"}

        # Calculate current price (market cap / shares)
        current_price = market_cap / shares_outstanding

        # Calculate EPS
        eps = net_income / shares_outstanding if shares_outstanding > 0 else 0

        if eps == 0:
            return {"error": "EPS is zero, cannot calculate P/E ratio"}

        pe_ratio = current_price / eps

        return {
            "pe_ratio": round(pe_ratio, 2),
            "current_price": round(current_price, 2),
            "eps": round(eps, 2),
            "interpretation": self._interpret_pe_ratio(pe_ratio),
        }

    def _calculate_debt_to_equity(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate debt-to-equity ratio"""
        total_debt = financial_data.get("total_debt", 0)
        total_equity = financial_data.get("total_equity", 0)

        if total_equity == 0:
            return {
                "error": "Total equity is zero, cannot calculate debt-to-equity ratio"
            }

        debt_to_equity = total_debt / total_equity

        return {
            "debt_to_equity": round(debt_to_equity, 2),
            "total_debt": total_debt,
            "total_equity": total_equity,
            "interpretation": self._interpret_debt_to_equity(debt_to_equity),
        }

    def _calculate_roe(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Return on Equity"""
        net_income = financial_data.get("net_income", 0)
        total_equity = financial_data.get("total_equity", 0)

        if total_equity == 0:
            return {"error": "Total equity is zero, cannot calculate ROE"}

        roe = (net_income / total_equity) * 100

        return {
            "roe": round(roe, 2),
            "net_income": net_income,
            "total_equity": total_equity,
            "interpretation": self._interpret_roe(roe),
        }

    def _calculate_revenue_growth(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate revenue growth rate"""
        current_revenue = financial_data.get("revenue", 0)
        previous_revenue = financial_data.get("previous_revenue", 0)

        if previous_revenue == 0:
            return {"error": "Previous revenue is zero, cannot calculate growth rate"}

        growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100

        return {
            "revenue_growth": round(growth_rate, 2),
            "current_revenue": current_revenue,
            "previous_revenue": previous_revenue,
            "interpretation": self._interpret_growth_rate(growth_rate),
        }

    def _calculate_profit_margin(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate profit margin"""
        net_income = financial_data.get("net_income", 0)
        revenue = financial_data.get("revenue", 0)

        if revenue == 0:
            return {"error": "Revenue is zero, cannot calculate profit margin"}

        profit_margin = (net_income / revenue) * 100

        return {
            "profit_margin": round(profit_margin, 2),
            "net_income": net_income,
            "revenue": revenue,
            "interpretation": self._interpret_profit_margin(profit_margin),
        }

    def _calculate_market_cap(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market capitalization"""
        shares_outstanding = financial_data.get("shares_outstanding", 0)
        current_price = financial_data.get("current_price", 0)

        market_cap = shares_outstanding * current_price

        return {
            "market_cap": market_cap,
            "shares_outstanding": shares_outstanding,
            "current_price": current_price,
            "market_cap_category": self._categorize_market_cap(market_cap),
        }

    def _calculate_dividend_yield(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate dividend yield"""
        annual_dividend = financial_data.get("annual_dividend", 0)
        current_price = financial_data.get("current_price", 0)

        if current_price == 0:
            return {"error": "Current price is zero, cannot calculate dividend yield"}

        dividend_yield = (annual_dividend / current_price) * 100

        return {
            "dividend_yield": round(dividend_yield, 2),
            "annual_dividend": annual_dividend,
            "current_price": current_price,
            "interpretation": self._interpret_dividend_yield(dividend_yield),
        }

    def _interpret_pe_ratio(self, pe_ratio: float) -> str:
        """Interpret P/E ratio"""
        if pe_ratio < 0:
            return "Negative earnings"
        elif pe_ratio < 15:
            return "Low P/E - potentially undervalued"
        elif pe_ratio < 25:
            return "Normal P/E"
        elif pe_ratio < 40:
            return "High P/E - potentially overvalued"
        else:
            return "Very high P/E - likely overvalued"

    def _interpret_debt_to_equity(self, debt_to_equity: float) -> str:
        """Interpret debt-to-equity ratio"""
        if debt_to_equity < 0.5:
            return "Low debt - strong financial position"
        elif debt_to_equity < 1.0:
            return "Moderate debt - acceptable leverage"
        elif debt_to_equity < 2.0:
            return "High debt - concerning leverage"
        else:
            return "Very high debt - risky financial position"

    def _interpret_roe(self, roe: float) -> str:
        """Interpret Return on Equity"""
        if roe < 0:
            return "Negative ROE - losses"
        elif roe < 10:
            return "Low ROE - poor profitability"
        elif roe < 15:
            return "Average ROE"
        elif roe < 20:
            return "Good ROE - strong profitability"
        else:
            return "Excellent ROE - exceptional profitability"

    def _interpret_growth_rate(self, growth_rate: float) -> str:
        """Interpret growth rate"""
        if growth_rate < 0:
            return "Negative growth - declining business"
        elif growth_rate < 5:
            return "Low growth - stagnant business"
        elif growth_rate < 15:
            return "Moderate growth - healthy business"
        elif growth_rate < 25:
            return "High growth - expanding business"
        else:
            return "Very high growth - rapidly expanding"

    def _interpret_profit_margin(self, profit_margin: float) -> str:
        """Interpret profit margin"""
        if profit_margin < 0:
            return "Negative margin - losses"
        elif profit_margin < 5:
            return "Low margin - thin profitability"
        elif profit_margin < 15:
            return "Average margin - reasonable profitability"
        elif profit_margin < 25:
            return "Good margin - strong profitability"
        else:
            return "Excellent margin - exceptional profitability"

    def _interpret_dividend_yield(self, dividend_yield: float) -> str:
        """Interpret dividend yield"""
        if dividend_yield == 0:
            return "No dividend - growth company"
        elif dividend_yield < 2:
            return "Low yield - growth focused"
        elif dividend_yield < 4:
            return "Average yield - balanced"
        elif dividend_yield < 6:
            return "High yield - income focused"
        else:
            return "Very high yield - income stock"

    def _categorize_market_cap(self, market_cap: float) -> str:
        """Categorize market capitalization"""
        if market_cap < 2e9:  # < $2B
            return "Small Cap"
        elif market_cap < 10e9:  # < $10B
            return "Mid Cap"
        elif market_cap < 200e9:  # < $200B
            return "Large Cap"
        else:
            return "Mega Cap"

    def _generate_fundamental_summary(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fundamental analysis summary"""
        summary = {
            "overall_health": "neutral",
            "strengths": [],
            "weaknesses": [],
            "key_insights": [],
        }

        # Analyze P/E ratio
        if "pe_ratio" in metrics:
            pe_interpretation = metrics["pe_ratio"].get("interpretation", "")
            if "undervalued" in pe_interpretation:
                summary["strengths"].append("Attractive valuation")
            elif "overvalued" in pe_interpretation:
                summary["weaknesses"].append("Expensive valuation")

        # Analyze ROE
        if "roe" in metrics:
            roe_interpretation = metrics["roe"].get("interpretation", "")
            if "excellent" in roe_interpretation:
                summary["strengths"].append("Exceptional profitability")
            elif "poor" in roe_interpretation:
                summary["weaknesses"].append("Low profitability")

        # Analyze debt
        if "debt_to_equity" in metrics:
            debt_interpretation = metrics["debt_to_equity"].get("interpretation", "")
            if "strong" in debt_interpretation:
                summary["strengths"].append("Strong financial position")
            elif "risky" in debt_interpretation:
                summary["weaknesses"].append("High financial risk")

        # Determine overall health
        strengths_count = len(summary["strengths"])
        weaknesses_count = len(summary["weaknesses"])

        if strengths_count > weaknesses_count:
            summary["overall_health"] = "strong"
        elif weaknesses_count > strengths_count:
            summary["overall_health"] = "weak"
        else:
            summary["overall_health"] = "neutral"

        return summary

    def _generate_fundamental_recommendations(
        self, metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate fundamental analysis recommendations"""
        recommendations = []

        # P/E based recommendations
        if "pe_ratio" in metrics:
            pe_interpretation = metrics["pe_ratio"].get("interpretation", "")
            if "undervalued" in pe_interpretation:
                recommendations.append("Consider buying - attractive valuation")
            elif "overvalued" in pe_interpretation:
                recommendations.append("Consider waiting for better valuation")

        # ROE based recommendations
        if "roe" in metrics:
            roe_interpretation = metrics["roe"].get("interpretation", "")
            if "poor" in roe_interpretation:
                recommendations.append("Monitor profitability improvements")
            elif "exceptional" in roe_interpretation:
                recommendations.append("Strong profitability - consider investment")

        # Debt based recommendations
        if "debt_to_equity" in metrics:
            debt_interpretation = metrics["debt_to_equity"].get("interpretation", "")
            if "risky" in debt_interpretation:
                recommendations.append("High financial risk - monitor debt levels")
            elif "strong" in debt_interpretation:
                recommendations.append("Strong financial position - lower risk")

        return recommendations

    def _identify_fundamental_risks(self, metrics: Dict[str, Any]) -> List[str]:
        """Identify fundamental risk factors"""
        risks = []

        # High debt risk
        if "debt_to_equity" in metrics:
            debt_to_equity = metrics["debt_to_equity"].get("debt_to_equity", 0)
            if debt_to_equity > 2.0:
                risks.append("High debt-to-equity ratio")

        # Low profitability risk
        if "roe" in metrics:
            roe = metrics["roe"].get("roe", 0)
            if roe < 5:
                risks.append("Low return on equity")

        # Negative growth risk
        if "revenue_growth" in metrics:
            revenue_growth = metrics["revenue_growth"].get("revenue_growth", 0)
            if revenue_growth < 0:
                risks.append("Negative revenue growth")

        # Low margin risk
        if "profit_margin" in metrics:
            profit_margin = metrics["profit_margin"].get("profit_margin", 0)
            if profit_margin < 0:
                risks.append("Negative profit margin")
            elif profit_margin < 5:
                risks.append("Low profit margin")

        return risks

    def _calculate_dcf_valuation(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate DCF valuation (simplified)"""
        # Simplified DCF calculation
        current_fcf = financial_data.get("free_cash_flow", 0)
        growth_rate = financial_data.get("growth_rate", 0.05)
        discount_rate = 0.10  # 10% discount rate
        terminal_growth = 0.03  # 3% terminal growth

        # 5-year projection
        fcf_projections = []
        for year in range(1, 6):
            fcf = current_fcf * ((1 + growth_rate) ** year)
            fcf_projections.append(fcf)

        # Calculate present value
        pv_sum = 0
        for i, fcf in enumerate(fcf_projections):
            pv = fcf / ((1 + discount_rate) ** (i + 1))
            pv_sum += pv

        # Terminal value
        terminal_fcf = fcf_projections[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        terminal_pv = terminal_value / ((1 + discount_rate) ** 5)

        total_value = pv_sum + terminal_pv

        return {
            "method": "DCF",
            "fair_value": round(total_value, 2),
            "assumptions": {
                "growth_rate": growth_rate,
                "discount_rate": discount_rate,
                "terminal_growth": terminal_growth,
            },
            "projections": fcf_projections,
            "terminal_value": round(terminal_value, 2),
        }

    def _calculate_pe_valuation(
        self, financial_data: Dict[str, Any], company_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate P/E based valuation"""
        industry_pe = financial_data.get("industry_pe", 15)
        eps = company_metrics.get("pe_ratio", {}).get("eps", 0)

        if eps == 0:
            return {"error": "EPS is zero, cannot calculate P/E valuation"}

        fair_value = eps * industry_pe

        return {
            "method": "P/E",
            "fair_value": round(fair_value, 2),
            "industry_pe": industry_pe,
            "current_eps": eps,
        }

    def _calculate_book_value_valuation(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate book value based valuation"""
        book_value_per_share = financial_data.get("book_value_per_share", 0)
        price_to_book = financial_data.get("price_to_book", 1.5)

        if book_value_per_share == 0:
            return {"error": "Book value per share is zero"}

        fair_value = book_value_per_share * price_to_book

        return {
            "method": "Book Value",
            "fair_value": round(fair_value, 2),
            "book_value_per_share": book_value_per_share,
            "price_to_book": price_to_book,
        }

    def _calculate_valuation_confidence(self, valuations: Dict[str, Any]) -> float:
        """Calculate confidence score for valuation"""
        valuations_list = []
        for method, data in valuations.items():
            if "fair_value" in data:
                valuations_list.append(data["fair_value"])

        if len(valuations_list) < 2:
            return 0.5  # Low confidence with only one method

        # Calculate standard deviation
        mean_val = sum(valuations_list) / len(valuations_list)
        variance = sum((val - mean_val) ** 2 for val in valuations_list) / len(
            valuations_list
        )
        std_dev = variance**0.5

        # Lower standard deviation = higher confidence
        if mean_val == 0:
            return 0.5

        cv = std_dev / mean_val  # Coefficient of variation

        if cv < 0.1:
            return 0.9
        elif cv < 0.2:
            return 0.8
        elif cv < 0.3:
            return 0.7
        elif cv < 0.5:
            return 0.6
        else:
            return 0.4

    def _generate_valuation_recommendation(self, valuation: Dict[str, Any]) -> str:
        """Generate valuation recommendation"""
        confidence = valuation.get("confidence_score", 0.5)
        fair_value_range = valuation.get("fair_value_range", {})

        if not fair_value_range:
            return "hold"

        median_value = fair_value_range.get("median", 0)
        current_price = (
            valuation.get("valuation_methods", {})
            .get("dcf", {})
            .get("current_price", 0)
        )

        if current_price == 0:
            return "hold"

        # Calculate upside/downside
        upside = (median_value - current_price) / current_price * 100

        if confidence > 0.7 and upside > 20:
            return "strong_buy"
        elif confidence > 0.5 and upside > 10:
            return "buy"
        elif confidence > 0.5 and upside < -10:
            return "sell"
        elif upside < -20:
            return "strong_sell"
        else:
            return "hold"

    def _get_industry_averages(self, industry: str) -> Dict[str, float]:
        """Get industry average metrics"""
        # Simplified industry averages
        industry_averages = {
            "Technology": {
                "pe_ratio": 25.0,
                "roe": 18.0,
                "debt_to_equity": 0.4,
                "profit_margin": 15.0,
                "revenue_growth": 12.0,
            },
            "Healthcare": {
                "pe_ratio": 20.0,
                "roe": 15.0,
                "debt_to_equity": 0.6,
                "profit_margin": 12.0,
                "revenue_growth": 8.0,
            },
            "Financial": {
                "pe_ratio": 15.0,
                "roe": 12.0,
                "debt_to_equity": 1.2,
                "profit_margin": 10.0,
                "revenue_growth": 5.0,
            },
            "Industrial": {
                "pe_ratio": 18.0,
                "roe": 14.0,
                "debt_to_equity": 0.8,
                "profit_margin": 8.0,
                "revenue_growth": 6.0,
            },
        }

        return industry_averages.get(
            industry,
            {
                "pe_ratio": 20.0,
                "roe": 15.0,
                "debt_to_equity": 0.7,
                "profit_margin": 10.0,
                "revenue_growth": 8.0,
            },
        )

    def _calculate_percentile(self, ratio: float) -> str:
        """Calculate percentile based on ratio"""
        if ratio < 0.5:
            return "25th percentile"
        elif ratio < 0.8:
            return "50th percentile"
        elif ratio < 1.2:
            return "75th percentile"
        else:
            return "90th percentile"

    def _determine_competitive_position(self, comparisons: Dict[str, Any]) -> str:
        """Determine competitive position"""
        if not comparisons:
            return "insufficient_data"

        # Count superior metrics
        superior_count = 0
        total_count = len(comparisons)

        for metric, data in comparisons.items():
            if data.get("ratio", 1) > 1:
                superior_count += 1

        if superior_count / total_count > 0.7:
            return "leader"
        elif superior_count / total_count > 0.5:
            return "above_average"
        elif superior_count / total_count > 0.3:
            return "below_average"
        else:
            return "laggard"

    def _generate_industry_outlook(self, comparisons: Dict[str, Any]) -> str:
        """Generate industry outlook"""
        if not comparisons:
            return "neutral"

        # Calculate overall performance score
        total_ratio = sum(data.get("ratio", 1) for data in comparisons.values())
        avg_ratio = total_ratio / len(comparisons)

        if avg_ratio > 1.2:
            return "bullish"
        elif avg_ratio < 0.8:
            return "bearish"
        else:
            return "neutral"

    def _calculate_growth_metrics(
        self, financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate growth metrics"""
        metrics = {}

        # Revenue growth
        current_revenue = financial_data.get("revenue", 0)
        previous_revenue = financial_data.get("previous_revenue", 0)
        if previous_revenue > 0:
            metrics["revenue_growth"] = (
                (current_revenue - previous_revenue) / previous_revenue
            ) * 100

        # Earnings growth
        current_earnings = financial_data.get("net_income", 0)
        previous_earnings = financial_data.get("previous_net_income", 0)
        if previous_earnings > 0:
            metrics["earnings_growth"] = (
                (current_earnings - previous_earnings) / previous_earnings
            ) * 100

        # Historical growth rates
        metrics["historical_growth"] = financial_data.get("historical_growth_rates", [])

        return metrics

    def _analyze_growth_trends(self, growth_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze growth trends"""
        trends = {}

        # Current growth rates
        trends["current_revenue_growth"] = growth_metrics.get("revenue_growth", 0)
        trends["current_earnings_growth"] = growth_metrics.get("earnings_growth", 0)

        # Growth trend direction
        if trends["current_revenue_growth"] > 0:
            trends["revenue_trend"] = "growing"
        else:
            trends["revenue_trend"] = "declining"

        if trends["current_earnings_growth"] > 0:
            trends["earnings_trend"] = "growing"
        else:
            trends["earnings_trend"] = "declining"

        # Historical trend analysis
        historical_growth = growth_metrics.get("historical_growth", [])
        if len(historical_growth) >= 2:
            recent_growth = historical_growth[-2:]
            if recent_growth[-1] > recent_growth[-2]:
                trends["growth_acceleration"] = "accelerating"
            elif recent_growth[-1] < recent_growth[-2]:
                trends["growth_acceleration"] = "decelerating"
            else:
                trends["growth_acceleration"] = "stable"

        return trends

    def _generate_growth_projections(
        self, growth_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate growth projections"""
        projections = {}

        current_growth = growth_metrics.get("revenue_growth", 5.0)

        # 5-year projection
        projections["five_year_revenue_projection"] = []
        base_revenue = growth_metrics.get("current_revenue", 1000000)

        for year in range(1, 6):
            projected_revenue = base_revenue * ((1 + current_growth / 100) ** year)
            projections["five_year_revenue_projection"].append(
                {
                    "year": year,
                    "projected_revenue": round(projected_revenue, 2),
                    "growth_assumption": current_growth,
                }
            )

        # CAGR calculation
        if len(projections["five_year_revenue_projection"]) > 0:
            final_revenue = projections["five_year_revenue_projection"][-1][
                "projected_revenue"
            ]
            cagr = ((final_revenue / base_revenue) ** (1 / 5) - 1) * 100
            projections["cagr"] = round(cagr, 2)

        return projections

    def _assess_growth_quality(self, growth_metrics: Dict[str, Any]) -> str:
        """Assess growth quality"""
        revenue_growth = growth_metrics.get("revenue_growth", 0)
        earnings_growth = growth_metrics.get("earnings_growth", 0)

        # Check if earnings growth supports revenue growth
        if revenue_growth > 0 and earnings_growth > 0:
            if earnings_growth >= revenue_growth:
                return "high_quality"
            else:
                return "moderate_quality"
        elif revenue_growth > 0 and earnings_growth < 0:
            return "low_quality"
        else:
            return "declining"

    def _generate_growth_recommendations(
        self, growth_metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate growth recommendations"""
        recommendations = []

        revenue_growth = growth_metrics.get("revenue_growth", 0)
        earnings_growth = growth_metrics.get("earnings_growth", 0)

        if revenue_growth > 15:
            recommendations.append("High growth - monitor sustainability")
        elif revenue_growth < 0:
            recommendations.append(
                "Declining revenue - investigate turnaround strategy"
            )

        if earnings_growth > 20:
            recommendations.append(
                "Strong earnings growth - maintain operational efficiency"
            )
        elif earnings_growth < 0 and revenue_growth > 0:
            recommendations.append(
                "Revenue growth without earnings - improve profitability"
            )

        return recommendations

    def _estimate_tokens_used(self, result_data: Dict[str, Any]) -> int:
        """Estimate tokens used for the analysis"""
        import json

        text = json.dumps(result_data)
        return len(text.split())  # Rough word count

    def _estimate_cost(self, result_data: Dict[str, Any]) -> float:
        """Estimate cost in USD"""
        tokens = self._estimate_tokens_used(result_data)
        # Assume $0.002 per 1K tokens
        return (tokens / 1000) * 0.002
