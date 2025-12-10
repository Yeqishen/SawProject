# -*- coding: utf-8 -*-
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from prompt.narrative_architect import PROMPT

# 加载环境变量（指定 .env 文件的完整路径）
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

def call_gemini(topic: str, output_file: str = "output.json"):
    """
    调用 Gemini API 生成教学故事脚本

    Args:
        topic: 主题内容
        output_file: 输出的 JSON 文件路径
    """
    # 配置 API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("未找到 GOOGLE_API_KEY，请检查 .env 文件")

    genai.configure(api_key=api_key)

    # 使用 gemini-exp-1206 模型
    model = genai.GenerativeModel('gemini-exp-1206')

    # 构建完整提示
    full_prompt = f"{PROMPT}\n\n[主题]: {topic}"

    print(f"正在调用 Gemini API，主题: {topic}")

    # 调用 API
    response = model.generate_content(full_prompt)

    # 解析响应
    result_text = response.text.strip()

    # 尝试解析为 JSON
    try:
        # 移除可能的 markdown 标记
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        result_json = json.loads(result_text)

        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)

        print(f"✓ 成功生成并保存到 {output_file}")
        return result_json

    except json.JSONDecodeError as e:
        print(f"✗ JSON 解析失败: {e}")
        # 保存原始响应
        with open(output_file.replace('.json', '_raw.txt'), 'w', encoding='utf-8') as f:
            f.write(result_text)
        print(f"原始响应已保存到 {output_file.replace('.json', '_raw.txt')}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='调用 Gemini API 生成教学故事脚本')
    parser.add_argument('topic', nargs='?', default="认识数字 1-10", help='教学主题')
    parser.add_argument('-o', '--output', default="narrative_output.json", help='输出文件路径')

    args = parser.parse_args()
    call_gemini(args.topic, args.output)
