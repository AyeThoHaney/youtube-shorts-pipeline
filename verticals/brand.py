"""Cronduit brand identity and visual constants.

Source: ~/tools/BRAND.md + master_visual_style_lock.md
"""

# ─────────────────────────────────────────────────────
# Brand Identity
# ─────────────────────────────────────────────────────
BRAND_NAME = "Cronduit"
BRAND_TAGLINE = "Your edge in AI-powered automation."
BRAND_DESCRIPTION = "AI-first studio building automated systems for content, intelligence, and distribution."

# ─────────────────────────────────────────────────────
# Color Palette
# ─────────────────────────────────────────────────────

# Primary colors
COLOR_BG_DARK = "#111111"        # Dark background (start)
COLOR_BG_DARK_LIGHT = "#1A1A1A"  # Dark background (end, subtle gradient)
COLOR_PRIMARY_TEAL = "#00E5C0"   # Cronduit signature accent (energy, confidence, trust)
COLOR_SECONDARY_ICE = "#00B8FF"  # Electric ice-blue neon accent (clarity, technical precision)

# RGB equivalents for video/canvas rendering
RGB_BG_DARK = (17, 17, 17)
RGB_BG_DARK_LIGHT = (26, 26, 26)
RGB_PRIMARY_TEAL = (0, 229, 192)
RGB_SECONDARY_ICE = (0, 184, 255)

# Additional palette
COLOR_GRAYSCALE_LIGHT = "#E8E8E8"
COLOR_GRAYSCALE_MED = "#808080"
COLOR_GRAYSCALE_DARK = "#333333"

RGB_GRAYSCALE_LIGHT = (232, 232, 232)
RGB_GRAYSCALE_MED = (128, 128, 128)
RGB_GRAYSCALE_DARK = (51, 51, 51)

# ─────────────────────────────────────────────────────
# Visual Style Parameters
# ─────────────────────────────────────────────────────

# Glow and lighting
GLOW_RADIUS_PX = 10  # Soft 8-12px glow falloff for neon accents
NEON_GLOW_BLUR = 1.5  # Glow blur multiplier

# Contrast and spacing
CONTRAST_RATIO = "high"  # High contrast for clarity
NEGATIVE_SPACE_RATIO = 0.35  # Generous negative space (35% of frame)

# Typography
FONT_STYLE = "bold sans-serif"  # Clean, geometric, professional
HEADLINE_SCALE = 1.2  # 20% larger than body

# Composition
COMPOSITION_STYLE = "rule-of-thirds"  # or "centered focal point"
FOCAL_POINT_BREATHING_ROOM = True  # Leave space around focal elements

# Lighting model
LIGHTING_SOURCE = "top-left"  # Soft volumetric god rays
SUBSURFACE_GLOW = "subtle"  # Subtle neon subsurface glow
BOKEH_STYLE = "cinematic-35mm"  # Cinematic lens characteristics

# ─────────────────────────────────────────────────────
# Mood and Aesthetic
# ─────────────────────────────────────────────────────
MOOD = "confident, innovative, sophisticated, calm authority"
AESTHETIC = "premium minimalist tech cinematic"
REFERENCE_STYLE = "Apple 2026 + Blade Runner 2049 restraint"

# Technical specs
RENDER_RESOLUTION = "8K"  # Master render resolution
OUTPUT_RESOLUTION = "1200x630"  # Downsampled output (for graphics/socials)
QUALITY = "ultra-sharp, zero noise, perfect typography integration"

# ─────────────────────────────────────────────────────
# Video/Shorts Specific
# ─────────────────────────────────────────────────────

# Intro/Outro animation
INTRO_BG_COLOR = COLOR_BG_DARK
INTRO_ACCENT_COLOR = COLOR_PRIMARY_TEAL
INTRO_TEXT_COLOR = COLOR_GRAYSCALE_LIGHT
INTRO_DURATION_MS = 2000  # 2 seconds

# Outro animation
OUTRO_BG_COLOR = COLOR_BG_DARK
OUTRO_ACCENT_COLOR = COLOR_SECONDARY_ICE
OUTRO_TEXT_COLOR = COLOR_GRAYSCALE_LIGHT
OUTRO_DURATION_MS = 1500  # 1.5 seconds

# Caption styling
CAPTION_BG_COLOR = COLOR_BG_DARK
CAPTION_TEXT_COLOR = COLOR_GRAYSCALE_LIGHT
CAPTION_ACCENT_COLOR = COLOR_PRIMARY_TEAL
CAPTION_FONT_WEIGHT = 600  # Semi-bold

# Thumbnail styling
THUMBNAIL_BG_COLOR = COLOR_BG_DARK
THUMBNAIL_ACCENT_COLOR = COLOR_PRIMARY_TEAL
THUMBNAIL_TEXT_COLOR = COLOR_GRAYSCALE_LIGHT
THUMBNAIL_BORDER_COLOR = COLOR_SECONDARY_ICE
THUMBNAIL_BORDER_WIDTH = 3

# ─────────────────────────────────────────────────────
# Grok Imagine Prompt Template
# ─────────────────────────────────────────────────────
GROK_PROMPT_TEMPLATE = """You are Cronduit Visual Director.
Style: premium minimalist tech cinematic.
Color science: deep matte charcoal/black background (#111111 to #1A1A1A gradients), subtle dark-to-light radial gradients, Cronduit signature teal (#00E5C0) and electric ice-blue neon accents (#00B8FF) with soft 8-12px glow falloff. High contrast, generous negative space.
Composition: rule-of-thirds or centered focal point with breathing room for bold sans-serif headline overlay (Cronduit font family). Clean geometric data flows, abstract nodes, subtle circuit patterns or particle streams — never busy.
Lighting: soft volumetric god rays from top-left, gentle rim lighting on foreground elements, subtle neon subsurface glow, cinematic 35mm lens bokeh in background, micro-reflections on metallic surfaces.
Mood: confident, innovative, sophisticated, calm authority. Professional product photography fused with subtle cyber-minimalism (Apple 2026 + Blade Runner 2049 restraint).
Technical: photorealistic digital render, 8K resolution downsampled to 1200x630, ultra-sharp, zero noise, perfect typography integration potential, no people, no clutter, no text except subtle watermark if requested.
Output ONLY the complete ready-to-use Grok Imagine prompt string. No explanations.
"""

# ─────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple.

    Args:
        hex_color: Color in format "#RRGGBB"

    Returns:
        Tuple of (R, G, B) values 0-255
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color.

    Args:
        rgb: Tuple of (R, G, B) values 0-255

    Returns:
        Color in format "#RRGGBB"
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def get_color_palette(theme: str = "default") -> dict:
    """Get a complete color palette for a given theme.

    Args:
        theme: Theme name ("default", "dark", "light")

    Returns:
        Dictionary of color definitions
    """
    if theme == "dark":
        return {
            "bg": COLOR_BG_DARK,
            "bg_light": COLOR_BG_DARK_LIGHT,
            "primary": COLOR_PRIMARY_TEAL,
            "secondary": COLOR_SECONDARY_ICE,
            "text": COLOR_GRAYSCALE_LIGHT,
            "text_muted": COLOR_GRAYSCALE_MED,
        }
    # default theme
    return {
        "bg": COLOR_BG_DARK,
        "bg_light": COLOR_BG_DARK_LIGHT,
        "primary": COLOR_PRIMARY_TEAL,
        "secondary": COLOR_SECONDARY_ICE,
        "text": COLOR_GRAYSCALE_LIGHT,
        "text_muted": COLOR_GRAYSCALE_MED,
    }
