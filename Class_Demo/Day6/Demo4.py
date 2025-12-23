import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call

# ===================== MIDDLEWARE =====================

@wrap_model_call
def model_logging(request, handler):
    print("Before model call:", "-" * 20)
    response = handler(request)
    print("After model call:", "-" * 20)

    # Modify model output
    response.result[0].content = response.result[0].content.upper()
    return response


@wrap_model_call
def limit_model_context(request, handler):
    print("* Before model call:", "-" * 20)

    # Keep only last 5 messages
    request.messages = request.messages[-5:]

    response = handler(request)
    print("* After model call:", "-" * 20)

    # Modify model output
    response.result[0].content = response.result[0].content.upper()
    return response

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LangChain Middleware Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LangChain Agent with Middleware (Local LLM)", text_alignment="center")

# ===================== INIT MODEL =====================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://192.168.1.115:1234/v1",
    api_key="non-needed"
)

# ===================== CREATE AGENT ====================
agent = create_agent(
    model=llm,
    tools=[],
    middleware=[model_logging, limit_model_context],
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
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Append user message (dict is OK here)
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    # Invoke agent
    result = agent.invoke({
        "messages": st.session_state.conversation
    })

    # Get last AI message
    ai_msg = result["messages"][-1]

    # Show AI response (already uppercased by middleware)
    st.chat_message("assistant").write(ai_msg.content)

    # Update conversation history with LangChain objects
    st.session_state.conversation = result["messages"]
