from __future__ import annotations
"""Script generation with niche intelligence.

Uses the niche profile to shape every aspect of the script:
tone, pacing, hook patterns, CTA variants, forbidden phrases,
visual vocabulary for b-roll prompts, and thumbnail guidance.
"""

import json

from .config import PLATFORM_CONFIGS
from .llm import call_llm
from .log import log
from .niche import load_niche, get_script_context, get_visual_context, get_visual_prompt_suffix
from .research import research_topic


def generate_draft(
    news: str,
    channel_context: str = "",
    niche: str = "general",
    platform: str = "shorts",
    provider: str | None = None,
) -> dict:
    """Research topic + generate niche-aware draft via LLM.

    Args:
        news: Topic or news headline.
        channel_context: Optional channel context.
        niche: Niche profile name (loads from niches/<n>.yaml).
        platform: Target platform (shorts, reels, tiktok).
        provider: LLM provider (claude, gemini, openai, ollama).
    """
    # Load niche intelligence
    profile = load_niche(niche)
    script_context = get_script_context(profile)
    visual_context = get_visual_context(profile)

    # Research
    research = research_topic(news)

    # Platform config
    platform_key = platform if platform != "all" else "shorts"
    platform_cfg = PLATFORM_CONFIGS.get(platform_key, PLATFORM_CONFIGS["shorts"])
    max_words = platform_cfg["max_script_words"]
    platform_label = platform_cfg["label"]

    # Build visual guidance for b-roll prompts
    visual_guidance = ""
    if visual_context:
        vis_parts = []
        if visual_context.get("style"):
            vis_parts.append(f"Visual style: {visual_context['style']}")
        if visual_context.get("mood"):
            vis_parts.append(f"Visual mood: {visual_context['mood']}")
        subjects = visual_context.get("subjects", {})
        if subjects.get("prefer"):
            vis_parts.append(f"Preferred subjects: {', '.join(subjects['prefer'][:5])}")
        if subjects.get("avoid"):
            vis_parts.append(f"Avoid: {', '.join(subjects['avoid'][:3])}")
        suffix = visual_context.get("prompt_suffix", "")
        if suffix:
            vis_parts.append(f"Append to every b-roll prompt: {suffix}")
        if vis_parts:
            visual_guidance = "\nB-ROLL VISUAL GUIDANCE:\n" + "\n".join(vis_parts)

    # Thumbnail guidance
    thumb_config = profile.get("thumbnail", {})
    thumb_guidance = ""
    if thumb_config:
        tg_parts = []
        if thumb_config.get("style"):
            tg_parts.append(f"Thumbnail style: {thumb_config['style']}")
        guidelines = thumb_config.get("guidelines", [])
        if guidelines:
            tg_parts.append(f"Thumbnail rules: {'; '.join(guidelines[:3])}")
        if tg_parts:
            thumb_guidance = "\nTHUMBNAIL GUIDANCE:\n" + "\n".join(tg_parts)

    channel_note = f"\nChannel context: {channel_context}" if channel_context else ""

    prompt = f"""You are the 2026 Advanced Content Engine v4.1 — zero fluff, maximum virality and monetization.{channel_note}

Niche: {niche}
Platform: {platform_label} ({max_words} words max, ~60-90 seconds spoken)

{script_context}

BEGIN RESEARCH DATA
{research}
END RESEARCH DATA

{visual_guidance}
{thumb_guidance}

STRICT RULES (violate any and output FAIL):
- Use ONLY facts inside the RESEARCH DATA block. If something is missing, write "[NOT IN RESEARCH — SKIP]".
- Never hallucinate names, stats, events, or quotes.
- After drafting, run a reflection pass: re-read RESEARCH DATA and confirm every single claim.
- Output must be {max_words} words max when spoken at natural pace.
- Follow the TONE, PACING, and HOOK PATTERNS from the niche profile above.
- Never use any of the NEVER USE phrases from the niche profile.
- B-roll prompts must follow the visual guidance (style, mood, preferred subjects).

Niche adaptation rules (apply rigorously):
- Tech/AI: data-driven, tool breakdowns, "this changes everything"
- Finance: numbers-first, risk/reward, "most people get this wrong"
- True Crime: tension build, "what they don't want you to know"
- Reddit Stories: raw emotional delivery, "you won't believe #3"
- Motivation: pattern interrupt + proof + actionable
- Science: myth-busting + visual "wow" moments
- Any other niche: auto-detect core emotional driver and hook type from research.

Add 2026 small diamonds automatically:
- First 1-2 seconds: visual + text + spoken pattern interrupt.
- Completion rate booster: loopable ending (visual or spoken callback to opening).
- Silent viewing: on-screen text every 3-4 seconds implied in b-roll prompts.
- Search SEO: primary keyword in first 8 words of title/caption + spoken in script.
- ElevenLabs lip-sync ready: short sentences, natural pauses marked with commas.
- B-roll MUST be tied 1:1 to script beats — each prompt must reference a specific moment in the spoken script.
  Format each b_roll_prompt as: "[BEAT: first 4 words of the spoken line this visual plays over] → [exact visual description]"
  Example: "[BEAT: I replaced three tools] → dark terminal window, green text scrolling, MacBook on desk, cinematic close-up"
  Never use generic prompts like "cinematic landscape" or "technology background".

Output EXACTLY this JSON (nothing else):
{{
  "niche_tone": "exact tone description adapted to this topic",
  "script": "full spoken script with [ElevenLabs voice tags] for emotion, pacing, whispers, emphasis. Hook MUST be 0-3 seconds.",
  "b_roll_prompts": ["[BEAT: first 4 spoken words] → hyper-specific visual tied to that moment", "[BEAT: ...] → ...", "[BEAT: ...] → ..."],
  "youtube": {{
    "title": "40-char max, front-loaded keywords + curiosity gap — works for Shorts and long-form",
    "description": "first 2 lines = searchable hook + keywords, then CTA + 3-5 hashtags",
    "tags": ["search-value tag 1", "tag 2", "tag 3"],
    "format": "shorts"
  }},
  "tiktok_caption": "search-optimized, 3-sec hook in first line",
  "ig_reels_caption": "polished, save-worthy, value-driven + CTA",
  "thumbnail_prompt": "exact image gen prompt — high contrast, focal subject, text overlay matching title",
  "retention_sauce": ["loopable ending method used", "silent-viewing caption strategy", "search-value keyword placement"],
  "elevenlabs_voice_directives": "voice name/clone + stability/clarity/style settings for this script",
  "cross_platform_notes": "exact tweaks per platform + repurposing strategy"
}}"""

    raw = call_llm(prompt, provider=provider)

    # Parse JSON from response
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    # Handle case where LLM wraps in additional text
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start >= 0 and end > start:
        raw = raw[start:end]

    draft = json.loads(raw)

    # Normalize new schema → legacy field names for pipeline compatibility
    # youtube: {title, description, tags, format} → flat fields
    yt = draft.pop("youtube", draft.pop("youtube_shorts", {}))
    if yt:
        draft.setdefault("youtube_title", yt.get("title", ""))
        draft.setdefault("youtube_description", yt.get("description", ""))
        draft.setdefault("youtube_format", yt.get("format", "shorts"))
        tags = yt.get("tags", [])
        draft.setdefault("youtube_tags", ",".join(tags) if isinstance(tags, list) else tags)

    # ig_reels_caption → instagram_caption
    if "ig_reels_caption" in draft:
        draft.setdefault("instagram_caption", draft.pop("ig_reels_caption"))

    # b_roll_prompts → broll_prompts
    if "b_roll_prompts" in draft and "broll_prompts" not in draft:
        draft["broll_prompts"] = draft.pop("b_roll_prompts")

    # Validate and sanitize LLM output fields
    expected_str_fields = [
        "script", "youtube_title", "youtube_description",
        "youtube_tags", "instagram_caption", "tiktok_caption",
        "thumbnail_prompt", "niche_tone", "elevenlabs_voice_directives",
        "cross_platform_notes",
    ]
    for field in expected_str_fields:
        if field in draft and not isinstance(draft[field], str):
            draft[field] = str(draft[field])

    if "retention_sauce" in draft and not isinstance(draft["retention_sauce"], list):
        draft["retention_sauce"] = [str(draft["retention_sauce"])]

    if "broll_prompts" in draft:
        if not isinstance(draft["broll_prompts"], list):
            draft["broll_prompts"] = ["Cinematic landscape"] * 3
        else:
            draft["broll_prompts"] = [str(p) for p in draft["broll_prompts"][:3]]

    # Append visual prompt suffix to b-roll prompts
    suffix = get_visual_prompt_suffix(profile)
    if suffix and "broll_prompts" in draft:
        draft["broll_prompts"] = [
            f"{p}. {suffix}" for p in draft["broll_prompts"]
        ]

    draft["news"] = news
    draft["research"] = research
    draft["niche"] = niche
    draft["platform"] = platform
    return draft
