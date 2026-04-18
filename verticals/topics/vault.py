"""Vault topic source — pulls breaking AI intel from Obsidian wiki pages."""

import re
from pathlib import Path
from .base import TopicCandidate, TopicSource

VAULT_PATH = Path.home() / "The Codex Brain" / "wiki" / "pages"

# File patterns that signal high-value AI/tech content
HIGH_VALUE_PATTERNS = [
    r"intel-github.*\d{4,}-stars",   # repos with star counts
    r"analysis-",                     # deep research pages
    r"Claude.*[Rr]elease",
    r"GPT-",
    r"Best.*LLMs",
    r"ArcReel",
    r"agent-squad",
    r"herdr",
    r"1-bit",
    r"Bonsai",
]


def _extract_title(path: Path) -> str:
    """Pull display title from frontmatter or filename."""
    try:
        text = path.read_text(errors="ignore")
        # Try frontmatter title
        m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
        # Try first H1
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    # Fallback: clean up filename
    name = path.stem
    name = re.sub(r"^(intel|analysis|concept|entity|source)-", "", name)
    name = name.replace("-", " ").replace("_", " ")
    return name.title()


def _extract_summary(path: Path, max_chars: int = 200) -> str:
    """Pull first meaningful sentence from page body."""
    try:
        text = path.read_text(errors="ignore")
        # Skip frontmatter
        if text.startswith("---"):
            end = text.find("---", 3)
            text = text[end + 3:] if end > 0 else text
        # Find first non-empty, non-heading line
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-") and len(line) > 30:
                return line[:max_chars]
    except Exception:
        pass
    return ""


def _score_page(path: Path) -> float:
    """Score relevance: recency + pattern match."""
    import time
    score = 0.5
    name = path.name.lower()

    for pattern in HIGH_VALUE_PATTERNS:
        if re.search(pattern, name, re.IGNORECASE):
            score += 0.3
            break

    # Boost recently modified pages
    try:
        age_days = (time.time() - path.stat().st_mtime) / 86400
        if age_days < 1:
            score += 0.2
        elif age_days < 3:
            score += 0.1
        elif age_days < 7:
            score += 0.05
    except Exception:
        pass

    return min(1.0, score)


class VaultSource(TopicSource):
    name = "vault"

    def __init__(self, config: dict = None):
        config = config or {}
        self.vault_path = Path(config.get("path", str(VAULT_PATH))).expanduser()

    @property
    def is_available(self) -> bool:
        return self.vault_path.exists()

    def fetch_topics(self, limit: int = 10) -> list[TopicCandidate]:
        if not self.is_available:
            return []

        pages = sorted(
            self.vault_path.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        topics = []
        for page in pages[:60]:  # scan most recent 60
            name = page.name.lower()
            # Skip concept stubs and generic pages
            if any(x in name for x in ["concept-concept", "concept-slug", "concept-claude.md"]):
                continue

            score = _score_page(page)
            if score < 0.5:
                continue

            title = _extract_title(page)
            summary = _extract_summary(page)

            topics.append(TopicCandidate(
                title=title,
                source="vault",
                trending_score=score,
                summary=summary,
                metadata={"file": str(page)},
            ))

        topics.sort(key=lambda t: t.trending_score, reverse=True)
        return topics[:limit]
