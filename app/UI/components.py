import streamlit as st
import re


def render_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

    /* ===== GLOBAL RESET ===== */
    .stApp { background: #030308; overflow-x: hidden; }
    .main .block-container { padding: 1rem 2rem; max-width: 1200px; }
    
    /* ===== ANIMATED BACKGROUND ===== */
    .stApp::before {
        content: '';
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(ellipse at 20% 50%, rgba(120,0,255,0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(0,255,255,0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(255,0,128,0.05) 0%, transparent 50%);
        animation: bgPulse 8s ease-in-out infinite alternate;
        pointer-events: none; z-index: 0;
    }
    @keyframes bgPulse {
        0% { opacity: 0.6; transform: scale(1); }
        100% { opacity: 1; transform: scale(1.05); }
    }

    /* ===== SCANLINE EFFECT ===== */
    .stApp::after {
        content: '';
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg, transparent, transparent 2px,
            rgba(0,255,255,0.01) 2px, rgba(0,255,255,0.01) 4px
        );
        pointer-events: none; z-index: 1;
    }

    /* ===== HEADER ===== */
    .master-header {
        text-align: center;
        padding: 2rem 0 1rem;
        position: relative;
        z-index: 10;
    }
    .header-badge {
        display: inline-block;
        background: rgba(0,255,255,0.1);
        border: 1px solid rgba(0,255,255,0.3);
        color: #00ffff;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        letter-spacing: 4px;
        padding: 4px 16px;
        border-radius: 2px;
        margin-bottom: 12px;
        animation: flicker 3s infinite;
    }
    @keyframes flicker {
        0%, 95%, 100% { opacity: 1; }
        96% { opacity: 0.4; }
        97% { opacity: 1; }
        98% { opacity: 0.2; }
    }
    .header-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(1.8rem, 4vw, 3.2rem);
        font-weight: 900;
        background: linear-gradient(135deg, #00ffff 0%, #bf00ff 50%, #ff0080 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        letter-spacing: 2px;
        line-height: 1.1;
        margin: 0;
        animation: titleGlow 4s ease-in-out infinite alternate;
    }
    @keyframes titleGlow {
        from { filter: drop-shadow(0 0 20px rgba(0,255,255,0.3)); }
        to { filter: drop-shadow(0 0 40px rgba(191,0,255,0.5)); }
    }
    .header-sub {
        font-family: 'Rajdhani', sans-serif;
        color: rgba(0,255,255,0.6);
        font-size: 0.85rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-top: 8px;
    }
    .header-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ffff, #bf00ff, #ff0080, transparent);
        margin: 1.5rem auto;
        max-width: 600px;
        animation: dividerFlow 3s linear infinite;
    }
    @keyframes dividerFlow {
        0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; }
    }

    /* ===== BOOT CARD ===== */
    .boot-card {
        background: rgba(0,255,255,0.03);
        border: 1px solid rgba(0,255,255,0.2);
        border-radius: 12px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        animation: bootPulse 2s ease-in-out infinite;
    }
    @keyframes bootPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0,255,255,0.1); }
        50% { box-shadow: 0 0 40px rgba(0,255,255,0.25), 0 0 80px rgba(191,0,255,0.1); }
    }
    .boot-title {
        font-family: 'Orbitron', sans-serif;
        color: #00ffff;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 3px;
        margin-bottom: 8px;
    }
    .boot-sub {
        font-family: 'Share Tech Mono', monospace;
        color: rgba(0,255,255,0.5);
        font-size: 0.8rem;
        letter-spacing: 2px;
    }

    /* ===== STREAK BAR ===== */
    .streak-bar-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 16px;
        background: rgba(0,0,0,0.3);
        border: 1px solid rgba(0,255,255,0.1);
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    .streak-label {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffff;
        font-size: 0.7rem;
        letter-spacing: 2px;
        white-space: nowrap;
    }
    .streak-track {
        flex: 1;
        height: 4px;
        background: rgba(255,255,255,0.05);
        border-radius: 2px;
        overflow: hidden;
    }
    .streak-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ffff, #bf00ff, #ff0080);
        border-radius: 2px;
        transition: width 0.6s ease;
        box-shadow: 0 0 8px rgba(0,255,255,0.6);
    }
    .streak-count {
        font-family: 'Share Tech Mono', monospace;
        color: rgba(255,255,255,0.4);
        font-size: 0.65rem;
        white-space: nowrap;
    }

    /* ===== CHAT BUBBLES ===== */
    .chat-msg-user {
        display: flex;
        justify-content: flex-end;
        margin: 1rem 0;
        animation: slideInRight 0.3s ease;
    }
    .chat-msg-ai {
        display: flex;
        justify-content: flex-start;
        margin: 1rem 0;
        animation: slideInLeft 0.3s ease;
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .bubble-user {
        background: linear-gradient(135deg, rgba(191,0,255,0.25), rgba(0,128,255,0.2));
        border: 1px solid rgba(191,0,255,0.4);
        border-radius: 16px 4px 16px 16px;
        padding: 14px 18px;
        max-width: 70%;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: rgba(255,255,255,0.9);
        box-shadow: 0 4px 20px rgba(191,0,255,0.15);
        line-height: 1.5;
    }
    .bubble-ai {
        background: rgba(0,8,20,0.8);
        border: 1px solid rgba(0,255,255,0.2);
        border-radius: 4px 16px 16px 16px;
        padding: 0;
        max-width: 90%;
        box-shadow: 0 4px 30px rgba(0,255,255,0.08), inset 0 1px 0 rgba(0,255,255,0.1);
        overflow: hidden;
    }
    .ai-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 16px;
        background: rgba(0,255,255,0.05);
        border-bottom: 1px solid rgba(0,255,255,0.1);
    }
    .ai-avatar {
        width: 28px; height: 28px;
        background: linear-gradient(135deg, #00ffff, #bf00ff);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px;
        animation: avatarPulse 2s ease-in-out infinite;
        flex-shrink: 0;
    }
    @keyframes avatarPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0,255,255,0.4); }
        50% { box-shadow: 0 0 0 6px rgba(0,255,255,0); }
    }
    .ai-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        color: #00ffff;
        letter-spacing: 2px;
    }
    .ai-mode-tag {
        margin-left: auto;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.55rem;
        color: rgba(255,255,255,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2px 8px;
        border-radius: 2px;
    }
    .ai-body { padding: 16px; }

    /* ===== SECTION BLOCKS ===== */
    .section-block {
        margin: 12px 0;
        border-radius: 8px;
        overflow: hidden;
        animation: sectionReveal 0.4s ease;
    }
    @keyframes sectionReveal {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .section-header {
        padding: 8px 14px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 3px;
        font-weight: 700;
    }
    .section-content {
        padding: 12px 16px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        line-height: 1.7;
        color: rgba(255,255,255,0.85);
    }
    /* Explanation */
    .sec-explain .section-header { background: rgba(0,200,255,0.1); color: #00cfff; border-left: 3px solid #00cfff; }
    .sec-explain { border: 1px solid rgba(0,200,255,0.15); }
    /* Example */
    .sec-example .section-header { background: rgba(0,255,128,0.1); color: #00ff80; border-left: 3px solid #00ff80; }
    .sec-example { border: 1px solid rgba(0,255,128,0.15); }
    /* Diagram */
    .sec-diagram .section-header { background: rgba(255,200,0,0.1); color: #ffc800; border-left: 3px solid #ffc800; }
    .sec-diagram { border: 1px solid rgba(255,200,0,0.15); }
    .sec-diagram .section-content {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        background: rgba(0,0,0,0.4);
        white-space: pre-wrap;
        color: #ffc800;
    }
    /* Correction */
    .sec-correction .section-header { background: rgba(255,50,50,0.1); color: #ff4444; border-left: 3px solid #ff4444; }
    .sec-correction { border: 1px solid rgba(255,50,50,0.15); }
    /* Question */
    .sec-question .section-header { background: rgba(191,0,255,0.12); color: #df80ff; border-left: 3px solid #bf00ff; }
    .sec-question { border: 1px solid rgba(191,0,255,0.2); }
    .sec-question .section-content {
        color: #df80ff;
        font-style: italic;
        font-size: 1rem;
    }
    /* Practice */
    .sec-practice .section-header { background: rgba(255,165,0,0.1); color: #ffa500; border-left: 3px solid #ffa500; }
    .sec-practice { border: 1px solid rgba(255,165,0,0.15); }

    /* Raw fallback text */
    .raw-text {
        font-family: 'Rajdhani', sans-serif;
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        line-height: 1.7;
        padding: 4px 0;
    }

    /* ===== INPUT ZONE ===== */
    .input-zone { margin-top: 1.5rem; position: relative; z-index: 10; }
    div[data-testid="stTextInput"] input {
        background: rgba(0,8,20,0.9) !important;
        border: 1px solid rgba(0,255,255,0.25) !important;
        border-radius: 8px !important;
        color: white !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        padding: 14px 18px !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: rgba(0,255,255,0.6) !important;
        box-shadow: 0 0 20px rgba(0,255,255,0.15) !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,0.25) !important; }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0,255,255,0.15), rgba(191,0,255,0.15)) !important;
        border: 1px solid rgba(0,255,255,0.4) !important;
        color: #00ffff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px !important;
        border-radius: 6px !important;
        transition: all 0.3s !important;
        height: 52px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0,255,255,0.3), rgba(191,0,255,0.3)) !important;
        box-shadow: 0 0 20px rgba(0,255,255,0.3) !important;
        transform: translateY(-1px) !important;
    }
    #boot_btn { height: 56px !important; font-size: 0.8rem !important; }

    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: rgba(2,4,12,0.95) !important;
        border-right: 1px solid rgba(0,255,255,0.1) !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stRadio label {
        color: rgba(0,255,255,0.7) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.6rem;
        color: rgba(0,255,255,0.4);
        letter-spacing: 3px;
        border-bottom: 1px solid rgba(0,255,255,0.1);
        margin-bottom: 1rem;
    }
    .focus-indicator {
        display: flex; align-items: center; gap: 8px;
        background: rgba(0,255,0,0.05);
        border: 1px solid rgba(0,255,0,0.2);
        border-radius: 4px;
        padding: 8px 12px;
        margin-top: 1rem;
    }
    .focus-dot {
        width: 8px; height: 8px;
        background: #00ff80;
        border-radius: 50%;
        animation: focusBlink 1.5s ease-in-out infinite;
        flex-shrink: 0;
    }
    @keyframes focusBlink {
        0%, 100% { opacity: 1; box-shadow: 0 0 6px #00ff80; }
        50% { opacity: 0.3; box-shadow: none; }
    }
    .focus-text {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #00ff80;
        letter-spacing: 1px;
    }
    .micro-text {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        color: rgba(255,255,255,0.25);
        text-align: center;
        margin-top: 2rem;
        font-style: italic;
        letter-spacing: 1px;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,255,255,0.2); border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,255,255,0.4); }

    /* ===== HIDE STREAMLIT DEFAULT ===== */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    div[data-testid="stDecoration"] { display: none; }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="master-header">
        <div class="header-badge">◈ NEURAL EDUCATION SYSTEM v4.0 ◈</div>
        <h1 class="header-title">AI MASTER TEACHER 2070</h1>
        <p class="header-sub">Powered by Google Gemma 4 · Zero to Pro</p>
        <div class="header-divider"></div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">⬡ AMT-2070 CONTROL PANEL ⬡</div>', unsafe_allow_html=True)

        mode = st.radio(
            "🎛️ TEACHING MODE",
            ["Study Mode", "Visual Mode", "Practice Mode"],
            index=0
        )

        language = st.selectbox(
            "🌐 LANGUAGE",
            ["English", "Urdu/Hinglish"],
            index=0
        )

        st.markdown("""
        <div class="focus-indicator">
            <div class="focus-dot"></div>
            <span class="focus-text">FOCUS MODE ACTIVE</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p class="micro-text">
            "The mind is not a vessel to be filled,<br>but a fire to be kindled."<br>— Plutarch
        </p>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:rgba(0,255,255,0.25); letter-spacing:1px;">
        MODEL: google/gemma-4-26B-A4B-it<br>
        RUNTIME: Kaggle T4 GPU<br>
        QUANT: 4-bit NF4<br>
        STATUS: <span style="color:#00ff80">ONLINE</span>
        </div>
        """, unsafe_allow_html=True)

    return mode, language


SECTION_MAP = {
    r'\[📖': ('sec-explain', '📖 EXPLANATION'),
    r'\[🌍': ('sec-example', '🌍 REAL-LIFE EXAMPLE'),
    r'\[📊': ('sec-diagram', '📊 DIAGRAM'),
    r'\[⚠️': ('sec-correction', '⚠️ CORRECTION'),
    r'\[🧠': ('sec-question', '🧠 THINKING QUESTION'),
    r'\[🎯': ('sec-practice', '🎯 PRACTICE PROBLEMS'),
    r'\[🌍 REAL LIFE': ('sec-example', '🌍 REAL LIFE EXAMPLE'),
    r'\[📖 WAZAHAT': ('sec-explain', '📖 WAZAHAT'),
    r'\[⚠️ ISLAH': ('sec-correction', '⚠️ ISLAH'),
    r'\[🧠 SOCHNE': ('sec-question', '🧠 SOCHNE WALA SAWAL'),
}


def parse_ai_response(text: str) -> list:
    """Split AI response into labeled sections."""
    # Pattern: lines starting with [emoji WORD]
    pattern = r'(\[(?:📖|🌍|📊|⚠️|🧠|🎯)[^\]]*\])'
    parts = re.split(pattern, text)

    sections = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if not part:
            i += 1
            continue

        # Check if it's a section header
        matched = False
        for key, (css_class, label) in SECTION_MAP.items():
            if re.match(key, part):
                content = parts[i + 1].strip() if i + 1 < len(parts) else ""
                sections.append({"type": css_class, "label": label, "content": content})
                i += 2
                matched = True
                break

        if not matched:
            if part:
                sections.append({"type": "raw", "label": "", "content": part})
            i += 1

    return sections if sections else [{"type": "raw", "label": "", "content": text}]


def render_chat_bubble(role: str, content: str, mode: str = "Study Mode"):
    if role == "user":
        st.markdown(f"""
        <div class="chat-msg-user">
            <div class="bubble-user">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sections = parse_ai_response(content)
        
        section_html = ""
        for sec in sections:
            if sec["type"] == "raw":
                section_html += f'<div class="raw-text">{sec["content"]}</div>'
            else:
                label = sec["label"]
                body = sec["content"].replace("\n", "<br>")
                section_html += f"""
                <div class="section-block {sec['type']}">
                    <div class="section-header">{label}</div>
                    <div class="section-content">{body}</div>
                </div>
                """

        st.markdown(f"""
        <div class="chat-msg-ai">
            <div class="bubble-ai">
                <div class="ai-header">
                    <div class="ai-avatar">🧠</div>
                    <span class="ai-name">GEMMA 4 · MASTER TEACHER</span>
                    <span class="ai-mode-tag">{mode.upper()}</span>
                </div>
                <div class="ai-body">
                    {section_html}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
                
