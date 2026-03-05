"""
Technical Analyst Agent - Concrete Implementation
Implements technical analysis capabilities with proper observability
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
from utils import safe_decimal, validate_symbol


class TechnicalAnalystAgent(BaseAgent):
    """Technical analysis agent implementation"""

    def __init__(self, agent_id: str, observability_client=None):
        super().__init__(agent_id, AgentType.TECHNICAL_ANALYST, "Technical Analyst")
        self._technical_indicators = {
            "rsi": self._calculate_rsi,
            "macd": self._calculate_macd,
            "bollinger": self._calculate_bollinger_bands,
            "moving_average": self._calculate_moving_average,
            "volume_analysis": self._analyze_volume,
        }

    def get_capabilities(self) -> List[str]:
        """Get list of supported task types"""
        return [
            "analyze_symbol",
            "generate_signal",
            "risk_assessment",
            "calculate_rsi",
            "calculate_macd",
            "calculate_bollinger_bands",
            "calculate_moving_average",
            "analyze_volume",
        ]

    def can_handle_task(self, task: AgentTask) -> bool:
        """Check if agent can handle the given task"""
        return task.task_type in self.get_capabilities()

    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute technical analysis task"""
        start_time = datetime.now()

        try:
            # Add task to current tasks
            self._add_task(task)

            # Extract task data
            symbol = task.input_data.get("symbol")
            price_data = task.input_data.get("price_data", {})
            indicators = task.input_data.get("indicators", [])

            # Validate inputs
            if not symbol:
                raise ValueError("Symbol is required")

            symbol = validate_symbol(symbol)

            # Execute analysis
            if task.task_type == "analyze_symbol":
                result_data = await self._analyze_symbol(symbol, price_data, indicators)
            elif task.task_type == "generate_signal":
                result_data = await self._generate_trading_signal(
                    symbol, price_data, indicators
                )
            elif task.task_type == "risk_assessment":
                result_data = await self._assess_risk(symbol, price_data, indicators)
            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")

            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Create result
            result = AgentResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                success=True,
                output_data=result_data,
                confidence=0.85,
                execution_time_ms=int(execution_time),
                metadata={
                    "indicators_calculated": len(indicators),
                    "data_points": len(price_data.get("prices", [])),
                    "analysis_type": task.task_type,
                },
            )

            # Update metrics
            self._update_metrics(result)

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Create error result
            result = AgentResult(
                task_id=task.task_id,
                agent_id=self.agent_id,
                success=False,
                output_data={},
                confidence=0.0,
                execution_time_ms=int(execution_time),
                error_message=str(e),
                metadata={"error_type": type(e).__name__},
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
            agent_type=AgentType.TECHNICAL_ANALYST,
            name="Technical Analyst Agent",
            description="Performs technical analysis on financial instruments using various indicators",
            version="1.0.0",
            capabilities=[
                "rsi_analysis",
                "macd_analysis",
                "bollinger_bands",
                "moving_averages",
                "volume_analysis",
                "trend_analysis",
                "support_resistance",
                "signal_generation",
            ],
            supported_task_types=[
                "analyze_symbol",
                "generate_signal",
                "risk_assessment",
            ],
            max_concurrent_tasks=5,
            timeout_seconds=300,
        )

    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types"""
        return ["analyze_symbol", "generate_signal", "risk_assessment"]

    async def _analyze_symbol(
        self, symbol: str, price_data: Dict[str, Any], indicators: List[str]
    ) -> Dict[str, Any]:
        """Perform comprehensive technical analysis"""
        analysis = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "indicators": {},
            "summary": {},
            "recommendations": [],
        }

        # Calculate requested indicators
        for indicator in indicators:
            if indicator in self._technical_indicators:
                try:
                    indicator_result = self._technical_indicators[indicator](price_data)
                    analysis["indicators"][indicator] = indicator_result
                except Exception as e:
                    analysis["indicators"][indicator] = {"error": str(e)}

        # Generate summary
        analysis["summary"] = self._generate_analysis_summary(analysis["indicators"])

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(
            analysis["indicators"]
        )

        return analysis

    async def _generate_trading_signal(
        self, symbol: str, price_data: Dict[str, Any], indicators: List[str]
    ) -> Dict[str, Any]:
        """Generate trading signal"""
        # First perform analysis
        analysis = await self._analyze_symbol(symbol, price_data, indicators)

        # Generate signal based on analysis
        signal = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "signal": self._determine_signal(analysis["indicators"]),
            "confidence": self._calculate_confidence(analysis["indicators"]),
            "action": self._recommend_action(analysis["indicators"]),
            "price_targets": self._calculate_price_targets(
                analysis["indicators"], price_data
            ),
            "risk_level": self._assess_signal_risk(analysis["indicators"]),
            "reasoning": self._generate_signal_reasoning(analysis["indicators"]),
        }

        return signal

    async def _assess_risk(
        self, symbol: str, price_data: Dict[str, Any], indicators: List[str]
    ) -> Dict[str, Any]:
        """Assess risk for the symbol"""
        analysis = await self._analyze_symbol(symbol, price_data, indicators)

        risk_assessment = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "risk_score": self._calculate_risk_score(analysis["indicators"]),
            "risk_factors": self._identify_risk_factors(analysis["indicators"]),
            "volatility": self._calculate_volatility(price_data),
            "liquidity": self._assess_liquidity(price_data),
            "recommendations": self._generate_risk_recommendations(
                analysis["indicators"]
            ),
        }

        return risk_assessment

    def _calculate_rsi(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate RSI indicator"""
        prices = price_data.get("prices", [])
        if len(prices) < 14:
            return {"error": "Insufficient data for RSI calculation"}

        # Simple RSI calculation (simplified)
        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        avg_gain = sum(gains[-14:]) / 14 if len(gains) >= 14 else 0
        avg_loss = sum(losses[-14:]) / 14 if len(losses) >= 14 else 0

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        return {
            "rsi": round(rsi, 2),
            "signal": (
                "overbought" if rsi > 70 else "oversold" if rsi < 30 else "neutral"
            ),
            "period": 14,
        }

    def _calculate_macd(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate MACD indicator"""
        prices = price_data.get("prices", [])
        if len(prices) < 26:
            return {"error": "Insufficient data for MACD calculation"}

        # Simplified MACD calculation
        ema_12 = sum(prices[-12:]) / 12
        ema_26 = sum(prices[-26:]) / 26
        macd_line = ema_12 - ema_26
        signal_line = macd_line * 0.9  # Simplified signal line
        histogram = macd_line - signal_line

        return {
            "macd": round(macd_line, 4),
            "signal": round(signal_line, 4),
            "histogram": round(histogram, 4),
            "signal_type": "bullish" if histogram > 0 else "bearish",
        }

    def _calculate_bollinger_bands(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate Bollinger Bands"""
        prices = price_data.get("prices", [])
        if len(prices) < 20:
            return {"error": "Insufficient data for Bollinger Bands"}

        recent_prices = prices[-20:]
        sma = sum(recent_prices) / len(recent_prices)
        variance = sum((price - sma) ** 2 for price in recent_prices) / len(
            recent_prices
        )
        std_dev = variance**0.5

        upper_band = sma + (2 * std_dev)
        lower_band = sma - (2 * std_dev)

        current_price = prices[-1]
        position = (
            "above_upper"
            if current_price > upper_band
            else "below_lower" if current_price < lower_band else "between"
        )

        return {
            "upper_band": round(upper_band, 4),
            "middle_band": round(sma, 4),
            "lower_band": round(lower_band, 4),
            "current_position": position,
            "bandwidth": round((upper_band - lower_band) / sma * 100, 2),
        }

    def _calculate_moving_average(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate moving averages"""
        prices = price_data.get("prices", [])

        mas = {}
        periods = [5, 10, 20, 50]

        for period in periods:
            if len(prices) >= period:
                ma = sum(prices[-period:]) / period
                mas[f"ma_{period}"] = round(ma, 4)

        # Determine trend
        if "ma_5" in mas and "ma_20" in mas:
            trend = "bullish" if mas["ma_5"] > mas["ma_20"] else "bearish"
            mas["trend"] = trend

        return mas

    def _analyze_volume(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze volume patterns"""
        volumes = price_data.get("volumes", [])
        prices = price_data.get("prices", [])

        if not volumes or len(volumes) < 10:
            return {"error": "Insufficient volume data"}

        avg_volume = sum(volumes[-10:]) / 10
        current_volume = volumes[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

        # Volume-price analysis
        price_change = 0
        if len(prices) >= 2:
            price_change = (prices[-1] - prices[-2]) / prices[-2] * 100

        volume_signal = (
            "confirming"
            if (
                (price_change > 0 and volume_ratio > 1.2)
                or (price_change < 0 and volume_ratio > 1.2)
            )
            else "diverging"
        )

        return {
            "current_volume": current_volume,
            "average_volume": round(avg_volume, 2),
            "volume_ratio": round(volume_ratio, 2),
            "volume_signal": volume_signal,
            "trend": "increasing" if current_volume > avg_volume else "decreasing",
        }

    def _generate_analysis_summary(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary from indicators"""
        summary = {
            "overall_sentiment": "neutral",
            "key_signals": [],
            "trend": "sideways",
            "volatility": "normal",
        }

        # Analyze RSI
        if "rsi" in indicators and "signal" in indicators["rsi"]:
            rsi_signal = indicators["rsi"]["signal"]
            if rsi_signal == "overbought":
                summary["key_signals"].append("RSI indicates overbought conditions")
                summary["overall_sentiment"] = "bearish"
            elif rsi_signal == "oversold":
                summary["key_signals"].append("RSI indicates oversold conditions")
                summary["overall_sentiment"] = "bullish"

        # Analyze MACD
        if "macd" in indicators and "signal_type" in indicators["macd"]:
            macd_signal = indicators["macd"]["signal_type"]
            summary["key_signals"].append(f"MACD shows {macd_signal} momentum")
            if macd_signal == "bullish" and summary["overall_sentiment"] == "neutral":
                summary["overall_sentiment"] = "bullish"
            elif macd_signal == "bearish" and summary["overall_sentiment"] == "neutral":
                summary["overall_sentiment"] = "bearish"

        # Analyze moving averages
        if "trend" in indicators.get("moving_average", {}):
            trend = indicators["moving_average"]["trend"]
            summary["trend"] = trend
            summary["key_signals"].append(f"Moving averages show {trend} trend")

        return summary

    def _generate_recommendations(self, indicators: Dict[str, Any]) -> List[str]:
        """Generate trading recommendations"""
        recommendations = []

        # RSI-based recommendations
        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            if rsi > 70:
                recommendations.append(
                    "Consider taking profits - RSI indicates overbought"
                )
            elif rsi < 30:
                recommendations.append(
                    "Consider buying opportunity - RSI indicates oversold"
                )

        # MACD-based recommendations
        if "macd" in indicators:
            signal_type = indicators["macd"].get("signal_type")
            if signal_type == "bullish":
                recommendations.append(
                    "MACD suggests bullish momentum - consider long positions"
                )
            elif signal_type == "bearish":
                recommendations.append(
                    "MACD suggests bearish momentum - consider short positions"
                )

        # Bollinger Bands recommendations
        if "bollinger" in indicators:
            position = indicators["bollinger"].get("current_position")
            if position == "above_upper":
                recommendations.append(
                    "Price above upper Bollinger Band - potential reversal"
                )
            elif position == "below_lower":
                recommendations.append(
                    "Price below lower Bollinger Band - potential bounce"
                )

        return recommendations

    def _determine_signal(self, indicators: Dict[str, Any]) -> str:
        """Determine overall trading signal"""
        bullish_signals = 0
        bearish_signals = 0

        # Count signals from indicators
        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            if rsi < 30:
                bullish_signals += 1
            elif rsi > 70:
                bearish_signals += 1

        if "macd" in indicators:
            signal_type = indicators["macd"].get("signal_type")
            if signal_type == "bullish":
                bullish_signals += 1
            elif signal_type == "bearish":
                bearish_signals += 1

        if "moving_average" in indicators:
            trend = indicators["moving_average"].get("trend")
            if trend == "bullish":
                bullish_signals += 1
            elif trend == "bearish":
                bearish_signals += 1

        # Determine overall signal
        if bullish_signals > bearish_signals:
            return "bullish"
        elif bearish_signals > bullish_signals:
            return "bearish"
        else:
            return "neutral"

    def _calculate_confidence(self, indicators: Dict[str, Any]) -> float:
        """Calculate confidence level for signal"""
        confidence = 0.5  # Base confidence

        # Increase confidence based on indicator agreement
        total_indicators = len(indicators)
        if total_indicators > 0:
            agreement_bonus = min(0.3, total_indicators * 0.1)
            confidence += agreement_bonus

        # Adjust based on data quality
        if "rsi" in indicators and "error" not in indicators["rsi"]:
            confidence += 0.1

        if "macd" in indicators and "error" not in indicators["macd"]:
            confidence += 0.1

        return min(1.0, confidence)

    def _recommend_action(self, indicators: Dict[str, Any]) -> str:
        """Recommend trading action"""
        signal = self._determine_signal(indicators)

        if signal == "bullish":
            return "buy"
        elif signal == "bearish":
            return "sell"
        else:
            return "hold"

    def _calculate_price_targets(
        self, indicators: Dict[str, Any], price_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate price targets"""
        prices = price_data.get("prices", [])
        if not prices:
            return {"error": "No price data available"}

        current_price = prices[-1]

        # Simple target calculation (2% and 5%)
        targets = {
            "current_price": current_price,
            "stop_loss": current_price * 0.98,  # 2% below
            "target_1": current_price * 1.02,  # 2% above
            "target_2": current_price * 1.05,  # 5% above
        }

        # Adjust based on volatility
        if "bollinger" in indicators:
            bandwidth = indicators["bollinger"].get("bandwidth", 0)
            if bandwidth > 4:  # High volatility
                targets["stop_loss"] = current_price * 0.96  # Tighter stop
                targets["target_2"] = current_price * 1.08  # Higher target

        return targets

    def _assess_signal_risk(self, indicators: Dict[str, Any]) -> str:
        """Assess risk level of signal"""
        risk_score = 0

        # RSI risk assessment
        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            if rsi > 80 or rsi < 20:
                risk_score += 2  # Extreme RSI levels
            elif rsi > 70 or rsi < 30:
                risk_score += 1  # Overbought/oversold

        # MACD risk assessment
        if "macd" in indicators:
            histogram = indicators["macd"].get("histogram", 0)
            if abs(histogram) > 0.01:
                risk_score += 1  # Strong momentum

        # Determine risk level
        if risk_score >= 3:
            return "high"
        elif risk_score >= 1:
            return "medium"
        else:
            return "low"

    def _generate_signal_reasoning(self, indicators: Dict[str, Any]) -> str:
        """Generate reasoning for signal"""
        reasons = []

        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            signal = indicators["rsi"].get("signal", "neutral")
            reasons.append(f"RSI at {rsi:.1f} indicates {signal} conditions")

        if "macd" in indicators:
            signal_type = indicators["macd"].get("signal_type")
            reasons.append(f"MACD shows {signal_type} momentum")

        if "moving_average" in indicators:
            trend = indicators["moving_average"].get("trend", "sideways")
            reasons.append(f"Moving averages show {trend} trend")

        if "bollinger" in indicators:
            position = indicators["bollinger"].get("current_position")
            reasons.append(f"Price is {position} Bollinger Bands")

        return "; ".join(reasons)

    def _estimate_tokens_used(self, result_data: Dict[str, Any]) -> int:
        """Estimate tokens used for the analysis"""
        # Rough estimation based on output size
        import json

        text = json.dumps(result_data)
        return len(text.split())  # Rough word count

    def _estimate_cost(self, result_data: Dict[str, Any]) -> float:
        """Estimate cost in USD"""
        tokens = self._estimate_tokens_used(result_data)
        # Assume $0.002 per 1K tokens
        return (tokens / 1000) * 0.002

    def _calculate_risk_score(self, indicators: Dict[str, Any]) -> float:
        """Calculate overall risk score"""
        risk_score = 0.5  # Base risk

        # Adjust based on volatility
        if "bollinger" in indicators:
            bandwidth = indicators["bollinger"].get("bandwidth", 0)
            if bandwidth > 4:
                risk_score += 0.2
            elif bandwidth > 2:
                risk_score += 0.1

        # Adjust based on RSI extremes
        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            if rsi > 80 or rsi < 20:
                risk_score += 0.2
            elif rsi > 70 or rsi < 30:
                risk_score += 0.1

        return min(1.0, risk_score)

    def _identify_risk_factors(self, indicators: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors"""
        factors = []

        if "rsi" in indicators:
            rsi = indicators["rsi"].get("rsi", 50)
            if rsi > 80:
                factors.append("Extremely overbought RSI")
            elif rsi < 20:
                factors.append("Extremely oversold RSI")

        if "bollinger" in indicators:
            position = indicators["bollinger"].get("current_position")
            if position == "above_upper":
                factors.append("Price above upper Bollinger Band")
            elif position == "below_lower":
                factors.append("Price below lower Bollinger Band")

        if "volume" in indicators:
            volume_signal = indicators["volume"].get("volume_signal")
            if volume_signal == "diverging":
                factors.append("Volume diverging from price action")

        return factors

    def _calculate_volatility(self, price_data: Dict[str, Any]) -> float:
        """Calculate volatility"""
        prices = price_data.get("prices", [])
        if len(prices) < 2:
            return 0.0

        # Simple volatility calculation
        returns = []
        for i in range(1, len(prices)):
            ret = (prices[i] - prices[i - 1]) / prices[i - 1]
            returns.append(ret)

        if not returns:
            return 0.0

        mean_return = sum(returns) / len(returns)
        variance = sum((ret - mean_return) ** 2 for ret in returns) / len(returns)
        volatility = variance**0.5

        return volatility

    def _assess_liquidity(self, price_data: Dict[str, Any]) -> str:
        """Assess liquidity"""
        volumes = price_data.get("volumes", [])
        if not volumes:
            return "unknown"

        avg_volume = (
            sum(volumes[-20:]) / 20
            if len(volumes) >= 20
            else sum(volumes) / len(volumes)
        )
        current_volume = volumes[-1]

        if current_volume > avg_volume * 2:
            return "high"
        elif current_volume < avg_volume * 0.5:
            return "low"
        else:
            return "normal"

    def _generate_risk_recommendations(self, indicators: Dict[str, Any]) -> List[str]:
        """Generate risk management recommendations"""
        recommendations = []

        risk_score = self._calculate_risk_score(indicators)

        if risk_score > 0.7:
            recommendations.append(
                "High risk detected - consider reducing position size"
            )
            recommendations.append("Use tight stop-loss orders")
        elif risk_score > 0.5:
            recommendations.append("Moderate risk - monitor closely")

        if "bollinger" in indicators:
            position = indicators["bollinger"].get("current_position")
            if position == "above_upper":
                recommendations.append("Consider taking partial profits")
            elif position == "below_lower":
                recommendations.append("Wait for confirmation before entering")

        return recommendations
