import streamlit as st
from ollama import chat, ChatResponse

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ollama Chat",
    page_icon="🤖",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ---------- global ---------- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0f;
    color: #e8e6e0;
}

/* ---------- hide default streamlit chrome ---------- */
#MainMenu, footer, header { visibility: hidden; }

/* ---------- app container ---------- */
.block-container {
    max-width: 780px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

/* ---------- title ---------- */
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #f0ede6;
    margin-bottom: 0.15rem;
}
.hero-sub {
    font-size: 0.85rem;
    color: #6b6760;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: #111114;
    border-right: 1px solid #1e1e22;
}
[data-testid="stSidebar"] h2 {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #a0a09e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ---------- chat messages ---------- */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 0.4rem 0;
    margin-bottom: 0.25rem;
}

/* user bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: #1a1a1f;
    border: 1px solid #252528;
}

/* assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: #13131a;
    border: 1px solid #1e1e2a;
}

/* ---------- chat input ---------- */
[data-testid="stChatInput"] textarea {
    background: #16161a !important;
    border: 1px solid #2a2a30 !important;
    border-radius: 10px !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    caret-color: #c8ff57;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: #c8ff57 !important;
    box-shadow: 0 0 0 2px rgba(200,255,87,0.12) !important;
}

/* ---------- model badge ---------- */
.model-badge {
    display: inline-block;
    background: #1c1c22;
    border: 1px solid #2e2e36;
    border-radius: 6px;
    padding: 2px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #c8ff57;
    margin-bottom: 1.4rem;
    letter-spacing: 0.04em;
}

/* ---------- clear button ---------- */
.stButton > button {
    background: transparent;
    border: 1px solid #2a2a30;
    color: #7a7a7e;
    border-radius: 8px;
    font-size: 0.8rem;
    padding: 0.35rem 1rem;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    border-color: #c8ff57;
    color: #c8ff57;
    background: rgba(200,255,87,0.06);
}

/* ---------- spinner ---------- */
.stSpinner > div { border-top-color: #c8ff57 !important; }

/* ---------- select box ---------- */
[data-testid="stSelectbox"] div {
    background: #16161a;
    border: 1px solid #2a2a30;
    color: #e8e6e0;
    border-radius: 8px;
}

/* ---------- scrollbar ---------- */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d0d0f; }
::-webkit-scrollbar-thumb { background: #2a2a30; border-radius: 4px; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Settings")

    model = st.selectbox(
        "Model",
        options=[
            "minimax-m2.7:cloud",
            "llama3.2",
            "llama3.1",
            "mistral",
            "gemma3",
            "phi4",
            "deepseek-r1",
            "qwen2.5",
        ],
        index=0,
    )

    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.05
    )
    max_tokens = st.slider(
        "Max tokens", min_value=128, max_value=4096, value=1024, step=128
    )

    st.markdown("---")

    system_prompt = st.text_area(
        "System prompt",
        value="You are a helpful, concise assistant.",
        height=100,
    )

    st.markdown("---")

    if st.button("🗑 Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<span style='font-size:0.72rem;color:#3a3a40;'>Powered by Ollama + Streamlit</span>",
        unsafe_allow_html=True,
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Ollama Chat</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Local AI · No cloud required</div>', unsafe_allow_html=True
)
st.markdown(f'<div class="model-badge">▸ {model}</div>', unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Render history ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask anything…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build message list for Ollama (include system prompt)
    ollama_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
    ]

    # Call Ollama
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                response: ChatResponse = chat(
                    model=model,
                    messages=ollama_messages,
                    options={
                        "temperature": temperature,
                        "num_predict": max_tokens,
                    },
                )
                reply = response.message.content
            except Exception as e:
                reply = f"⚠️ **Error:** {e}\n\nMake sure Ollama is running (`ollama serve`) and the model is pulled."

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
