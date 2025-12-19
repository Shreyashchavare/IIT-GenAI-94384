import streamlit as st
import time

# ==================== Page Config =======================
st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ==================== CSS ===============================
st.markdown("""
<style>
.chat-container{
    max-width: 1500px;
    width: 80%;
    margin: auto;
}

.chat-msg{
    display: flex;
    gap: 10px;
    margin: 10px 0;
    font-size: 16px;
    line-height: 1.5;
}

.user-msg {
    justify-content: flex-end;
}

.bot-msg {
    justify-content: flex-start;
}

.msg-text{
    max-width: 75%;
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

.user-icon,
.bot-icon{
    font-size: 26px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 32px;
    font-family: "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif;
}

.typing {
    font-style: italic;
    color: #777;
    padding: 6px 10px;
}
</style>
""", unsafe_allow_html=True)

# =================== Session State ==================
if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= Unified Bot UI ==================
def bot_response_ui(placeholder, text):
    # ---- Typing indicator ----
    dots = ["", ".", "..", "..."]
    for i in range(6):
        placeholder.markdown(f"""
        <div class="chat-msg bot-msg">
            <div class="bot-icon">🤖</div>
            <div class="typing">typing{dots[i % 4]}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.25)

    # ---- Streaming reply ----
    words = text.split()
    reply = ""
    for w in words:
        reply += w + " "
        placeholder.markdown(f"""
        <div class="chat-msg bot-msg">
            <div class="bot-icon">🤖</div>
            <div class="msg-text">{reply}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.05)

# =================== UI ===================
st.title("💬 Chatbot by Shreyash", text_alignment="center")

with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    # Display chat history
    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"""
            <div class="chat-msg user-msg">
                <div class="msg-text">{msg}</div>
                <div class="user-icon">🧑</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-msg bot-msg">
                <div class="bot-icon">🤖</div>
                <div class="msg-text">{msg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================== INPUT =========================
user_input = st.chat_input("Type your message...")

if user_input:
    # Save user message
    st.session_state.chat.append(("user", user_input))

    # Show user message immediately
    st.markdown(f"""
    <div class="chat-msg user-msg">
        <div class="msg-text">{user_input}</div>
        <div class="user-icon">🧑</div>
    </div>
    """, unsafe_allow_html=True)

    # Bot reply
    bot_reply = f"You said: {user_input}"

    # Single placeholder for bot
    bot_placeholder = st.empty()

    # Typing + streaming (no UI glitch)
    bot_response_ui(bot_placeholder, bot_reply)

    # Save bot reply
    st.session_state.chat.append(("bot", bot_reply))
