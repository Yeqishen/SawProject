# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

from prompt.prompt_config import TEXT_TONE

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent

from prompt.narrative_architect import PROMPT

# 加载环境变量（指定 .env 文件的完整路径）
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

def call_openrouter(topic: str, output_file: str = "output.json", model: str = "gemini-3-pro-preview"):
    """
    调用 OpenRouter API 生成教学故事脚本

    Args:
        topic: 主题内容
        output_file: 输出的 JSON 文件路径
        model: 使用的模型名称（默认：gemini-3-pro-preview）
               常用模型：
               - gemini-3-pro-preview (高性价比推理模型)
    """
    # 配置 API
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("未找到 OPENROUTER_API_KEY，请检查 .env 文件")

    # OpenRouter API 端点
    url = "https://openrouter.ai/api/v1/chat/completions"

    # 构建完整提示
    full_prompt = PROMPT.format(TEXT_TONE=TEXT_TONE, TOPIC=topic)

    # 构建请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/SawProject",  # 可选，用于分析
        "X-Title": "Teaching Story Script Generator"  # 可选，用于在 OpenRouter 仪表板显示
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 20000
    }

    print(f"正在调用 OpenRouter API")
    print(f"模型: {model}")
    print(f"主题: {topic}")
    print("-" * 50)

    # 调用 API
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()  # 检查 HTTP 错误

        response_data = response.json()

        # 提取生成的文本
        if 'choices' not in response_data or len(response_data['choices']) == 0:
            raise ValueError(f"API 响应格式异常: {response_data}")

        result_text = response_data['choices'][0]['message']['content'].strip()

        # 显示使用统计
        if 'usage' in response_data:
            usage = response_data['usage']
            print(f"\n使用统计:")
            print(f"  输入 tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"  输出 tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"  总计 tokens: {usage.get('total_tokens', 'N/A')}")

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

            # 确保输出目录存在
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 保存到文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_json, f, ensure_ascii=False, indent=2)

            print(f"\n✓ 成功生成并保存到 {output_file}")
            return result_json

        except json.JSONDecodeError as e:
            print(f"\n✗ JSON 解析失败: {e}")
            # 保存原始响应
            raw_file = output_file.replace('.json', '_raw.txt')
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(result_text)
            print(f"原始响应已保存到 {raw_file}")
            raise

    except requests.exceptions.RequestException as e:
        print(f"\n✗ API 请求失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"错误详情: {e.response.text}")
        raise


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='调用 OpenRouter API 生成教学故事脚本')
    parser.add_argument('topic', nargs='?', default="大班第一学期数学：奖牌数一数，写一篇教案", help='教学主题')
    parser.add_argument('-o', '--output', default="narrative_output.json", help='输出文件路径')
    parser.add_argument('-m', '--model', default="google/gemini-3-pro-preview",
                        help='模型名称（默认: gemini-3-pro-preview）')

    args = parser.parse_args()

    call_openrouter(args.topic, args.output, args.model)
