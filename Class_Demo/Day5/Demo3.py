from langchain.chat_models import init_chat_model
import os
import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(page_title="LangChain Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 LangChain Chatbot by Shreyash")

# ================= LLM INIT ====================
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ================= SESSION STATE ===============
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ================= USER INPUT ==================
user_input = st.chat_input("You:")

if user_input:
    if user_input.lower() == "exit":
        st.success("Thank you for visiting. You have exited the chat 👋")
        st.stop()

    # ---- Add user message
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    # ---- LLM response
    llm_output = llm.invoke(st.session_state.conversation)

    st.session_state.conversation.append(
        {"role": "assistant", "content": llm_output.content}
    )

# ================= DISPLAY CHAT ================
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
