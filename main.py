from core.step_generate_script import NarrativeArchitect
from core.visual_engineer import VisualEngineer
from core.asset_generator import AssetGenerator

def main(topic: str, skip_gen: bool=False):
    print("🚀 系统启动...")

    # Step 1: 生成剧本
    architect = NarrativeArchitect()
    script = architect.generate_script(topic)
    if not script:
        return

    # Step 2: 拆解素材
    engineer = VisualEngineer()
    assets = engineer.analyze_assets()
    if not assets:
        return

    # Step 3: 生产图片
    if not skip_gen:
        generator = AssetGenerator()
        generator.run()
    else:
        print("⏩ 已跳过图片生成步骤。")

if __name__ == "__main__":
    t = "大班第一学期数学：奖牌数一数"
    main(topic=t)