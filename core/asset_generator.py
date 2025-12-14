# asset_generator.py
import os
import json
import requests
import fal_client
from pathlib import Path
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from io import BytesIO
from rembg import remove

load_dotenv()


class AssetGenerator:
    def __init__(self, output_dir="assets"):
        self.output_dir = Path(output_dir)
        self.bg_dir = self.output_dir / "backgrounds"
        self.char_dir = self.output_dir / "characters"
        self.prop_dir = self.output_dir / "props"

        # 确保目录结构存在
        for d in [self.bg_dir, self.char_dir, self.prop_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def _call_fal_flux(self, prompt, image_size="landscape_16_9"):
        """调用 Fal.ai Flux-1 Schnell"""
        # print(f"   Generating: {prompt[:40]}...") # 减少刷屏
        try:
            handler = fal_client.submit(
                "fal-ai/z-image/turbo",  # 或者 "fal-ai/flux-1/schnell" 视 API 变动而定
                arguments={
                    "prompt": prompt,
                    "image_size": image_size,
                    "num_inference_steps": 4,
                    "enable_safety_checker": False
                },
            )
            result = handler.get()
            return result['images'][0]['url']
        except Exception as e:
            print(f"   ⚠️ API Error: {e}")
            return None

    def _process_single_asset(self, item, category_type):
        """处理单个素材的任务函数"""

        # 1. 确定路径和参数
        if category_type == "background":
            folder = self.bg_dir
            filename = f"{item['id']}.png"  # 背景存 PNG 或 JPG 均可
            size = "landscape_16_9"
            need_rembg = False
        elif category_type == "character":
            folder = self.char_dir
            filename = f"{item['id']}.png"
            size = "portrait_4_3"  # 角色用竖屏
            need_rembg = True
        elif category_type == "prop":
            folder = self.prop_dir
            # 兼容 prop_id 或 asset_id
            pid = item.get('asset_id', item.get('id', 'unknown'))
            filename = f"{pid}.png"
            size = "square_hd"  # 道具用正方形
            need_rembg = True

        filepath = folder / filename

        if filepath.exists():
            print(f"   ⏩ 跳过已存在: {filename}")
            return

        # 2. 生成图片
        print(f"   🎨 生成中: {filename}")
        img_url = self._call_fal_flux(item['prompt'], image_size=size)

        if not img_url:
            return

        # 3. 下载与处理
        try:
            resp = requests.get(img_url)
            img = Image.open(BytesIO(resp.content))

            if need_rembg:
                # 抠图处理
                img = remove(img)  # RemBg 自动抠图

            img.save(filepath, "PNG")
            print(f"   ✅ 已保存: {filename}")

        except Exception as e:
            print(f"   ❌ 处理图片出错 {filename}: {e}")

    def run(self, input_file="assets_list.json"):
        print(f"🎨 [3/3] 启动素材生产工厂...")

        if not os.path.exists(input_file):
            print("❌ 找不到素材列表文件，请先运行步骤 2。")
            return

        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 使用线程池并行处理，加快速度
        # 注意：RemBg 在 CPU 上跑比较占资源，如果卡顿请调低 max_workers
        with ThreadPoolExecutor(max_workers=3) as executor:
            # 1. Backgrounds
            if 'backgrounds' in data:
                print("   --- 处理背景 ---")
                for item in data['backgrounds']:
                    executor.submit(self._process_single_asset, item, "background")

            # 2. Characters
            if 'character_sprites' in data:
                print("   --- 处理角色 ---")
                for item in data['character_sprites']:
                    executor.submit(self._process_single_asset, item, "character")

            # 3. Props
            if 'interactive_props' in data:
                print("   --- 处理道具 ---")
                for item in data['interactive_props']:
                    executor.submit(self._process_single_asset, item, "prop")

        print("🎉 所有素材生成完毕！请检查 assets 文件夹。")


if __name__ == "__main__":
    generator = AssetGenerator()
    generator.run()
