# visual_engineer.py
import os
import json
import requests
from dotenv import load_dotenv

# 导入你的 Prompt 字符串
from prompt.visual_engineer import PROMPT as ENGINEER_PROMPT

load_dotenv()


class VisualEngineer:
    def __init__(self, model="google/gemini-3-pro-preview"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model

    def analyze_assets(self, input_file="narrative_output.json"):
        print(f"🧠 [2/3] 正在拆解视觉素材并去重...")

        if not os.path.exists(input_file):
            print("❌ 找不到剧本文件，请先运行步骤 1。")
            return None

        with open(input_file, 'r', encoding='utf-8') as f:
            storyboard_data = json.load(f)

        # 构造 Prompt：将剧本数据喂给 LLM
        # 注意：这里我们将 storyboard 转为字符串放入 Prompt
        user_message = f"Here is the Storyboard JSON List:\n{json.dumps(storyboard_data, ensure_ascii=False)}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": ENGINEER_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']

            # 清洗 Markdown
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")

            assets_list = json.loads(content)

            # 保存结果
            output_file = "assets_list.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(assets_list, f, ensure_ascii=False, indent=2)

            # 统计一下优化效果
            bg_count = len(assets_list.get('backgrounds', []))
            char_count = len(assets_list.get('character_sprites', []))
            prop_count = len(assets_list.get('interactive_props', []))

            print(f"✅ 素材拆解完毕。优化结果：")
            print(f"   - 背景图: {bg_count} 张 (对应 {len(storyboard_data)} 页PPT)")
            print(f"   - 角色动作: {char_count} 个")
            print(f"   - 交互道具: {prop_count} 个")
            print(f"   已保存至 {output_file}")

            return assets_list

        except Exception as e:
            print(f"❌ 视觉拆解失败: {e}")
            return None


if __name__ == "__main__":
    engineer = VisualEngineer()
    engineer.analyze_assets()
