# utils.py
from openai import OpenAI

def get_client(model_conf):
    """创建 OpenAI Client"""
    if not model_conf or not model_conf.get("api_key"):
        raise ValueError(f"⚠️ 模型 '{model_conf.get('name')}' 未配置 API Key。\n请在 .env 文件中检查 {model_conf.get('env_key_name')}")

    return OpenAI(
        api_key=model_conf["api_key"],
        base_url=model_conf["base_url"]
    )

def get_ai_response(system_prompt, user_content, model_conf):
    """
    通用调用函数
    model_conf: 包含 api_key, base_url, model, name
    """
    try:
        client = get_client(model_conf)

        response = client.chat.completions.create(
            model=model_conf["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # 返回错误信息而不是崩溃，方便前端展示
        return f"🚨 **Error ({model_conf.get('name')}):** {str(e)}"