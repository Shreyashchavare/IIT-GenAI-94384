import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LangChain Tool Agent",
    layout="wide"
)

st.title("LangChain Calculator Agent (Local LLM)", text_alignment="center")

# ===================== TOOL ============================
@tool
def calculator(expression: str):
    """
    Solves arithmetic expressions using +, -, *, / and parentheses.
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"

# ===================== INIT MODEL ======================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://192.168.1.115:1234/v1",
    api_key="non-needed"
)

# ===================== CREATE AGENT ====================
agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="You are a helpful assistant. Answer in short."
)

# ===================== SESSION STATE ===================
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ===================== DISPLAY CHAT ====================
for msg in st.session_state.conversation:
    if msg.type == "human":
        st.chat_message("user").write(msg.content)
    elif msg.type == "ai":
        st.chat_message("assistant").write(msg.content)

# ===================== USER INPUT ======================
user_input = st.chat_input("Ask something (e.g. 12 * (5 + 3))")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Append user message
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    # Invoke agent
    result = agent.invoke({
        "messages": st.session_state.conversation
    })

    # Get last AI message
    ai_msg = result["messages"][-1]

    # Show AI response
    st.chat_message("assistant").write(ai_msg.content)

    # Update conversation history with LangChain objects
    st.session_state.conversation = result["messages"]

