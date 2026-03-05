"""
Sentiment Analyst Agent - Concrete Implementation
Implements sentiment analysis capabilities with proper observability
"""

from __future__ import annotations

import asyncio
import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

from agent.agent_contract import (
    AgentInfo,
    AgentResult,
    AgentTask,
    AgentTaskStatus,
    AgentType,
    BaseAgent,
)
from utils import validate_symbol


class SentimentAnalystAgent(BaseAgent):
    """Sentiment analysis agent implementation"""

    def __init__(self, agent_id: str, observability_client=None):
        super().__init__(agent_id, AgentType.SENTIMENT_ANALYST, "Sentiment Analyst")
        self._sentiment_indicators = {
            "news_sentiment": self._analyze_news_sentiment,
            "social_sentiment": self._analyze_social_sentiment,
            "market_sentiment": self._analyze_market_sentiment,
            "analyst_sentiment": self._analyze_analyst_sentiment,
            "volume_sentiment": self._analyze_volume_sentiment,
        }

        # Sentiment keywords
        self._positive_keywords = [
            "bullish",
            "buy",
            "strong",
            "excellent",
            "growth",
            "profit",
            "up",
            "outperform",
            "upgrade",
            "positive",
            "optimistic",
            "favorable",
            "beat",
            "exceed",
            "improve",
            "success",
            "opportunity",
            "good",
        ]

        self._negative_keywords = [
            "bearish",
            "sell",
            "weak",
            "poor",
            "decline",
            "loss",
            "down",
            "underperform",
            "downgrade",
            "negative",
            "pessimistic",
            "unfavorable",
            "miss",
            "fall",
            "decrease",
            "failure",
            "risk",
            "bad",
            "concern",
        ]

        self._neutral_keywords = [
            "hold",
            "neutral",
            "maintain",
            "stable",
            "unchanged",
            "steady",
            "mixed",
            "cautious",
            "wait",
            "monitor",
            "observe",
            "evaluate",
        ]

    async def execute_task(self, task: AgentTask) -> AgentResult:
        """Execute sentiment analysis task"""
        start_time = datetime.now()

        try:
            # Add task to current tasks
            self._add_task(task)

            # Extract task data
            symbol = task.input_data.get("symbol")
            text_data = task.input_data.get("text_data", {})
            sources = task.input_data.get("sources", [])

            # Validate inputs
            if not symbol:
                raise ValueError("Symbol is required")

            symbol = validate_symbol(symbol)

            # Execute analysis
            if task.task_type == "analyze_sentiment":
                result_data = await self._analyze_sentiment(symbol, text_data, sources)
            elif task.task_type == "social_media_sentiment":
                result_data = await self._analyze_social_media_sentiment(
                    symbol, text_data
                )
            elif task.task_type == "news_sentiment":
                result_data = await self._analyze_news_sentiment(symbol, text_data)
            elif task.task_type == "market_sentiment":
                result_data = await self._analyze_market_sentiment(symbol, text_data)
            elif task.task_type == "sentiment_summary":
                result_data = await self._generate_sentiment_summary(
                    symbol, text_data, sources
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
                    "sources_analyzed": len(sources),
                    "text_items": len(text_data),
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
            agent_type=AgentType.SENTIMENT_ANALYST,
            name="Sentiment Analyst Agent",
            description="Performs sentiment analysis on financial instruments using various data sources",
            version="1.0.0",
            capabilities=[
                "news_sentiment",
                "social_sentiment",
                "market_sentiment",
                "analyst_sentiment",
                "volume_sentiment",
                "text_classification",
                "trend_analysis",
                "sentiment_scoring",
            ],
            supported_task_types=[
                "analyze_sentiment",
                "social_media_sentiment",
                "news_sentiment",
                "market_sentiment",
                "sentiment_summary",
            ],
            max_concurrent_tasks=8,
            timeout_seconds=180,
        )

    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types"""
        return [
            "analyze_sentiment",
            "social_media_sentiment",
            "news_sentiment",
            "market_sentiment",
            "sentiment_summary",
        ]

    async def _analyze_sentiment(
        self, symbol: str, text_data: Dict[str, Any], sources: List[str]
    ) -> Dict[str, Any]:
        """Perform comprehensive sentiment analysis"""
        analysis = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "sentiment_scores": {},
            "overall_sentiment": "neutral",
            "confidence": 0.0,
            "sentiment_distribution": {},
            "key_insights": [],
            "recommendations": [],
        }

        # Analyze each source
        for source in sources:
            if source in text_data:
                source_data = text_data[source]
                if source in self._sentiment_indicators:
                    try:
                        source_analysis = self._sentiment_indicators[source](
                            source_data
                        )
                        analysis["sentiment_scores"][source] = source_analysis
                    except Exception as e:
                        analysis["sentiment_scores"][source] = {"error": str(e)}

        # Calculate overall sentiment
        if analysis["sentiment_scores"]:
            analysis["overall_sentiment"] = self._calculate_overall_sentiment(
                analysis["sentiment_scores"]
            )
            analysis["confidence"] = self._calculate_confidence(
                analysis["sentiment_scores"]
            )
            analysis["sentiment_distribution"] = self._calculate_sentiment_distribution(
                analysis["sentiment_scores"]
            )

        # Generate insights
        analysis["key_insights"] = self._generate_sentiment_insights(
            analysis["sentiment_scores"]
        )

        # Generate recommendations
        analysis["recommendations"] = self._generate_sentiment_recommendations(
            analysis["sentiment_scores"]
        )

        return analysis

    async def _analyze_news_sentiment(
        self, symbol: str, text_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze news sentiment"""
        news_articles = text_data.get("articles", [])

        if not news_articles:
            return {"error": "No news articles provided"}

        sentiment_scores = []
        article_sentiments = []

        for article in news_articles:
            title = article.get("title", "")
            content = article.get("content", "")
            full_text = f"{title} {content}"

            # Calculate sentiment score
            sentiment_score = self._calculate_text_sentiment(full_text)
            sentiment_scores.append(sentiment_score)

            # Classify sentiment
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            article_sentiments.append(
                {
                    "title": title,
                    "sentiment": sentiment,
                    "score": sentiment_score,
                    "confidence": abs(sentiment_score),
                }
            )

        # Calculate overall news sentiment
        if sentiment_scores:
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            overall_sentiment = self._classify_sentiment(avg_sentiment)
        else:
            avg_sentiment = 0
            overall_sentiment = "neutral"

        return {
            "source": "news",
            "overall_sentiment": overall_sentiment,
            "average_score": round(avg_sentiment, 3),
            "article_count": len(news_articles),
            "article_sentiments": article_sentiments,
            "sentiment_distribution": self._count_sentiments(article_sentiments),
            "key_topics": self._extract_key_topics(news_articles),
        }

    async def _analyze_social_sentiment(
        self, symbol: str, text_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze social media sentiment"""
        social_posts = text_data.get("posts", [])

        if not social_posts:
            return {"error": "No social media posts provided"}

        sentiment_scores = []
        post_sentiments = []

        for post in social_posts:
            content = post.get("content", "")
            author = post.get("author", "")
            timestamp = post.get("timestamp", "")

            # Calculate sentiment score
            sentiment_score = self._calculate_text_sentiment(content)
            sentiment_scores.append(sentiment_score)

            # Classify sentiment
            if sentiment_score > 0.1:
                sentiment = "positive"
            elif sentiment_score < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            post_sentiments.append(
                {
                    "author": author,
                    "content": content[:100] + "..." if len(content) > 100 else content,
                    "sentiment": sentiment,
                    "score": sentiment_score,
                    "timestamp": timestamp,
                }
            )

        # Calculate overall social sentiment
        if sentiment_scores:
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            overall_sentiment = self._classify_sentiment(avg_sentiment)
        else:
            avg_sentiment = 0
            overall_sentiment = "neutral"

        return {
            "source": "social_media",
            "overall_sentiment": overall_sentiment,
            "average_score": round(avg_sentiment, 3),
            "post_count": len(social_posts),
            "post_sentiments": post_sentiments,
            "sentiment_distribution": self._count_sentiments(post_sentiments),
            "engagement_metrics": self._calculate_engagement_metrics(social_posts),
            "influencer_sentiment": self._analyze_influencer_sentiment(post_sentiments),
        }

    async def _analyze_market_sentiment(
        self, symbol: str, text_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze market sentiment"""
        market_data = text_data.get("market_data", {})

        # Extract price action sentiment
        price_data = market_data.get("price_data", {})
        volume_data = market_data.get("volume_data", {})

        # Price-based sentiment
        price_sentiment = self._analyze_price_sentiment(price_data)

        # Volume-based sentiment
        volume_sentiment = self._analyze_volume_sentiment(volume_data)

        # Options data sentiment
        options_data = market_data.get("options_data", {})
        options_sentiment = self._analyze_options_sentiment(options_data)

        # Combine market sentiment indicators
        market_sentiments = {
            "price_sentiment": price_sentiment,
            "volume_sentiment": volume_sentiment,
            "options_sentiment": options_sentiment,
        }

        # Calculate overall market sentiment
        overall_sentiment = self._calculate_market_overall_sentiment(market_sentiments)

        return {
            "source": "market",
            "overall_sentiment": overall_sentiment,
            "market_indicators": market_sentiments,
            "confidence": self._calculate_market_confidence(market_sentiments),
            "technical_signals": self._extract_technical_signals(market_data),
            "market_momentum": self._calculate_market_momentum(market_data),
        }

    async def _analyze_social_media_sentiment(
        self, symbol: str, text_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze social media sentiment (alias for social_sentiment)"""
        return await self._analyze_social_sentiment(symbol, text_data)

    async def _generate_sentiment_summary(
        self, symbol: str, text_data: Dict[str, Any], sources: List[str]
    ) -> Dict[str, Any]:
        """Generate comprehensive sentiment summary"""
        # Get individual source analyses
        source_analyses = {}
        for source in sources:
            if source in text_data:
                if source == "news":
                    source_analyses["news"] = await self._analyze_news_sentiment(
                        symbol, text_data
                    )
                elif source in ["social", "social_media"]:
                    source_analyses["social"] = await self._analyze_social_sentiment(
                        symbol, text_data
                    )
                elif source == "market":
                    source_analyses["market"] = await self._analyze_market_sentiment(
                        symbol, text_data
                    )

        # Combine all analyses
        combined_analysis = await self._analyze_sentiment(symbol, text_data, sources)

        # Generate summary
        summary = {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "overall_sentiment": combined_analysis.get("overall_sentiment", "neutral"),
            "confidence": combined_analysis.get("confidence", 0.0),
            "source_analyses": source_analyses,
            "sentiment_trends": self._analyze_sentiment_trends(source_analyses),
            "consensus_score": self._calculate_consensus_score(source_analyses),
            "divergence_alerts": self._identify_divergence_alerts(source_analyses),
            "key_drivers": self._identify_key_sentiment_drivers(source_analyses),
            "recommendations": self._generate_comprehensive_recommendations(
                source_analyses
            ),
        }

        return summary

    def _calculate_text_sentiment(self, text: str) -> float:
        """Calculate sentiment score for text"""
        if not text:
            return 0.0

        # Convert to lowercase for analysis
        text_lower = text.lower()

        # Count sentiment keywords
        positive_count = sum(
            1 for word in self._positive_keywords if word in text_lower
        )
        negative_count = sum(
            1 for word in self._negative_keywords if word in text_lower
        )
        neutral_count = sum(1 for word in self._neutral_keywords if word in text_lower)

        # Calculate sentiment score
        total_words = positive_count + negative_count + neutral_count
        if total_words == 0:
            return 0.0

        # Weight positive and negative more heavily
        sentiment_score = (positive_count * 1.0 - negative_count * 1.0) / total_words

        # Normalize to [-1, 1] range
        return max(-1.0, min(1.0, sentiment_score))

    def _classify_sentiment(self, score: float) -> str:
        """Classify sentiment based on score"""
        if score > 0.1:
            return "positive"
        elif score < -0.1:
            return "negative"
        else:
            return "neutral"

    def _calculate_overall_sentiment(self, sentiment_scores: Dict[str, Any]) -> str:
        """Calculate overall sentiment from multiple sources"""
        scores = []

        for source, data in sentiment_scores.items():
            if isinstance(data, dict) and "average_score" in data:
                scores.append(data["average_score"])
            elif isinstance(data, dict) and "score" in data:
                scores.append(data["score"])

        if not scores:
            return "neutral"

        avg_score = sum(scores) / len(scores)
        return self._classify_sentiment(avg_score)

    def _calculate_confidence(self, sentiment_scores: Dict[str, Any]) -> float:
        """Calculate confidence in sentiment analysis"""
        if not sentiment_scores:
            return 0.0

        # Calculate confidence based on agreement between sources
        sentiments = []
        for source, data in sentiment_scores.items():
            if isinstance(data, dict):
                if "overall_sentiment" in data:
                    sentiments.append(data["overall_sentiment"])
                elif "sentiment" in data:
                    sentiments.append(data["sentiment"])

        if len(sentiments) <= 1:
            return 0.5

        # Calculate agreement
        sentiment_counts = Counter(sentiments)
        most_common_count = max(sentiment_counts.values())
        agreement = most_common_count / len(sentiments)

        return agreement

    def _calculate_sentiment_distribution(
        self, sentiment_scores: Dict[str, Any]
    ) -> Dict[str, int]:
        """Calculate sentiment distribution"""
        distribution = {"positive": 0, "negative": 0, "neutral": 0}

        for source, data in sentiment_scores.items():
            if isinstance(data, dict):
                if "sentiment_distribution" in data:
                    # Add distribution from source
                    source_dist = data["sentiment_distribution"]
                    for sentiment, count in source_dist.items():
                        distribution[sentiment] += count
                elif "overall_sentiment" in data:
                    distribution[data["overall_sentiment"]] += 1
                elif "sentiment" in data:
                    distribution[data["sentiment"]] += 1

        return distribution

    def _generate_sentiment_insights(
        self, sentiment_scores: Dict[str, Any]
    ) -> List[str]:
        """Generate insights from sentiment analysis"""
        insights = []

        # Check for strong consensus
        if len(sentiment_scores) > 1:
            sentiments = []
            for source, data in sentiment_scores.items():
                if isinstance(data, dict):
                    if "overall_sentiment" in data:
                        sentiments.append(data["overall_sentiment"])
                    elif "sentiment" in data:
                        sentiments.append(data["sentiment"])

            sentiment_counts = Counter(sentiments)
            most_common = sentiment_counts.most_common(1)[0]
            if sentiment_counts[most_common] > len(sentiments) * 0.7:
                insights.append(
                    f"Strong consensus: {most_common} sentiment across sources"
                )

        # Check for divergence
        if len(sentiment_scores) > 1:
            sentiments = []
            for source, data in sentiment_scores.items():
                if isinstance(data, dict):
                    if "overall_sentiment" in data:
                        sentiments.append(data["overall_sentiment"])
                    elif "sentiment" in data:
                        sentiments.append(data["sentiment"])

            unique_sentiments = set(sentiments)
            if len(unique_sentiments) > 2:
                insights.append("Divergent sentiment across sources - requires caution")

        # Check for extreme sentiment
        for source, data in sentiment_scores.items():
            if isinstance(data, dict):
                score = data.get("average_score", data.get("score", 0))
                if abs(score) > 0.7:
                    insights.append(
                        f"Extreme sentiment in {source}: {self._classify_sentiment(score)}"
                    )

        return insights

    def _generate_sentiment_recommendations(
        self, sentiment_scores: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on sentiment"""
        recommendations = []

        overall_sentiment = self._calculate_overall_sentiment(sentiment_scores)
        confidence = self._calculate_confidence(sentiment_scores)

        if overall_sentiment == "positive" and confidence > 0.7:
            recommendations.append(
                "Strong positive sentiment - consider bullish positions"
            )
        elif overall_sentiment == "negative" and confidence > 0.7:
            recommendations.append(
                "Strong negative sentiment - consider bearish positions"
            )
        elif overall_sentiment == "neutral":
            recommendations.append("Neutral sentiment - wait for clearer signals")

        if confidence < 0.5:
            recommendations.append("Low confidence in sentiment - monitor closely")

        return recommendations

    def _count_sentiments(self, sentiments: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count sentiment occurrences"""
        counts = {"positive": 0, "negative": 0, "neutral": 0}

        for sentiment_data in sentiments:
            sentiment = sentiment_data.get("sentiment", "neutral")
            counts[sentiment] += 1

        return counts

    def _extract_key_topics(self, articles: List[Dict[str, Any]]) -> List[str]:
        """Extract key topics from articles"""
        all_text = " ".join(
            [
                article.get("title", "") + " " + article.get("content", "")
                for article in articles
            ]
        )

        # Simple keyword extraction (in real implementation, use NLP)
        common_words = [
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
        ]
        words = all_text.lower().split()
        word_counts = Counter(
            word for word in words if word not in common_words and len(word) > 2
        )

        return [word for word, count in word_counts.most_common(10)]

    def _calculate_engagement_metrics(
        self, posts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate engagement metrics for social posts"""
        if not posts:
            return {}

        total_likes = sum(post.get("likes", 0) for post in posts)
        total_shares = sum(post.get("shares", 0) for post in posts)
        total_comments = sum(post.get("comments", 0) for post in posts)

        return {
            "total_likes": total_likes,
            "total_shares": total_shares,
            "total_comments": total_comments,
            "average_likes": total_likes / len(posts),
            "average_shares": total_shares / len(posts),
            "average_comments": total_comments / len(posts),
        }

    def _analyze_influencer_sentiment(
        self, posts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze sentiment from influential accounts"""
        # Filter posts from influential accounts (high engagement)
        avg_engagement = self._calculate_engagement_metrics(posts).get(
            "average_likes", 0
        )
        influencer_posts = [
            post for post in posts if post.get("likes", 0) > avg_engagement * 2
        ]

        if not influencer_posts:
            return {"message": "No influencer posts found"}

        influencer_sentiments = [
            post.get("sentiment", "neutral") for post in influencer_posts
        ]
        influencer_counts = Counter(influencer_sentiments)

        return {
            "influencer_count": len(influencer_posts),
            "influencer_sentiments": dict(influencer_counts),
            "influencer_consensus": influencer_counts.most_common(1)[0],
            "influencer_agreement": (
                influencer_counts.most_common(1)[1] / len(influencer_posts)
                if influencer_posts
                else 0
            ),
        }

    def _analyze_price_sentiment(self, price_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze price-based sentiment"""
        prices = price_data.get("prices", [])

        if len(prices) < 2:
            return {"error": "Insufficient price data"}

        # Calculate price changes
        price_changes = []
        for i in range(1, len(prices)):
            change = (prices[i] - prices[i - 1]) / prices[i - 1]
            price_changes.append(change)

        # Calculate moving averages
        short_ma = sum(prices[-5:]) / 5 if len(prices) >= 5 else prices[-1]
        long_ma = sum(prices[-20:]) / 20 if len(prices) >= 20 else prices[-1]

        # Determine sentiment
        current_price = prices[-1]
        if current_price > short_ma and short_ma > long_ma:
            sentiment = "bullish"
        elif current_price < short_ma and short_ma < long_ma:
            sentiment = "bearish"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "current_price": current_price,
            "short_ma": short_ma,
            "long_ma": long_ma,
            "price_changes": price_changes[-10:],  # Last 10 changes
            "volatility": self._calculate_volatility(price_changes),
        }

    def _analyze_volume_sentiment(self, volume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze volume-based sentiment"""
        volumes = volume_data.get("volumes", [])

        if len(volumes) < 2:
            return {"error": "Insufficient volume data"}

        avg_volume = (
            sum(volumes[-20:]) / 20
            if len(volumes) >= 20
            else sum(volumes) / len(volumes)
        )
        current_volume = volumes[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

        # Determine sentiment
        if volume_ratio > 1.5:
            sentiment = "bullish"  # High volume on price increase
        elif volume_ratio < 0.7:
            sentiment = "bearish"  # Low volume on price decrease
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "current_volume": current_volume,
            "average_volume": avg_volume,
            "volume_ratio": round(volume_ratio, 2),
            "volume_trend": (
                "increasing" if current_volume > avg_volume else "decreasing"
            ),
        }

    def _analyze_options_sentiment(
        self, options_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze options-based sentiment"""
        put_call_ratio = options_data.get("put_call_ratio", 1.0)
        implied_volatility = options_data.get("implied_volatility", 0.2)

        # Determine sentiment
        if put_call_ratio > 1.2:
            sentiment = "bearish"  # More puts than calls
        elif put_call_ratio < 0.8:
            sentiment = "bullish"  # More calls than puts
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "put_call_ratio": put_call_ratio,
            "implied_volatility": implied_volatility,
            "volatility_level": (
                "high"
                if implied_volatility > 0.3
                else "normal" if implied_volatility > 0.15 else "low"
            ),
        }

    def _calculate_market_overall_sentiment(
        self, market_sentiments: Dict[str, Any]
    ) -> str:
        """Calculate overall market sentiment"""
        sentiments = []

        for indicator, data in market_sentiments.items():
            if isinstance(data, dict) and "sentiment" in data:
                sentiments.append(data["sentiment"])

        if not sentiments:
            return "neutral"

        # Weight options sentiment more heavily
        weights = {
            "price_sentiment": 0.3,
            "volume_sentiment": 0.2,
            "options_sentiment": 0.5,
        }

        sentiment_scores = {"bullish": 1, "bearish": -1, "neutral": 0}

        weighted_score = 0
        total_weight = 0

        for indicator, data in market_sentiments.items():
            if indicator in weights and isinstance(data, dict) and "sentiment" in data:
                weight = weights[indicator]
                score = sentiment_scores.get(data["sentiment"], 0)
                weighted_score += weight * score
                total_weight += weight

        if total_weight == 0:
            return "neutral"

        avg_score = weighted_score / total_weight

        if avg_score > 0.2:
            return "bullish"
        elif avg_score < -0.2:
            return "bearish"
        else:
            return "neutral"

    def _calculate_market_confidence(self, market_sentiments: Dict[str, Any]) -> float:
        """Calculate confidence in market sentiment"""
        sentiments = []

        for indicator, data in market_sentiments.items():
            if isinstance(data, dict) and "sentiment" in data:
                sentiments.append(data["sentiment"])

        if len(sentiments) <= 1:
            return 0.5

        sentiment_counts = Counter(sentiments)
        most_common_count = sentiment_counts.most_common(1)[0]
        return most_common_count / len(sentiments)

    def _extract_technical_signals(self, market_data: Dict[str, Any]) -> List[str]:
        """Extract technical signals from market data"""
        signals = []

        price_data = market_data.get("price_data", {})
        if price_data:
            price_sentiment = self._analyze_price_sentiment(price_data)
            if price_sentiment.get("sentiment") == "bullish":
                signals.append("Price above moving averages")
            elif price_sentiment.get("sentiment") == "bearish":
                signals.append("Price below moving averages")

        volume_data = market_data.get("volume_data", {})
        if volume_data:
            volume_sentiment = self._analyze_volume_sentiment(volume_data)
            if volume_sentiment.get("sentiment") == "bullish":
                signals.append("Above average volume")
            elif volume_sentiment.get("sentiment") == "bearish":
                signals.append("Below average volume")

        return signals

    def _calculate_market_momentum(self, market_data: Dict[str, Any]) -> str:
        """Calculate market momentum"""
        price_data = market_data.get("price_data", {})
        prices = price_data.get("prices", [])

        if len(prices) < 10:
            return "insufficient_data"

        # Calculate momentum over last 10 periods
        momentum = (prices[-1] - prices[-10]) / prices[-10]

        if momentum > 0.05:
            return "strong_up"
        elif momentum > 0.02:
            return "up"
        elif momentum < -0.05:
            return "strong_down"
        elif momentum < -0.02:
            return "down"
        else:
            return "sideways"

    def _calculate_volatility(self, changes: List[float]) -> float:
        """Calculate volatility from price changes"""
        if len(changes) < 2:
            return 0.0

        mean_change = sum(changes) / len(changes)
        variance = sum((change - mean_change) ** 2 for change in changes) / len(changes)
        return variance**0.5

    def _analyze_sentiment_trends(
        self, source_analyses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze sentiment trends across sources"""
        trends = {}

        for source, analysis in source_analyses.items():
            if isinstance(analysis, dict):
                if "sentiment_distribution" in analysis:
                    dist = analysis["sentiment_distribution"]
                    total = sum(dist.values())
                    if total > 0:
                        trends[source] = {
                            "positive_pct": dist.get("positive", 0) / total * 100,
                            "negative_pct": dist.get("negative", 0) / total * 100,
                            "neutral_pct": dist.get("neutral", 0) / total * 100,
                        }

        return trends

    def _calculate_consensus_score(self, source_analyses: Dict[str, Any]) -> float:
        """Calculate consensus score across sources"""
        if len(source_analyses) <= 1:
            return 0.5

        sentiments = []
        for analysis in source_analyses.values():
            if isinstance(analysis, dict):
                if "overall_sentiment" in analysis:
                    sentiments.append(analysis["overall_sentiment"])
                elif "sentiment" in analysis:
                    sentiments.append(analysis["sentiment"])

        if not sentiments:
            return 0.5

        sentiment_counts = Counter(sentiments)
        most_common_count = sentiment_counts.most_common(1)[1]
        return most_common_count / len(sentiments)

    def _identify_divergence_alerts(self, source_analyses: Dict[str, Any]) -> List[str]:
        """Identify divergence alerts between sources"""
        alerts = []

        if len(source_analyses) < 2:
            return alerts

        sentiments = []
        for analysis in source_analyses.values():
            if isinstance(analysis, dict):
                if "overall_sentiment" in analysis:
                    sentiments.append(analysis["overall_sentiment"])
                elif "sentiment" in analysis:
                    sentiments.append(analysis["sentiment"])

        unique_sentiments = set(sentiments)
        if len(unique_sentiments) > 2:
            alerts.append("Multiple conflicting sentiments detected")

        # Check for extreme divergence
        if len(source_analyses) == 2:
            sentiment1 = list(source_analyses.values())[0].get(
                "overall_sentiment", "neutral"
            )
            sentiment2 = list(source_analyses.values())[1].get(
                "overall_sentiment", "neutral"
            )

            if (sentiment1 == "positive" and sentiment2 == "negative") or (
                sentiment1 == "negative" and sentiment2 == "positive"
            ):
                alerts.append("Direct sentiment conflict between sources")

        return alerts

    def _identify_key_sentiment_drivers(
        self, source_analyses: Dict[str, Any]
    ) -> List[str]:
        """Identify key drivers of sentiment"""
        drivers = []

        # Find most extreme sentiment
        extreme_source = None
        extreme_score = 0

        for source, analysis in source_analyses.items():
            if isinstance(analysis, dict):
                score = analysis.get("average_score", analysis.get("score", 0))
                if abs(score) > abs(extreme_score):
                    extreme_score = score
                    extreme_source = source

        if extreme_source and abs(extreme_score) > 0.5:
            drivers.append(
                f"{extreme_source} shows {self._classify_sentiment(extreme_score)} sentiment"
            )

        return drivers

    def _generate_comprehensive_recommendations(
        self, source_analyses: Dict[str, Any]
    ) -> List[str]:
        """Generate comprehensive recommendations"""
        recommendations = []

        overall_sentiment = self._calculate_overall_sentiment(source_analyses)
        consensus_score = self._calculate_consensus_score(source_analyses)

        if overall_sentiment == "positive" and consensus_score > 0.7:
            recommendations.append(
                "Strong positive consensus - consider bullish strategies"
            )
        elif overall_sentiment == "negative" and consensus_score > 0.7:
            recommendations.append(
                "Strong negative consensus - consider bearish strategies"
            )
        elif consensus_score < 0.5:
            recommendations.append("Low consensus - wait for clearer signals")
        else:
            recommendations.append("Moderate consensus - proceed with caution")

        # Check for divergence
        divergence_alerts = self._identify_divergence_alerts(source_analyses)
        if divergence_alerts:
            recommendations.append("Divergent sentiment detected - monitor closely")

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
