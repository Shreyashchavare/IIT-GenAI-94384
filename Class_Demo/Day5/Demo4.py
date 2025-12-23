import streamlit as st
from langchain.chat_models import init_chat_model
import os

# =================== PAGE CONFIG ===================
st.set_page_config(page_title="LangChain Chatbot",page_icon="🤖",layout="wide")

st.title("🤖 LangChain Chatbot with GROQ", text_alignment="center")

# =================== LLM INIT ===================
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# =================== SESSION STATE ===================
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

# =================== SIDEBAR ===================
with st.sidebar:
    st.header("⚙️ Settings")
    context_limit = st.slider(
        "Context window (last N messages)",
        min_value=2,
        max_value=20,
        value=10,
        step=2
    )

# =================== DISPLAY CHAT ===================
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# =================== USER INPUT ===================
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message
    user_msg = {"role": "user", "content": user_input}
    st.session_state.conversation.append(user_msg)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare limited context
    system_msg = st.session_state.conversation[0]
    recent_msgs = st.session_state.conversation[-context_limit:]
    llm_messages = [system_msg] + recent_msgs

    # Invoke LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            llm_output = llm.invoke(llm_messages)
            st.markdown(llm_output.content)

    # Save assistant reply
    assistant_msg = {
        "role": "assistant",
        "content": llm_output.content
    }
    st.session_state.conversation.append(assistant_msg)
