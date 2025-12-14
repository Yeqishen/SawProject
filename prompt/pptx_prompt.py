# prompt/pptx_prompt.py
import json

def build_pptx_layout_prompt(narrative_chunk, assets_full):
    """
    构建用于生成 python-pptx 布局指令的 Prompt。
    """

    narrative_str = json.dumps(narrative_chunk, ensure_ascii=False, indent=2)
    assets_str = json.dumps(assets_full, ensure_ascii=False, indent=2)

    prompt = f"""
    You are an expert Presentation Layout Engine using python-pptx. 
    Your goal is to visualize a children's interactive storybook based on a narrative script and a list of available assets.

    [GLOBAL CANVAS SETTINGS]
    - Aspect Ratio: 16:9
    - Width: 10 inches
    - Height: 5.625 inches
    - Coordinate System: (0,0) is Top-Left.
    - Z-Index Strategy: Background (0) -> Props (1) -> Narrator (2) -> Dialogue Box (3) -> Text (4).

    [ASSETS LIBRARY]
    {assets_str}

    [NARRATIVE SCRIPT (Current Batch)]
    {narrative_str}

    [LAYOUT RULES]
    1. **Background**: Must cover the entire slide (left: 0, top: 0, width: 10, height: 5.625).
    2. **Narrator**: 
       - Usually placed on the Left or Right side. 
       - Typical size: width ~2.5 to 3.5 inches. 
       - Ensure feet align near the bottom (but not cut off).
    3. **Dialogue Box**:
       - Create a semi-transparent shape at the bottom for text readability.
       - Position: typically left: 0.5, top: 4.2, width: 9, height: 1.2.
    4. **Props**:
       - If multiple props exist (e.g., counting medals), distribute them evenly in the "Action Area" (center of screen, y=1.0 to y=4.0).
       - Do NOT overlap props with the Narrator.
    5. **Text**:
       - 'text' field from script goes into the Dialogue Box.
       - Font size should be readable (approx 18-24pt).

    [OUTPUT FORMAT]
    Return a STRICT JSON list (no markdown formatting, no comments outside JSON). 
    Each item in the list represents one slide containing a list of 'elements'.

    Expected JSON Structure:
    [
      {{
        "page_id": 1,
        "elements": [
          {{
            "type": "image", 
            "content": "backgrounds/scene_forest_podium.png", 
            "position": {{ "left": 0, "top": 0, "width": 10, "height": 5.625 }}
          }},
          {{
            "type": "image", 
            "content": "characters/narrator_happy.png", 
            "position": {{ "left": 0.5, "top": 2.0, "width": 3.0, "height": 3.5 }} 
          }},
          {{
            "type": "shape",
            "shape_type": "RECTANGLE",
            "color_hex": "FFFFFF",
            "opacity": 0.8,
            "position": {{ "left": 0.5, "top": 4.2, "width": 9.0, "height": 1.2 }}
          }},
          {{
            "type": "text",
            "content": "Hello, friends! Welcome to the Forest Sports Day!",
            "font_size": 20,
            "font_color": "000000",
            "position": {{ "left": 0.7, "top": 4.3, "width": 8.6, "height": 1.0 }}
          }}
        ]
      }},
      ... (next slide)
    ]
    """
    return prompt