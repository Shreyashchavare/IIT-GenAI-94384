import streamlit as st
import time

# ==================== Page Config =======================
st.set_page_config(page_title="Chatbot",page_icon="🤖", layout="wide")

# ==================== CSS ===============================

st.markdown("""
<style>
.chat-container{
            max-width: 1700px;
            width: 90%;
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
            font-size: 25px;            
}
            
input{
            font-size: 16px;     
}
</style>
""", unsafe_allow_html= True)

# =================== Session State ==================

if "chat" not in st.session_state:
    st.session_state.chat = []

# ================= Streaming Function ===================

def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

# =========== UI of Bot ============
st.title("💬 Chatbot by Shreyash", text_alignment="center")

with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(
                f"""<div class="chat-msg user-msg">
                        <div class="msg-text">{msg}</div>
                        <div class="user-icon">👱</div>
                    </div>
                """,unsafe_allow_html= True
            )
        else:
            st.markdown(f"""
                <div class="chat-msg bot-msg">
                    <div class="bot-icon">🤖</div>
                    <div class="msg-text">{msg}</div>
                </div>
            """, unsafe_allow_html=True)
    
        st.markdown("</div>", unsafe_allow_html= True)

# ======================== INPUT =========================

user_input = st.chat_input("Type your message...")

if user_input: 
    # save your message 
    st.session_state.chat.append(("user", user_input))

    # Bot reply
    bot_reply = f"You said: {user_input}"

    # Display message 
    st.markdown(f"""
            <div class="chat-msg user-msg">
            <div class="msg-text">{user_input}</div>
            <div class="user-icon">🧑</div>
            </div>
    """,unsafe_allow_html=True)

    # Stream bot reply
    with st.markdown("""<div class='chat-msg bot-msg'>
                     <div class='bot-icon'>🤖</div>
                     <div class='msg-text'>
                     """, unsafe_allow_html=True):
        st.write_stream(stream_reply(bot_reply))

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Save bot reply 
    st.session_state.chat.append(("bot", bot_reply))