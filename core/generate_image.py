from prompt.prompt_config import VISUAL_STYLE_KEYWORDS


def generate_final_image_prompts(visual_data_list):
    """
    接收阶段二的 JSON，结合全局风格配置，生成最终发给 DALL-E/MJ 的提示词。
    """
    final_tasks = []

    for page in visual_data_list:
        # ---------------------------
        # A. 生成背景图 Prompt
        # ---------------------------
        bg_prompt = (
            f"Scene: {page['background_summary']}. "
            f"Art Style: {VISUAL_STYLE_KEYWORDS}. "
            "Composition: Wide angle, clear center area for text (negative space), balanced composition. "
            "Line Work: Crisp line art, bold contours. "  # 强调线条
            "Restrictions: No text, no watermark, no blur, no realistic shading."
        )
        final_tasks.append({"type": "background", "prompt": bg_prompt, "page": page['page_id']})

        # ---------------------------
        # B. 生成道具图 Prompt (Assets)
        # ---------------------------
        for asset in page['assets']:
            asset_prompt = (
                f"Item: {asset['image_prompt']}. "
                "View: Front view, full shot. "
                f"Art Style: {VISUAL_STYLE_KEYWORDS}. "
                # 关键：强调纯白背景和模切感，为了完美抠图
                "Setting: ISOLATED on a PURE WHITE background, die-cut sticker style with strong black outline, no shadow, no reflection. "
                "Quality: 8k resolution, vector render, 2d."
            )
            final_tasks.append({"type": "asset", "id": asset['asset_id'], "prompt": asset_prompt})

    return final_tasks