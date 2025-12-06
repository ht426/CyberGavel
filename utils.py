# utils.py
from openai import OpenAI
from config import MODEL_CONFIG


def get_client(role_type):
    """根据角色类型，创建对应的 OpenAI Client"""
    config = MODEL_CONFIG.get(role_type)
    if not config or not config["api_key"]:
        raise ValueError(f"🚨 配置错误: 找不到角色 '{role_type}' 的 API Key，请检查 .env 文件")

    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    ), config["model"]


def get_ai_response(system_prompt, user_content, role_type="jury"):
    """
    通用调用函数，支持多模型路由
    role_type: 'judge' | 'lawyer' | 'jury'
    """
    try:
        client, model_name = get_client(role_type)

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7  # 稍微降低一点温度，保证稳定性
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"🚨 模型调用失败 ({role_type}): {str(e)}"