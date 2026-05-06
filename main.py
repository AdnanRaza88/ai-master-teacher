import streamlit as st
import time
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.core.config import APP_CONFIG
from app.services.ai_teacher import AITeacher
from app.ui.components import render_css, render_header, render_chat_bubble, render_sidebar

st.set_page_config(
    page_title="AI Master Teacher 2070",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_css()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "teacher" not in st.session_state:
    st.session_state.teacher = None
if "mode" not in st.session_state:
    st.session_state.mode = "Study Mode"
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False

mode, language = render_sidebar()
st.session_state.mode = mode

render_header()

# Model loader
if not st.session_state.model_loaded:
    with st.container():
        st.markdown('<div class="load-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="boot-card">
                <div class="boot-title">⚡ INITIALIZING GEMMA 4 CORE</div>
                <div class="boot-sub">Google Gemma-4-26B-A4B-it Loading...</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 BOOT AI CORE", key="boot_btn", use_container_width=True):
                progress = st.progress(0, text="Warming up quantum cores...")
                for i in range(0, 101, 5):
                    time.sleep(0.05)
                    msgs = {
                        0: "Loading tokenizer...", 20: "Mapping device layers...",
                        40: "Quantizing weights (4-bit)...", 60: "Warming up attention heads...",
                        80: "Calibrating teaching neurons...", 100: "GEMMA 4 ONLINE ✓"
                    }
                    progress.progress(i, text=msgs.get(i, f"Loading... {i}%"))

                try:
                    st.session_state.teacher = AITeacher(language=language)
                    st.session_state.model_loaded = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Model load failed: {e}")
                    st.info("💡 Make sure you're on Kaggle T4 GPU with internet ON for first run.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # Main chat area
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)

    # Streak bar
    streak_pct = min(st.session_state.streak * 10, 100)
    st.markdown(f"""
    <div class="streak-bar-container">
        <span class="streak-label">⚡ LEARNING STREAK</span>
        <div class="streak-track">
            <div class="streak-fill" style="width:{streak_pct}%"></div>
        </div>
        <span class="streak-count">{st.session_state.streak} exchanges</span>
    </div>
    """, unsafe_allow_html=True)

    # Chat history render
    for msg in st.session_state.messages:
        render_chat_bubble(msg["role"], msg["content"], msg.get("mode", "Study Mode"))

    st.markdown('</div>', unsafe_allow_html=True)

    # Input area
    st.markdown('<div class="input-zone">', unsafe_allow_html=True)
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        user_input = st.text_input(
            "",
            placeholder="🧠 Ask anything... Python, Physics, Philosophy, Maths, History...",
            key="user_input",
            label_visibility="collapsed"
        )
    with col_btn:
        send = st.button("⚡ ASK", use_container_width=True, key="send_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "mode": st.session_state.mode
        })

        with st.spinner("🧬 Gemma 4 is thinking..."):
            response = st.session_state.teacher.teach(
                question=user_input,
                history=st.session_state.messages[:-1],
                mode=st.session_state.mode
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "mode": st.session_state.mode
        })
        st.session_state.streak += 1
        st.rerun()
