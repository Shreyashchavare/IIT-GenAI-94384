import streamlit as st
import pandas as pd
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

# ===================== IMPORT TOOLS =====================
from csv_qa_tool import csv_qa_tool
from sunbeam_webscrapper_tool import sunbeam_scrapper_tool

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LangChain Tool Agent",
    page_icon="🧮",
    layout="wide"
)

st.title(
    "🧮 LangChain Multitool Agent (CSV Explorer + Web Scraper)",
    text_alignment="center"
)

# ===================== CSV UPLOAD (OPTIONAL) =====================
st.subheader("📂 Upload CSV File (Required only for CSV questions)")

csv_file = st.file_uploader(
    "Upload a CSV file if you want to ask CSV-related questions",
    type=["csv"]
)

df = None
if csv_file:
    df = pd.read_csv(csv_file)
    st.session_state.df = df

    st.success("CSV uploaded successfully!")

    st.write("### 📊 CSV Schema")
    st.write(df.dtypes)

    st.write("### 👀 Data Preview")
    st.dataframe(df.head())

# ===================== INIT MODEL ======================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://10.230.255.200:1234/v1",
    api_key="not-needed"
)

# ===================== CREATE AGENT ====================
agent = create_agent(
    model=llm,
    tools=[csv_qa_tool, sunbeam_scrapper_tool],
    system_prompt=(
        "You are a helpful assistant. "
        "If the question is about CSV data, use the CSV tool. "
        "If the question is about Sunbeam internships or batches, "
        "use the Sunbeam web tool. "
        "If CSV is not uploaded and a CSV question is asked, "
        "politely ask the user to upload a CSV file. "
        "Always explain answers in simple English."
    )
)

# ===================== SESSION STATE ===================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ===================== DISPLAY CHAT ====================
st.divider()
st.subheader("💬 Chat")

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# ===================== USER INPUT ======================
user_input = st.chat_input(
    "Ask about Sunbeam internships/batches or the uploaded CSV"
)

if user_input:
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    response = agent.invoke({
        "messages": st.session_state.messages,
        "df": df
    })

    ai_message = response["messages"][-1].content

    st.chat_message("assistant").write(ai_message)

    st.session_state.messages = response["messages"]
