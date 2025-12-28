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
st.subheader("Upload CSV File (Required only for CSV questions)")

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
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

# ===================== CREATE AGENT ====================
agent = create_agent(
    model=llm,
    tools=[csv_qa_tool, sunbeam_scrapper_tool],
    system_prompt=(f"""
        You are a helpful, reliable assistant.

        PRIMARY RULES:
        1. Always explain answers in simple, clear English. Avoid jargon unless necessary.
        2. Decide tool usage strictly based on the user question and available context.

        TOOL USAGE RULES:
        - If the question is about Sunbeam Institute, Sunbeam internships, or Sunbeam batches:
        → Use the Sunbeam Web Tool to fetch accurate information.

        - If a CSV file is uploaded AND the question is about the CSV data (columns, rows, statistics, filtering, aggregation, trends, etc.):
        → Use the CSV Tool to answer.

        ERROR & WARNING HANDLING:
        - If the user asks a question related to CSV data BUT no CSV file is uploaded:
        → Respond with exactly:
            "CSV is not uploaded."

        - If a CSV file IS uploaded BUT the user asks a question about Sunbeam internships or batches:
        → First show this warning:
            "You have uploaded a CSV file, but it is not used for this question. Answering based on general knowledge."
        → Then answer the question using the Sunbeam Web Tool or your general knowledge.

        GENERAL BEHAVIOR:
        - Do NOT use tools unnecessarily.
        - Use only one tool per question unless explicitly required.
        - If the question does not match any tool category, answer using your own knowledge.
        - Keep responses concise, structured, and easy to understand.
        """
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
