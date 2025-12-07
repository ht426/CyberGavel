# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- 模型池定义 ---
# 格式: "UI显示名称": { "env_key": 环境变量名, "base_url": API地址, "model": 模型ID }
AVAILABLE_MODELS = {
    "DeepSeek-Chat": {
        "env_key": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat"
    },
    "Qwen-Plus ": {
        "env_key": "DASHSCOPE_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus"
    },
    "Qwen-Turbo ": {
        "env_key": "DASHSCOPE_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo"
    },
    "Kimi-K2-Turbo-Preview": {
        "env_key": "MOONSHOT_API_KEY",
        "base_url": "https://api.moonshot.cn/v1",
        "model": "kimi-k2-turbo-preview"
    },
    "GLM-4.6": {
        "env_key": "ZHIPU_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "model": "glm-4.6"
    },
}


def get_model_config(model_name):
    """根据UI选择的名称，返回具体的配置字典"""
    config_template = AVAILABLE_MODELS.get(model_name)
    if not config_template:
        raise ValueError(f"未知的模型名称: {model_name}")

    api_key = os.getenv(config_template["env_key"])

    return {
        "api_key": api_key,
        "base_url": config_template["base_url"],
        "model": config_template["model"],
        "name": model_name,  # 用于UI显示
        "env_key_name": config_template["env_key"]  # 用于报错提示
    }