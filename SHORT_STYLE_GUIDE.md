# Cronduit YouTube Shorts Style Guide

A quick visual reference for content creators using the YouTube Shorts pipeline.

## Visual Identity at a Glance

| Aspect | Details |
|--------|---------|
| **Brand** | Cronduit — AI-powered content automation |
| **Aesthetic** | Premium minimalist tech cinematic |
| **Mood** | Confident, sophisticated, technically precise |
| **Primary Color** | Teal (#00E5C0) — Energy, confidence, trust |
| **Secondary Color** | Ice Blue (#00B8FF) — Clarity, technical precision |
| **Background** | Dark charcoal (#111111→#1A1A1A gradient) |
| **Text** | Light gray (#E8E8E8) for maximum readability |

## Your Video Will Have

### 1. Animated 2-Second Intro
- Dark background with subtle gradient
- Your video title in bold sans-serif font
- Teal accent animations
- Professional motion graphics
- **No customization needed** — automatic branding

### 2. Kinetic Captions Throughout
- Word-by-word animations synchronized to voiceover
- Teal highlighting on key words
- Professional typography
- Full video duration
- **Readable on all thumbnail sizes** — optimized for mobile

### 3. Professional Thumbnail
- Gemini AI-generated base image
- Your video title overlaid in light gray text
- High contrast for visibility
- Dark background matching brand
- **Automatically optimized** — no manual design needed

### 4. Polished Video Assembly
- Cinematic b-roll with Ken Burns effects (pan/zoom)
- Natural AI voiceover (your choice of voice)
- Mood-matched background music
- Audio ducking during speech
- Seamless fade transitions

## Color Reference for Custom Overlays

If you're adding custom graphics, use these colors for consistency:

```
Teal #00E5C0      RGB: 0, 229, 192
Dark #111111       RGB: 17, 17, 17
Light #E8E8E8      RGB: 232, 232, 232
Ice Blue #00B8FF   RGB: 0, 184, 255
```

## What NOT to Do

- ❌ Don't add text overlays in white — use light gray (#E8E8E8)
- ❌ Don't use bright, saturated colors — stick to teal and ice blue
- ❌ Don't remove the intro/outro — they're part of the brand
- ❌ Don't add watermarks — branding is handled automatically
- ❌ Don't change the background to light — dark mode is part of identity

## What TO Do

- ✅ Use teal (#00E5C0) for emphasis and highlighting
- ✅ Keep text large and bold for mobile viewing
- ✅ Trust the automatic intro/caption styling
- ✅ Let the algorithm pick music that matches your topic
- ✅ Focus on compelling content — branding is handled

## Example Visual Palette

```
Primary Accent:        ████ #00E5C0 (Teal)
Secondary Accent:      ████ #00B8FF (Ice Blue)
Background:            ████ #111111 (Dark)
Background Light:      ████ #1A1A1A (Slightly Lighter Dark)
Primary Text:          ████ #E8E8E8 (Light Gray)
Secondary Text:        ████ #808080 (Medium Gray)
```

## Animation Style

All animations use:
- **Smooth easing** — ease-in-out for natural motion
- **Quick transitions** — 200-300ms for snappy feel
- **Soft glow effects** — 8-12px neon glow around accents
- **Volumetric lighting** — God rays from top-left
- **No clutter** — Clean, minimal, spacious composition

## Typography

Default text uses:
- **Font:** Bold sans-serif (system fonts optimized)
- **Size:** Large for mobile (48px+)
- **Weight:** 600-700 (semi-bold to bold)
- **Spacing:** Generous line height for readability
- **Color:** Light gray (#E8E8E8) or white for contrast

## Platform Optimization

Your shorts are optimized for:
- **YouTube Shorts** — 9:16 vertical (1080x1920)
- **Instagram Reels** — 9:16 vertical (exported format)
- **TikTok** — 9:16 vertical (exported format)
- **Mobile phones** — Tested on all screen sizes
- **Low bandwidth** — Compressed without quality loss

## Music Mood Matching

The pipeline automatically selects background music based on your content niche:

| Niche | Music Mood | Example |
|-------|-----------|---------|
| Tech/AI | Modern, upbeat, futuristic | Synth-driven, electronic |
| Finance | Professional, confident, analytical | Piano, strings, modern |
| Gaming | Energetic, intense, immersive | Electronic, high energy |
| Fitness | Motivational, powerful, driving | Upbeat, rhythmic |
| Beauty | Elegant, sophisticated, trendy | Ambient, modern pop |
| Business | Professional, authoritative, clear | Corporate, instrumental |

## Quality Checklist

Before publishing, verify:

- [ ] **Intro** — Title is clear and centered
- [ ] **Captions** — All words are visible and in sync with audio
- [ ] **Thumbnail** — Title text is readable (not cut off)
- [ ] **Colors** — All graphics use brand palette
- [ ] **Audio** — Voiceover is clear, music doesn't overpower
- [ ] **Duration** — 30-90 seconds for Shorts (recommended: 45-60s)
- [ ] **Aspect Ratio** — 9:16 vertical (automatic from pipeline)

## Common Questions

**Q: Can I customize the intro animation?**  
A: The intro uses the Cronduit brand style. For custom animations, edit `verticals/remotion.py`.

**Q: Can I use different background colors?**  
A: Dark mode is part of the brand. Override in `verticals/brand.py` if needed.

**Q: Why is my text gray instead of white?**  
A: Light gray (#E8E8E8) has better contrast on video backgrounds. It meets WCAG AA standards.

**Q: Can I skip the branded intro?**  
A: Yes, pass `remotion_title=None` in draft to skip intro generation.

**Q: What if I want a different music vibe?**  
A: Manually select track from `music/` directory. Pipeline will use it if only one track exists.

## Need More Help?

- **Brand Details:** See [BRAND_INTEGRATION.md](BRAND_INTEGRATION.md)
- **Full Brand Spec:** Read [`~/tools/BRAND.md`](../../tools/BRAND.md)
- **Code Examples:** Check `verticals/brand.py` for all color constants
- **Visual Lock:** See `~/tools/townhall/config/master_visual_style_lock.md` for complete visual direction

---

**Remember:** You focus on content. The Cronduit brand system handles the visual polish. ✨
