# styles.py
import streamlit as st
import markdown  # 【必须确保安装：pip install markdown】
from datetime import datetime  # 引入时间模块


def apply_custom_css():
    st.markdown("""
    <style>
    /* 全局重置 */
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }


    /* 修改侧边栏宽度*/
    /* ============================================================ */
    section[data-testid="stSidebar"] {
        width: 400px !important;      /* 设置为你想要的宽度 */
        min-width: 400px !important;  /* 锁死最小宽度 */
        max-width: 400px !important;  /* 锁死最大宽度 */
    }
    /* ============================================================ */
    
    /* 滚动条美化 */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #888; }

    /* 输入框与按钮修正 */
    .stTextInput > label { color: #fff; font-weight: bold; margin-bottom: 5px; }
    div[data-testid="stTextInput"] { margin-bottom: -15px !important; }
    div[data-testid="stButton"] > button { width: 100%; border-radius: 0 0 8px 8px; background: #ff4b4b; border: none; color: white; font-weight: bold;}

    /* --- 通用文字容器 --- */
    .html-content {
        font-size: 0.95rem;
        line-height: 1.6;
        text-align: justify;
    }
    .html-content p { margin-bottom: 0.8em; margin-top: 0; }
    .html-content ul, .html-content ol { padding-left: 20px; margin-bottom: 10px; }
    .html-content li { margin-bottom: 5px; }
    .html-content strong { color: #ffeb3b; font-weight: 900; }
    .html-content h1, .html-content h2, .html-content h3 { 
        color: #fff; margin-top: 15px; margin-bottom: 10px; font-size: 1.1em; 
        border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 5px;
    }

    /* --- 律师卡片 --- */
    .lawyer-box {
        height: 600px;
        overflow-y: auto;
        border-radius: 12px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        position: relative;
        background-color: #1e2025;
    }

    .lawyer-header {
        position: sticky;
        top: 0;
        z-index: 100;
        padding: 15px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-weight: bold;
        font-size: 1.1em;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .lawyer-body { padding: 20px; padding-top: 10px; }

    /* 原告/被告 配色 */
    .plaintiff-box { border: 1px solid #ff4d6d; }
    .plaintiff-header { background: linear-gradient(90deg, #3b1e22, #1a1a2e); color: #ff4d6d; border-bottom: 2px solid #ff4d6d; }

    .defendant-box { border: 1px solid #4cc9f0; }
    .defendant-header { background: linear-gradient(90deg, #162447, #1a1a2e); color: #4cc9f0; border-bottom: 2px solid #4cc9f0; }

    /* --- 陪审团卡片 --- */
    .jury-card {
        background: #1f4068;
        border: 1px solid #30475e;
        border-radius: 10px;
        height: 500px;
        overflow-y: auto;
        position: relative;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    .jury-header {
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: #1f4068;
        padding: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 4px rgba(0,0,0,0.1);
    }

    .jury-body { padding: 15px; padding-top: 10px; }
    .jury-name { font-weight: bold; color: #f05454; font-size: 1.1em; }
    .jury-emoji { font-size: 24px; }

    /* 模型标签样式 */
    .model-tag {
        font-size: 0.7em; 
        background: rgba(255,255,255,0.1); 
        padding: 2px 6px; 
        border-radius: 4px; 
        border: 1px solid rgba(255,255,255,0.2);
        color: #ccc;
        font-weight: normal;
    }

    /* --- 判决书 --- */
    .verdict-container { display: block; padding: 20px 0; width: 100%; }
    .verdict-paper {
        background-color: #fdfbf7;
        color: #2c3e50;
        padding: 40px;
        width: 100%;
        max-width: none;
        border: 1px solid #dcdcdc;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-family: 'Georgia', serif;
        border-radius: 12px;
    }
    .verdict-content h1, .verdict-content h2, .verdict-content h3 {
        color: #2c3e50; border-bottom: 2px solid #8d6e63; margin-top: 30px; padding-bottom: 10px; font-family: sans-serif;
    }
    .verdict-content strong { color: #d35400; font-weight: bold; }
    .verdict-content p { margin-bottom: 1em; line-height: 1.8; font-size: 1.05rem; }
    </style>
    """, unsafe_allow_html=True)


def md_to_html(text):
    if not text: return ""
    return markdown.markdown(text, extensions=['nl2br', 'sane_lists'])


# 【修改点 1】增加了 model_name 参数，并显示在右上角
def render_lawyer_message(role, content, model_name="AI Model"):
    # 生成右上角的模型标签
    tag = f'<span class="model-tag">{model_name}</span>'

    if "Error" in content:
        content_html = "<div style='color:red; font-weight:bold;'>⚠️ 律师信号中断 (API Error)</div>"
    else:
        content_html = md_to_html(content)

    if role == "plaintiff":
        return f"""
        <div class="lawyer-box plaintiff-box">
            <div class="lawyer-header plaintiff-header">
                <span>🦁 原告律师</span>
                {tag}
            </div>
            <div class="lawyer-body html-content">
                {content_html}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="lawyer-box defendant-box">
            <div class="lawyer-header defendant-header">
                <span>被告律师 🦈</span>
                {tag}
            </div>
            <div class="lawyer-body html-content">
                {content_html}
            </div>
        </div>
        """


# 【修改点 2】增加了 model_name 参数，显示在名字旁边
def render_jury_card(name, avatar, content, model_name="AI"):
    content_html = md_to_html(content)

    return f"""
    <div class="jury-card">
        <div class="jury-header">
            <div>
                <div class="jury-name">{name}</div>
                <div style="font-size:0.7em; color:#aaa; margin-top:2px;">Using: {model_name}</div>
            </div>
            <div class="jury-emoji">{avatar}</div>
        </div>
        <div class="jury-body html-content">
            {content_html}
        </div>
    </div>
    """


def render_verdict(content):
    content_html = md_to_html(content)
    return f"""
    <div class="verdict-container">
        <div class="verdict-paper">
            <div style="text-align:center; margin-bottom:40px;">
                <h1 style="margin:0; font-size:2.5em; color:#2c3e50;">⚖️ 最终判决书</h1>
                <div style="color:#7f8c8d; font-size:0.9em; margin-top:10px;">CyberGavel • 案件编号 #2025-001</div>
            </div>
            <hr style="border:0; border-top:1px solid #eee; margin-bottom:30px;">
            <div class="verdict-content">
                {content_html}
            </div>
            <div style="margin-top:60px; text-align:right;">
                <div style="font-family: cursive; font-size:1.5em; color:#2c3e50;">Judge CyberGavel</div>
                <div style="color:#999; font-size:0.8em;">Electronic Signature Valid</div>
            </div>
        </div>
    </div>
    """


def get_verdict_download_html(content):
    content_html = md_to_html(content)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>AI 法庭判决书</title>
        <style>
            body {{
                font-family: 'Georgia', 'SimSun', serif;
                background-color: #f0f2f6;
                display: flex;
                justify-content: center;
                padding: 40px;
                margin: 0;
            }}
            .verdict-paper {{
                background-color: #fdfbf7;
                color: #2c3e50;
                padding: 60px;
                width: 100%;
                max-width: 900px;
                border: 1px solid #dcdcdc;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            h1 {{ text-align: center; color: #2c3e50; border-bottom: 3px double #8d6e63; padding-bottom: 20px; margin-bottom: 30px; }}
            h2, h3 {{ color: #2c3e50; border-left: 5px solid #8d6e63; padding-left: 15px; margin-top: 30px; }}
            p {{ line-height: 1.8; font-size: 16px; margin-bottom: 15px; text-align: justify; }}
            strong {{ color: #d35400; font-weight: 900; }}
            ul, ol {{ background: rgba(0,0,0,0.03); padding: 20px 40px; border-radius: 5px; }}
            .footer {{ margin-top: 60px; text-align: right; font-family: cursive; color: #555; }}
            .watermark {{ text-align: center; color: #ccc; font-size: 12px; margin-top: 50px; border-top: 1px solid #eee; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="verdict-paper">
            <h1>⚖️ AI 法庭最终判决书</h1>
            <div>{content_html}</div>
            <div class="footer">
                <div style="font-size: 24px;">Judge CyberGavel</div>
                <div style="font-size: 14px;">Electronic Signature Verified ✅</div>
                <div>{now_str}</div>
            </div>
            <div class="watermark">Generated by CyberGavel</div>
        </div>
    </body>
    </html>
    """