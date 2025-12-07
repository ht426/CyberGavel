# main.py
import streamlit as st
import time
import styles
from utils import get_ai_response
from prompts import LAWYER_PROMPTS, JURY_PERSONAS, JUDGE_PROMPT
# 【新增】引入配置文件的模型池和获取函数
from config import AVAILABLE_MODELS, get_model_config

st.set_page_config(page_title="CyberGavel", page_icon="⚖️", layout="wide")
styles.apply_custom_css()

# ==========================================
# 侧边栏：模型选角中心
# ==========================================
with st.sidebar:
    st.title("⚙️ 庭审配置中心")

    # 1. 获取所有可用模型的名称列表 (来自 config.py)
    model_names = list(AVAILABLE_MODELS.keys())

    st.markdown("### 1. 法官设置")
    # 默认 index=0 (通常是 DeepSeek)
    judge_model_name = st.selectbox("👨‍⚖️ 法官模型", model_names, index=0)

    st.markdown("### 2. 律师设置")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        # 默认 index=1 (通常是 Qwen-Plus)
        plaintiff_model_name = st.selectbox("🦁 原告模型", model_names, index=1)
    with col_l2:
        defendant_model_name = st.selectbox("🦈 被告模型", model_names, index=1)

    st.markdown("### 3. 陪审团与流程")
    rounds = st.slider("🗣️ 辩论回合数", 1, 4, 2)

    # 使用 Expander 折叠陪审团详细配置，避免侧边栏过长
    jury_configs = {}
    with st.expander("👥 点击配置 5 位陪审员模型", expanded=False):
        for persona in JURY_PERSONAS:
            # 默认给陪审团选稍微便宜或快速的模型 (index=2, e.g., Qwen-Turbo or Kimi)
            selected = st.selectbox(
                f"{persona['avatar']} {persona['name']}",
                model_names,
                index=2,
                key=f"jury_{persona['id']}"
            )
            jury_configs[persona['id']] = selected

st.title("⚖️ 赛博公堂")
st.caption(f"当前裁判: {judge_model_name} | 控方: {plaintiff_model_name} vs 辩方: {defendant_model_name}")

# ==========================================
# 核心逻辑：准备配置对象
# ==========================================
# 在循环开始前，先把用户选的名字转换成 config.py 里的配置字典
# 这样如果缺少 API Key，在这里就会报错提示，而不是等到运行一半时报错
try:
    CONFIGS = {
        "judge": get_model_config(judge_model_name),
        "plaintiff": get_model_config(plaintiff_model_name),
        "defendant": get_model_config(defendant_model_name),
        "jury": {pid: get_model_config(m_name) for pid, m_name in jury_configs.items()}
    }
except ValueError as e:
    st.error(str(e))
    st.stop()  # 如果配置有误（如缺Key），停止运行

# ==========================================
# 输入区域
# ==========================================
topic = st.text_input("📝 输入案件争议焦点：", value="AI生成的画作版权应该归属于提示词作者吗？")
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

        # --- 原告发言 ---
        with col_p:
            prompt = f"话题：'{topic}'。请开篇立论。" if i == 0 else f"话题：'{topic}'。对方说：'{last_argument}'。请反驳！"

            with st.spinner(f"🦁 原告 ({plaintiff_model_name}) 发言中..."):
                # 【修改】传入具体的配置字典 CONFIGS["plaintiff"]
                p_msg = get_ai_response(LAWYER_PROMPTS["plaintiff"], prompt, CONFIGS["plaintiff"])

                last_argument = p_msg
                full_transcript += f"\n[原告]: {p_msg}"

                # 【修改】传入模型名称用于 UI 显示
                st.markdown(styles.render_lawyer_message("plaintiff", p_msg, plaintiff_model_name),
                            unsafe_allow_html=True)

        # --- 被告发言 ---
        with col_d:
            prompt = f"话题：'{topic}'。原告说：'{last_argument}'。请反驳并立论。" if i == 0 else f"话题：'{topic}'。原告反驳：'{last_argument}'。请回击！"

            with st.spinner(f"🦈 被告 ({defendant_model_name}) 反击中..."):
                # 【修改】传入具体的配置字典 CONFIGS["defendant"]
                d_msg = get_ai_response(LAWYER_PROMPTS["defendant"], prompt, CONFIGS["defendant"])

                last_argument = d_msg
                full_transcript += f"\n[被告]: {d_msg}"

                # 【修改】传入模型名称用于 UI 显示
                st.markdown(styles.render_lawyer_message("defendant", d_msg, defendant_model_name),
                            unsafe_allow_html=True)

    # ==========================================
    # Phase 2: 陪审团投票
    # ==========================================
    st.markdown("---")
    st.subheader("👥 Phase 2: 陪审团合议")

    jury_progress_bar = st.progress(0, text="陪审团正在入场...")
    jury_opinions = []
    jury_cols = st.columns(len(JURY_PERSONAS))

    for idx, persona in enumerate(JURY_PERSONAS):
        jury_progress_bar.progress((idx + 1) / len(JURY_PERSONAS), text=f"正在听取 {persona['name']} 的意见...")

        with jury_cols[idx]:
            # 获取当前陪审员对应的配置
            current_jury_conf = CONFIGS["jury"][persona['id']]
            model_display_name = current_jury_conf['name']

            with st.spinner(f"{persona['name']} ({model_display_name}) 思考中..."):
                prompt = f"庭审记录片段：...{full_transcript[-1000:]}\n\n请用你的风格（{persona['style']}）点评并投票。"

                # 【修改】传入该陪审员特定的模型配置
                content = get_ai_response(persona['prompt'], prompt, current_jury_conf)

                jury_opinions.append(f"【陪审员-{persona['name']}】: {content}")

                # 【修改】UI 渲染
                st.markdown(styles.render_jury_card(persona['name'], persona['avatar'], content, model_display_name),
                            unsafe_allow_html=True)

                time.sleep(0.2)

    jury_progress_bar.progress(1.0, text="陪审团合议完毕。")
    time.sleep(1)
    jury_progress_bar.empty()

    # ==========================================
    # Phase 3: 法官判决
    # ==========================================
    st.markdown("---")
    st.subheader("⚖️ Phase 3: 最终判决")

    with st.status(f"👨‍⚖️ 法官 ({judge_model_name}) 正在审阅卷宗...", expanded=True) as status:
        st.write("✅ 已阅读双方律师辩词")
        st.write(f"✅ 已听取 {len(jury_opinions)} 位陪审员的投票意见")

        judge_prompt_content = f"""
            {full_transcript}
            ================================================
            【重要参考】陪审团的投票与意见如下：
            {chr(10).join(jury_opinions)}
            ================================================
            请结合上述辩论记录和陪审团的民意，做出最终判决。
            请使用清晰的 Markdown 格式（使用 ### 做小标题，**做加粗**）。
            """

        # 【修改】传入法官配置
        verdict = get_ai_response(JUDGE_PROMPT, judge_prompt_content, CONFIGS["judge"])

        status.update(label="判决已生成", state="complete", expanded=False)

    # 渲染
    st.markdown(styles.render_verdict(verdict), unsafe_allow_html=True)

    # ==========================================
    # Phase 4: 导出
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    col_empty, col_btn = st.columns([4, 1])

    with col_btn:
        html_data = styles.get_verdict_download_html(verdict)
        st.download_button(
            label="📥 导出判决书 (HTML)",
            data=html_data,
            file_name="AI_Court_Verdict.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )