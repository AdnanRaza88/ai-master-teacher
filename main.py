import streamlit as st
import time
import random
from app.core.config import settings
from app.services.llm_client import LLMClient
from app.services.ai_teacher import TeachingEngine

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="AI Master Teacher 2070",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# FUTURISTIC CSS & JS
# ------------------------------------------------------------------
def inject_css():
    st.markdown("""
    <style>
    /* Base */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Orbitron', sans-serif;
    }
    .stApp {
        background: transparent;
    }
    .bg-overlay {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at 20% 30%, #1a0033, #000510 80%);
        animation: bgMove 25s ease infinite alternate;
        z-index: -2;
    }
    @keyframes bgMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Floating particles */
    .particle-container {
        position: fixed; width: 100%; height: 100%; z-index: -1; overflow: hidden;
    }
    .particle {
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(#00ffff, #ff00c8);
        opacity: 0.5;
        animation: floatUp linear infinite;
    }
    @keyframes floatUp {
        0% { transform: translateY(100vh) scale(0); opacity: 0; }
        10% { opacity: 0.7; }
        90% { opacity: 0.7; }
        100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
    }

    /* Glass panels */
    .glass-panel {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(18px);
        border: 1px solid rgba(0, 255, 255, 0.12);
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.1), 0 8px 30px rgba(0,0,0,0.5);
        transition: all 0.3s ease;
    }
    .glass-panel:hover {
        box-shadow: 0 0 45px rgba(255, 0, 200, 0.25), 0 8px 30px rgba(0,0,0,0.5);
        border-color: rgba(255, 0, 200, 0.4);
    }

    /* Chat bubbles */
    .chat-row {
        display: flex;
        margin: 1rem 0;
    }
    .user-row { justify-content: flex-end; }
    .ai-row { justify-content: flex-start; }
    .bubble {
        max-width: 75%;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        font-size: 1rem;
        line-height: 1.5;
        animation: bubblePop 0.4s ease-out;
    }
    @keyframes bubblePop {
        0% { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .user-bubble {
        background: linear-gradient(135deg, #ff00c8, #00d4ff);
        color: #0a0a0f;
        border-bottom-right-radius: 5px;
        box-shadow: 0 0 25px #ff00c8aa, 0 8px 20px #000;
    }
    .ai-bubble {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-bottom-left-radius: 5px;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
        color: #d0d0ff;
    }

    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 0.5rem 0;
    }
    .typing-indicator span {
        width: 8px; height: 8px;
        background: #00ffff;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
        box-shadow: 0 0 10px #00ffff;
    }
    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }

    /* Message sections */
    .msg-section {
        margin-bottom: 1.2rem;
        opacity: 0; transform: translateY(20px);
    }
    .msg-section h4 {
        margin: 0 0 0.3rem 0;
        font-size: 1.1rem;
        background: linear-gradient(90deg, #00ffff, #ff00c8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .diagram-block {
        background: rgba(0,0,0,0.3);
        border: 1px solid #00ffff55;
        border-radius: 12px;
        padding: 0.8rem;
        font-family: 'Courier New', monospace;
        color: #0f0;
        text-shadow: 0 0 8px #0f0;
        white-space: pre-wrap;
        box-shadow: 0 0 15px #0f03;
        margin: 0.5rem 0;
    }
    .fadeInUp {
        animation: fadeInUp 0.6s ease forwards !important;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Top bar */
    .pulse-circle {
        width: 14px; height: 14px;
        background: #0f0;
        border-radius: 50%;
        box-shadow: 0 0 15px #0f0;
        animation: pulse 2s infinite;
        display: inline-block;
        margin-right: 10px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.7; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.7; }
    }
    .progress-bar-container {
        height: 12px;
        background: rgba(255,255,255,0.1);
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 0 15px #00ffff44;
    }
    .progress-bar-fill {
        height: 100%;
        width: 70%;
        background: linear-gradient(90deg, #ff00c8, #00d4ff);
        border-radius: 6px;
        box-shadow: 0 0 25px #ff00c8;
        transition: width 0.5s ease;
    }

    .neon-text {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #00ffff, #ff00c8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px #ff00c8;
    }
    </style>
    """, unsafe_allow_html=True)

def inject_js():
    js = """
    <script>
    function styleCheckedRadio() {
        const radioInputs = document.querySelectorAll('div[data-testid="stRadio"] input[type="radio"]');
        radioInputs.forEach(input => {
            const label = input.closest('label');
            if (label) {
                if (input.checked) {
                    label.style.background = 'linear-gradient(135deg, #ff00c8, #00d4ff)';
                    label.style.borderColor = 'transparent';
                    label.style.color = '#000';
                    label.style.boxShadow = '0 0 30px #ff00c8';
                } else {
                    label.style.background = '';
                    label.style.borderColor = '';
                    label.style.color = '';
                    label.style.boxShadow = '';
                }
            }
        });
    }

    function animateAIBubbles() {
        const bubbles = document.querySelectorAll('.ai-bubble:not([data-typed])');
        bubbles.forEach(bubble => {
            bubble.setAttribute('data-typed', 'true');
            const indicator = bubble.querySelector('.typing-indicator');
            const content = bubble.querySelector('.message-content');
            if (indicator && content) {
                setTimeout(() => {
                    indicator.style.transition = 'opacity 0.4s';
                    indicator.style.opacity = '0';
                    setTimeout(() => {
                        indicator.style.display = 'none';
                        content.style.display = 'block';
                        const sections = content.querySelectorAll('.msg-section');
                        sections.forEach((sec, i) => {
                            sec.style.animationDelay = (i * 0.3) + 's';
                            sec.classList.add('fadeInUp');
                        });
                    }, 400);
                }, 1500);
            }
        });
    }

    window.addEventListener('load', () => {
        styleCheckedRadio();
        animateAIBubbles();
    });
    const observer = new MutationObserver(() => {
        styleCheckedRadio();
        animateAIBubbles();
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)

def inject_particles():
    particles = ""
    for i in range(35):
        left = random.uniform(0, 100)
        top = random.uniform(0, 100)
        size = random.uniform(2, 8)
        dur = random.uniform(15, 35)
        delay = random.uniform(0, 15)
        particles += f'<span class="particle" style="left:{left}%; top:{top}%; width:{size}px; height:{size}px; animation-duration:{dur}s; animation-delay:-{delay}s;"></span>'
    st.markdown(f'<div class="particle-container">{particles}</div>', unsafe_allow_html=True)

def format_ai_response(explanation, example, diagram, question):
    return f"""
    <div class="typing-indicator">
        <span></span><span></span><span></span>
    </div>
    <div class="message-content" style="display:none;">
        <div class="msg-section">
            <h4>🧪 Explanation</h4>
            <p>{explanation}</p>
        </div>
        <div class="msg-section">
            <h4>💡 Example</h4>
            <p>{example}</p>
        </div>
        <div class="msg-section">
            <h4>📊 Diagram</h4>
            <pre class="diagram-block">{diagram}</pre>
        </div>
        <div class="msg-section">
            <h4>❓ Quick Question</h4>
            <p>{question}</p>
        </div>
    </div>
    """

if "messages" not in st.session_state:
    st.session_state.messages = []
if "ai_thinking" not in st.session_state:
    st.session_state.ai_thinking = False
if "last_user_msg" not in st.session_state:
    st.session_state.last_user_msg = ""

@st.cache_resource
def get_engine():
    llm = LLMClient(model_name=settings.LLM_MODEL)
    return TeachingEngine(llm)

engine = get_engine()

def render_top_bar():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("""
        <div style="display:flex; align-items:center;">
            <span class="pulse-circle"></span>
            <span style="color:#0f0; font-weight:bold; text-shadow: 0 0 10px #0f0;">FOCUS MODE ON</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="progress-bar-container" style="margin-top:0.5rem;">
            <div class="progress-bar-fill" style="width:70%;"></div>
        </div>
        <div style="text-align:center; margin-top:0.3rem; font-size:0.8rem; color:#00ffff;">Learning Streak</div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown('<p style="font-style:italic; color:#aaaaff; text-align:right;">"Keep the curiosity alive. You\'re doing great!"</p>', unsafe_allow_html=True)

def main():
    inject_css()
    inject_js()
    st.markdown('<div class="bg-overlay"></div>', unsafe_allow_html=True)
    inject_particles()

    col_h1, col_h2 = st.columns([1, 3])
    with col_h1:
        st.markdown("""
        <lottie-player src="https://assets9.lottiefiles.com/packages/lf20_fcfjwiyb.json" 
            background="transparent" speed="1" style="width: 130px; height: 130px;" loop autoplay>
        </lottie-player>
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        """, unsafe_allow_html=True)
    with col_h2:
        st.markdown('<h1 class="neon-text">AI Master Teacher</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#aa88ff; font-size:1.2rem;">Explain anything · Zero to Pro · 2070</p>', unsafe_allow_html=True)

    mode = st.radio(
        "Select Mode",
        ["🧠 Study Mode", "🎨 Visual Mode", "🏋️ Practice Mode"],
        horizontal=True,
        label_visibility="collapsed",
    )

    render_top_bar()
    st.markdown("---")

    st.markdown('<div class="glass-panel" style="height: 600px; overflow-y: auto; padding: 1rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-row user-row">
                <div class="bubble user-bubble">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row ai-row">
                <div class="bubble ai-bubble">
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Ask anything... (Urdu + English mix)")

    if user_input and not st.session_state.ai_thinking:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({
            "role": "ai",
            "content": '<div class="typing-indicator"><span></span><span></span><span></span></div><p style="color:#00ffff; margin-top:10px;">AI is thinking...</p>'
        })
        st.session_state.last_user_msg = user_input
        st.session_state.ai_thinking = True
        st.rerun()

    if st.session_state.ai_thinking:
        with st.spinner(""):
            time.sleep(settings.AI_THINKING_DELAY)
            response = engine.get_teaching_response(st.session_state.last_user_msg)
            ai_html = format_ai_response(
                explanation=response.explanation,
                example=response.example,
                diagram=response.diagram,
                question=response.question,
            )
        st.session_state.messages[-1] = {"role": "ai", "content": ai_html}
        st.session_state.ai_thinking = False
        st.rerun()

if __name__ == "__main__":
    main()
