# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- 模型配置路由 ---
MODEL_CONFIG = {
    # 1. 法官 (Judge) -> 使用 DeepSeek
    "judge": {
        "api_key": os.getenv("DEEPSEEK_API_KEY"),
        "base_url": "https://api.deepseek.com",  # DeepSeek 官方接口
        "model": "deepseek-chat"  # DeepSeek V3
    },

    # 2. 律师 (Lawyer) -> 使用 高级版 Qwen (Qwen-Plus/Max)
    "lawyer": {
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",  # 阿里云 OpenAI 兼容接口
        "model": "qwen-plus"  # 通义千问-Plus (能力强，适合逻辑攻防)
    },

    # 3. 陪审团 (Jury) -> 使用 低级版 Qwen (Qwen-Turbo)
    "jury": {
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo"  # 通义千问-Turbo (速度快，便宜，适合扮演普通人)
    }
}