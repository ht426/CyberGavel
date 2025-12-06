# styles.py
import streamlit as st
import markdown  # 【必须确保安装：pip install markdown】


def apply_custom_css():
    st.markdown("""
    <style>
    /* 全局重置 */
    .stApp { background-color: #1a1a2e; color: #e0e0e0; }

    /* 滚动条美化 (Chrome/Safari) */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #555; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #888; }

    /* 输入框与按钮修正 */
    .stTextInput > label { color: #fff; font-weight: bold; margin-bottom: 5px; }
    div[data-testid="stTextInput"] { margin-bottom: -15px !important; }
    div[data-testid="stButton"] > button { width: 100%; border-radius: 0 0 8px 8px; background: #ff4b4b; border: none; color: white; font-weight: bold;}

    /* --- 通用文字容器 (解析后的HTML样式) --- */
    .html-content {
        font-size: 0.95rem;
        line-height: 1.6;
        text-align: justify;
        /* 修复 Markdown 转 HTML 后的默认边距问题 */
        & p { margin-bottom: 0.8em; margin-top: 0; }
        & ul, & ol { padding-left: 20px; margin-bottom: 10px; }
        & li { margin-bottom: 5px; }
        & strong { color: #ffeb3b; font-weight: 900; } /* 重点文字高亮 */
        & h1, & h2, & h3 { color: #fff; margin-top: 15px; margin-bottom: 10px; font-size: 1.1em; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 5px;}
    }

    /* --- 律师卡片 --- */
    .lawyer-box {
        height: 600px;
        overflow-y: auto;
        border-radius: 12px;
        padding: 0; /* padding 移到内部，防止滚动条在 padding 里面 */
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
        position: relative; /* 为 sticky 定位做基准 */
        background-color: #1e2025; /* 兜底背景 */
    }

    .lawyer-header {
        position: sticky;
        top: 0;
        z-index: 100; /* 确保层级最高，压住文字 */
        padding: 15px 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-weight: bold;
        font-size: 1.1em;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .lawyer-body {
        padding: 20px; /* 文字内容的内边距 */
        padding-top: 10px;
    }

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
        z-index: 100; /* 必须比文字高 */
        background-color: #1f4068; /* 背景色必须不透明！否则文字会透出来 */
        padding: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 4px rgba(0,0,0,0.1); /* 加一点阴影遮挡下滚文字的边缘 */
    }

    .jury-body {
        padding: 15px;
        padding-top: 10px;
    }

    .jury-name { font-weight: bold; color: #f05454; font-size: 1.1em; }
    .jury-emoji { font-size: 24px; }

    /* --- 判决书优化 (修改为全宽版) --- */
    .verdict-container {
        display: block; /* 【修改】不再使用 flex 居中 */
        padding: 20px 0;
        width: 100%;    /* 【修改】容器全宽 */
    }

    .verdict-paper {
        background-color: #fdfbf7; /* 纸张白 */
        color: #2c3e50;
        padding: 40px;      /* 稍微减小一点 padding */
        width: 100%;        /* 【修改】宽度100% */
        max-width: none;    /* 【关键修改】去掉了 800px 限制，改为无限制 */
        border: 1px solid #dcdcdc;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        font-family: 'Georgia', serif; /* 衬线体，更像文档 */
        border-radius: 12px; /* 【修改】圆角和上面的卡片保持一致 */
    }

    /* 判决书内部 Markdown 样式覆盖 */
    .verdict-content h1, .verdict-content h2, .verdict-content h3 {
        color: #2c3e50; /* 标题颜色变深 */
        border-bottom: 2px solid #8d6e63;
        margin-top: 30px;
        padding-bottom: 10px;
        font-family: sans-serif;
    }
    .verdict-content strong {
        color: #d35400; /* 重点文字颜色 */
        font-weight: bold;
    }
    .verdict-content p {
        margin-bottom: 1em;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 辅助函数：Markdown 转 HTML ---
def md_to_html(text):
    if not text: return ""
    # 使用 markdown 库转换，extensions 处理列表和换行
    html = markdown.markdown(text, extensions=['nl2br', 'sane_lists'])
    return html


def render_lawyer_message(role, content):
    tag = '<span style="font-size:0.7em; background:rgba(255,255,255,0.1); padding:2px 6px; border-radius:4px;">Qwen-Plus</span>'

    if "Error" in content:
        content_html = "<div style='color:red; font-weight:bold;'>⚠️ 律师信号中断 (API Error)</div>"
    else:
        # 【关键修复】先把 AI 的 Markdown 转成 HTML
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


def render_jury_card(name, avatar, content):
    # 【关键修复】转 HTML
    content_html = md_to_html(content)

    return f"""
    <div class="jury-card">
        <div class="jury-header">
            <div class="jury-name">{name}</div>
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


# styles.py (保留上面的代码，在最下方增加这个新函数)

# ... (上面的 render_verdict 等函数保持不变) ...

# 【新增】生成用于下载的完整 HTML 文件内容
def get_verdict_download_html(content):
    # 将 Markdown 转为 HTML
    content_html = md_to_html(content)

    # 这是一个完整的 HTML 模板，包含了 CSS 样式
    # 这样用户下载后，离线打开依然好看
    return f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>DeepSeek AI 法庭判决书</title>
        <style>
            body {{
                font-family: 'Georgia', 'SimSun', serif; /* 衬线体，更有正式感 */
                background-color: #f0f2f6;
                display: flex;
                justify-content: center;
                padding: 40px;
                margin: 0;
            }}
            .verdict-paper {{
                background-color: #fdfbf7; /* 纸张米色 */
                color: #2c3e50;
                padding: 60px;
                width: 100%;
                max-width: 900px; /* 离线文档建议限制宽度，类似A4纸，方便阅读和打印 */
                border: 1px solid #dcdcdc;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            h1 {{
                text-align: center;
                color: #2c3e50;
                border-bottom: 3px double #8d6e63;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            h2, h3 {{
                color: #2c3e50;
                border-left: 5px solid #8d6e63;
                padding-left: 15px;
                margin-top: 30px;
            }}
            p {{
                line-height: 1.8;
                font-size: 16px;
                margin-bottom: 15px;
                text-align: justify;
            }}
            strong {{
                color: #d35400; /* 重点高亮颜色 */
                font-weight: 900;
            }}
            ul, ol {{
                background: rgba(0,0,0,0.03);
                padding: 20px 40px;
                border-radius: 5px;
            }}
            .footer {{
                margin-top: 60px;
                text-align: right;
                font-family: cursive;
                color: #555;
            }}
            .watermark {{
                text-align: center;
                color: #ccc;
                font-size: 12px;
                margin-top: 50px;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="verdict-paper">
            <h1>⚖️ AI 法庭最终判决书</h1>

            <div>
                {content_html}
            </div>

            <div class="footer">
                <div style="font-size: 24px;">Judge CyberGavel</div>
                <div style="font-size: 14px;">Electronic Signature Verified ✅</div>
                <div>{import_datetime()}</div>
            </div>

            <div class="watermark">
                Generated by CyberGavel • 此判决由 AI 生成，仅供娱乐
            </div>
        </div>
    </body>
    </html>
    """


# 辅助函数：获取当前时间（为了放在 HTML 里）
def import_datetime():
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

