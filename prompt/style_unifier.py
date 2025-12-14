from prompt.prompt_config import VISUAL_STYLE_KEYWORDS

# -----------------------------------------------------------------------------
# 风格核心配置：手绘油画卡通感
# -----------------------------------------------------------------------------
# 核心逻辑：
# 1. 彻底移除 "Vector", "Die-cut", "Sticker" 等导致“硬边”和“塑料感”的词。
# 2. 增加 "Oil painting", "Gouache", "Brushstrokes" 等强调材质的词。
# 3. 满足你的需求：保留轮廓线 (Outline)，但要是自然的笔触线。

# 模板 A：针对前景道具/角色 (Assets)
ASSET_PROMPT_TEMPLATE = (
    "Item: {item_description}. "
    "View: Front view, focus on the subject. "
    # 风格定义：强调油画/水粉手绘质感
    f"Art Style: {VISUAL_STYLE_KEYWORDS}, hand-painted oil painting cartoon style. "
    # 轮廓线需求：使用 'Bold organic outline' (粗犷的有机轮廓) 替代 'Vector outline'
    "Line Work: Bold, expressive organic outline surrounding the subject. "
    # 背景需求：背景淡化或简单背景，不强求扣图
    "Setting: Simple minimal background, soft faded colors, or isolated on white canvas. "
    # 材质细节
    "Texture: Rich oil paint texture, visible brushstrokes, vibrant colors. "
    "Lighting: Soft, warm volumetric lighting. "
    # 负向提示：防止出现照片写实或矢量图
    "Negative: Photorealistic, 3d render, vector art, flat design, hard mechanical lines."
)

# 模板 B：针对背景图 (Backgrounds)
BACKGROUND_PROMPT_TEMPLATE = (
    "Scene: {scene_description}. "
    f"Art Style: {VISUAL_STYLE_KEYWORDS}, hand-painted oil painting illustration. "
    "Composition: Wide angle, spacious, leaving center empty for text. "
    # 渲染方式：强调绘画性
    "Rendering: Painterly style with soft edges, oil painting texture on canvas. "
    "Line Work: Subtle hand-drawn outlines on major elements. "
    "Lighting: Atmospheric, dreamy, warm sunlight. "
    "Restriction: No characters, no text, no watermarks, no sharp vector look."
)