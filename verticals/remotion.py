"""Remotion integration — renders motion graphics clips via npx remotion render.

Two compositions available:
  VerticalIntro    - 2-second animated branded intro (prepended to final video)
  KineticCaption   - Word-by-word caption overlay (full video duration)

Usage:
  from verticals.remotion import render_intro, render_caption_overlay, remotion_available

  if remotion_available():
      intro = render_intro(title="Claude Code Is Wild", niche="AI Tools", out_dir=out_dir)
      # intro is a Path to a 2-second MP4 clip, or None on failure
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from .log import log

# Remotion project root lives next to the verticals package
_REMOTION_DIR = Path(__file__).parent.parent / "remotion"


def remotion_available() -> bool:
    """Check that npx and the remotion project are present."""
    if not shutil.which("npx"):
        return False
    if not (_REMOTION_DIR / "package.json").exists():
        return False
    node_modules = _REMOTION_DIR / "node_modules" / "remotion"
    return node_modules.exists()


def _render(
    composition: str,
    props: dict,
    out_path: Path,
    timeout: int = 120,
) -> Path | None:
    """Run `npx remotion render <composition>` with JSON props."""
    props_json = json.dumps(props)
    cmd = [
        "npx", "remotion", "render",
        composition,
        str(out_path),
        "--props", props_json,
        "--log", "error",
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(_REMOTION_DIR),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            log(f"[remotion] render failed for {composition}: {result.stderr[:300]}")
            return None
        return out_path
    except subprocess.TimeoutExpired:
        log(f"[remotion] render timed out for {composition}")
        return None
    except Exception as e:
        log(f"[remotion] unexpected error: {e}")
        return None


def render_intro(
    title: str,
    out_dir: Path,
    niche: str = "AI",
    accent_color: str = "#00E5C0",
    bg_color: str = "#111111",
) -> Path | None:
    """Render a 2-second branded intro clip.

    Returns Path to rendered MP4, or None if Remotion is unavailable or render fails.
    Falls back gracefully — pipeline continues without intro if this returns None.
    """
    if not remotion_available():
        log("[remotion] not installed — skipping intro render")
        return None

    out_path = out_dir / "remotion_intro.mp4"
    props = {
        "title": title,
        "niche": niche,
        "accentColor": accent_color,
        "bgColor": bg_color,
    }
    log(f"[remotion] rendering intro: '{title}'")
    result = _render("VerticalIntro", props, out_path)
    if result:
        log(f"[remotion] intro ready: {out_path}")
    return result


def render_caption_overlay(
    words: list[dict],
    duration_seconds: float,
    out_dir: Path,
    accent_color: str = "#00E5C0",  # Cronduit teal — matches VerticalIntro
) -> Path | None:
    """Render a kinetic caption overlay as MP4 (same dimensions as the main video).

    words: list of {"text": str, "startMs": int, "endMs": int}
    Returns Path to rendered MP4, or None on failure.
    """
    if not remotion_available():
        return None

    duration_frames = int(duration_seconds * 30)
    out_path = out_dir / "remotion_captions.mp4"
    props = {
        "words": words,
        "duration": duration_seconds,
        "accentColor": accent_color,
    }
    log(f"[remotion] rendering caption overlay ({duration_frames} frames)")
    return _render("KineticCaption", props, out_path, timeout=max(120, duration_frames * 2))
