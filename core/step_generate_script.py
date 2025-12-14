# step_generate_script.py
import os
import json
import requests
from dotenv import load_dotenv

# 假设你把提示词字符串放在了 prompt 包里，或者你可以直接粘贴在这里
from prompt.narrative_architect import PROMPT as ARCHITECT_PROMPT
from prompt.prompt_config import TEXT_TONE

load_dotenv()


class NarrativeArchitect:
    def __init__(self, model="google/gemini-3-pro-preview"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = model

    def generate_script(self, topic):
        print(f"📖 [1/3] 正在构思剧本: {topic}...")

        # 组装完整 Prompt
        full_prompt = ARCHITECT_PROMPT.replace("{TEXT_TONE}", TEXT_TONE).replace("{TOPIC}", topic)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/YourProject",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "response_format": {"type": "json_object"}  # 强制 JSON 模式
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']

            # 简单的清洗逻辑
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")

            script_json = json.loads(content)

            # 保存结果
            with open("narrative_output.json", "w", encoding="utf-8") as f:
                json.dump(script_json, f, ensure_ascii=False, indent=2)

            print(f"✅ 剧本生成完毕，共 {len(script_json)} 页。已保存至 narrative_output.json")
            return script_json

        except Exception as e:
            print(f"❌ 剧本生成失败: {e}")
            return None


if __name__ == "__main__":
    architect = NarrativeArchitect()
    architect.generate_script("大班数学：认识时钟")
