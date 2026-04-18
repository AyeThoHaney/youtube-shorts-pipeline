"""Google Trends topic source via pytrends.

Two modes:
- fetch_topics()        — real-time trending searches (broad)
- fetch_rising_topics() — breakout/rising queries for niche seed keywords (higher signal)
"""

import time
from .base import TopicCandidate, TopicSource

# Niche → seed keywords for related_queries rising pull
NICHE_SEEDS = {
    "ai":               ["artificial intelligence", "AI tools", "ChatGPT", "Claude AI"],
    "tech":             ["technology 2026", "tech news", "software"],
    "finance":          ["investing 2026", "stock market", "crypto", "money tips"],
    "true_crime":       ["true crime", "crime documentary", "unsolved mystery"],
    "reddit_stories":   ["reddit story", "AITA reddit", "reddit thread"],
    "motivation":       ["self improvement", "productivity tips", "mindset"],
    "science":          ["science news", "space exploration", "biology discovery"],
    "fitness":          ["workout tips", "gym motivation", "weight loss"],
    "cooking":          ["recipe ideas", "food trends", "cooking tips"],
    "gaming":           ["gaming news", "game release", "esports"],
    "education":        ["learn online", "study tips", "education news"],
    "agentic_workflows": ["AI agents", "automation tools", "Claude Code", "n8n"],
    "general":          ["trending now", "viral news", "what's happening"],
}


class GoogleTrendsSource(TopicSource):
    name = "google_trends"

    def __init__(self, config: dict = None):
        config = config or {}
        self.geo = config.get("geo", "US")
        self.niche = config.get("niche", "general")

    @property
    def is_available(self) -> bool:
        try:
            from pytrends.request import TrendReq  # noqa: F401
            return True
        except ImportError:
            return False

    def fetch_topics(self, limit: int = 10) -> list[TopicCandidate]:
        """Real-time trending searches for the configured geo."""
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=360)
        trending = pytrends.trending_searches(pn=self._geo_to_pn())

        topics = []
        for i, row in trending.head(limit).iterrows():
            title = str(row[0])
            score = max(0.1, 1.0 - (i * 0.05))
            topics.append(TopicCandidate(
                title=title,
                source="google_trends_trending",
                trending_score=score,
            ))
        return topics

    def fetch_rising_topics(self, limit: int = 15) -> list[TopicCandidate]:
        """Breakout/rising queries for niche seed keywords — higher signal than trending."""
        from pytrends.request import TrendReq

        seeds = NICHE_SEEDS.get(self.niche, NICHE_SEEDS["general"])
        pytrends = TrendReq(hl="en-US", tz=360)

        seen = set()
        topics = []

        for seed in seeds[:3]:  # max 3 seeds to stay under rate limit
            try:
                pytrends.build_payload(
                    [seed],
                    cat=0,
                    timeframe="now 7-d",
                    geo=self.geo,
                    gprop="youtube",  # YouTube search filter
                )
                related = pytrends.related_queries()
                rising_df = related.get(seed, {}).get("rising")

                if rising_df is not None and not rising_df.empty:
                    for _, row in rising_df.head(5).iterrows():
                        query = str(row["query"]).strip()
                        value = row["value"]  # int or "Breakout"

                        if query.lower() in seen:
                            continue
                        seen.add(query.lower())

                        # Score: Breakout = 1.0, else normalize 0-1
                        if isinstance(value, str) and value.lower() == "breakout":
                            score = 1.0
                        else:
                            try:
                                score = min(1.0, int(value) / 5000)
                            except (ValueError, TypeError):
                                score = 0.5

                        topics.append(TopicCandidate(
                            title=query,
                            source="google_trends_rising",
                            trending_score=score,
                            metadata={"seed": seed, "value": str(value), "geo": self.geo},
                        ))

                time.sleep(1.5)  # avoid rate limit between seeds

            except Exception:
                time.sleep(3)
                continue

        # Sort by score descending, return top N
        topics.sort(key=lambda t: t.trending_score, reverse=True)
        return topics[:limit]

    def _geo_to_pn(self) -> str:
        geo_map = {
            "US": "united_states",
            "GB": "united_kingdom",
            "AU": "australia",
            "IN": "india",
            "CA": "canada",
        }
        return geo_map.get(self.geo, "united_states")
