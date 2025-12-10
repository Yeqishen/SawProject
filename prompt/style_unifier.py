from prompt.prompt_config import VISUAL_STYLE_KEYWORDS

# 模板 A：针对前景道具 (Assets)
# 重点：强调 "die-cut sticker" (模切贴纸感) 和 "white border" (白边/轮廓)，这让转矢量图效果极佳。
ASSET_PROMPT_TEMPLATE = (
    "Item: {item_description}. "
    "View: Front view, full shot. "
    f"Art Style: {VISUAL_STYLE_KEYWORDS}. "
    # 这里的 magic words 是 'die-cut sticker' 和 'strong outline'
    "Setting: ISOLATED on a PURE WHITE background, die-cut sticker style with strong outline, no shadow, no reflection, clean edges. "
    "Quality: 8k resolution, vector render, 2d."
)

# 模板 B：针对背景图 (Backgrounds)
# 重点：背景虽然有描边，但要避免过度复杂的线条干扰文字阅读。
BACKGROUND_PROMPT_TEMPLATE = (
    "Scene: {scene_description}. "
    f"Art Style: {VISUAL_STYLE_KEYWORDS}. "
    "Composition: Wide angle, clear center area for text, plenty of negative space, balanced composition. "
    "Line Work: Crisp line art, bold contours. "  # 强调线条清晰
    "Lighting: Flat lighting, cheerful atmosphere. "
    "Restriction: No text, no watermark, no blur, no realistic shading."
)