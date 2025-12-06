# main.py
import streamlit as st
import time
import styles
from utils import get_ai_response
from prompts import LAWYER_PROMPTS, JURY_PERSONAS, JUDGE_PROMPT

st.set_page_config(page_title="CyberGavel", page_icon="⚖️", layout="wide")
styles.apply_custom_css()

# --- 侧边栏 ---
with st.sidebar:
    st.title("⚙️ 系统架构")
    st.info("🧠 **法官**")
    st.info("⚔️ **律师**")
    st.info("👥 **陪审团**")

    rounds = st.slider("辩论回合数", 1, 4, 2)

st.title("⚖️ 赛博公堂 ")
st.caption("Architecture: DeepSeek (Reasoning) + Qwen (Roleplay)")

# --- 输入区域 (保持之前的垂直贴合布局) ---
topic = st.text_input("📝 输入案件争议焦点：", value="程序员写Bug是否应该自己负责？")
start_btn = st.button("🔥 开庭审理", type="primary", use_container_width=True)

if start_btn and topic:
    full_transcript = f"案件：{topic}\n"
    last_argument = ""

    # ==========================================
    # Phase 1: 律师辩论
    # ==========================================
    st.subheader("⚔️ Phase 1: 控辩双方")
    st.progress(0.3)

    for i in range(rounds):
        col_p, col_d = st.columns(2)

        # 原告发言
        with col_p:
            prompt = f"话题：'{topic}'。请开篇立论。" if i == 0 else f"话题：'{topic}'。对方说：'{last_argument}'。请反驳！"
            with st.spinner("🦁 原告律师整理证据中..."):
                p_msg = get_ai_response(LAWYER_PROMPTS["plaintiff"], prompt, role_type="lawyer")
                last_argument = p_msg
                full_transcript += f"\n[原告]: {p_msg}"
                st.markdown(styles.render_lawyer_message("plaintiff", p_msg), unsafe_allow_html=True)

        # 被告发言
        with col_d:
            prompt = f"话题：'{topic}'。原告说：'{last_argument}'。请反驳并立论。" if i == 0 else f"话题：'{topic}'。原告反驳：'{last_argument}'。请回击！"
            with st.spinner("🦈 被告律师整理反击中..."):
                d_msg = get_ai_response(LAWYER_PROMPTS["defendant"], prompt, role_type="lawyer")
                last_argument = d_msg
                full_transcript += f"\n[被告]: {d_msg}"
                st.markdown(styles.render_lawyer_message("defendant", d_msg), unsafe_allow_html=True)

    # ==========================================
    # Phase 2: 陪审团投票 (动态过程)
    # ==========================================
    st.markdown("---")
    st.subheader("👥 Phase 2: 陪审团合议")

    # 创建进度条，增加仪式感
    jury_progress_bar = st.progress(0, text="陪审团正在入场...")

    jury_opinions = []

    # 预先创建好列容器，稍后一个个填充
    jury_cols = st.columns(len(JURY_PERSONAS))

    # 循环内逐个请求，逐个渲染，实现“动态投票”效果
    for idx, persona in enumerate(JURY_PERSONAS):
        # 更新进度条
        jury_progress_bar.progress((idx + 1) / len(JURY_PERSONAS), text=f"正在听取 {persona['name']} 的意见...")

        with jury_cols[idx]:
            # 这里显示局部 loading 状态
            with st.spinner(f"{persona['name']} 思考中..."):
                # 构建 Prompt
                prompt = f"庭审记录片段：...{full_transcript[-800:]}\n\n请用你的风格（{persona['style']}）点评并投票。"

                # 请求 AI
                content = get_ai_response(persona['prompt'], prompt, role_type="jury")

                # 收集意见用于发给法官
                jury_opinions.append(f"【陪审员-{persona['name']}】: {content}")

                # 【调用 styles 的渲染函数】确保对齐和美观
                st.markdown(styles.render_jury_card(persona['name'], persona['avatar'], content),
                            unsafe_allow_html=True)

                # 可选：稍微停顿 0.2秒，让视觉上更有“轮流发言”的节奏感
                time.sleep(0.2)

    jury_progress_bar.progress(1.0, text="陪审团合议完毕，已提交法官。")
    time.sleep(1)  # 停留一下让用户看到完成状态
    jury_progress_bar.empty()  # 隐藏进度条

    # ==========================================
    # Phase 3: 法官判决
    # ==========================================
    st.markdown("---")
    st.subheader("⚖️ Phase 3: 最终判决")

    with st.status("👨‍⚖️ 法官正在审阅卷宗...", expanded=True) as status:
        st.write("✅ 已阅读双方律师辩词")
        st.write(f"✅ 已听取 {len(jury_opinions)} 位陪审员的投票意见")
        st.write("🤔 正在进行最终法律裁定...")

        judge_prompt_content = f"""
            {full_transcript}

            ================================================
            【重要参考】陪审团的投票与意见如下：
            {chr(10).join(jury_opinions)}
            ================================================

            请结合上述辩论记录和陪审团的民意，做出最终判决。
            请使用清晰的 Markdown 格式（使用 ### 做小标题，**做加粗**）。
            """

        verdict = get_ai_response(JUDGE_PROMPT, judge_prompt_content, role_type="judge")

        status.update(label="判决已生成", state="complete", expanded=False)

    # 1. 渲染网页版判决书
    st.markdown(styles.render_verdict(verdict), unsafe_allow_html=True)

    # ==========================================
    # Phase 4: 导出功能 (新增)
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)  # 增加一点间距

    # 使用列布局，将按钮放在右侧，看起来更精致
    col_empty, col_btn = st.columns([4, 1])

    with col_btn:
        # 1. 获取带有完整 CSS 样式的 HTML 内容
        html_data = styles.get_verdict_download_html(verdict)

        # 2. 渲染下载按钮
        st.download_button(
            label="📥 导出判决书 (HTML)",
            data=html_data,
            file_name="AI_Court_Verdict.html",
            mime="text/html",
            use_container_width=True,  # 按钮填满这一列
            type="primary"  # 使用醒目的红色主色调
        )