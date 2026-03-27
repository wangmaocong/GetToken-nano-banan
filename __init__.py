from .banana_nodes import GetTokenBananaNode

NODE_CLASS_MAPPINGS = {
    "GetToken_Banana_Ultimate": GetTokenBananaNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GetToken_Banana_Ultimate": "🍌 GetToken NanoBanana ",
}

# ✨ 新增：告诉 ComfyUI 去加载 js 文件夹里的前端界面脚本
WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]