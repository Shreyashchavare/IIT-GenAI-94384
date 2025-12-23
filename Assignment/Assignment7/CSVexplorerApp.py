from langchain.chat_models import init_chat_model
import os
import pandas as pd
from pandasql import sqldf
import streamlit as st

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="CSV Explorer Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 CSV Explorer Agent", text_alignment="center")

# ====================== LLM CONFIG ======================
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ====================== SESSION STATE ======================
if "chat" not in st.session_state:
    st.session_state.chat = []

if "df" not in st.session_state:
    st.session_state.df = None

# ====================== FILE UPLOAD ======================
csv_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if csv_file:
    # Read CSV
    df = pd.read_csv(csv_file)

    
    df = df.reset_index(drop=True)

    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].astype("int64")
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype("float64")
        else:
            df[col] = df[col].astype(str)

    st.session_state.df = df

    st.subheader("📊 CSV Preview")
    st.dataframe(df.head())

    st.subheader("🧬 CSV Schema")
    st.write(df.dtypes.astype(str))  # Arrow-safe

# ====================== CHAT INPUT ======================
user_input = st.chat_input("Ask anything about this CSV...")

if user_input and st.session_state.df is not None:
    df = st.session_state.df

    # Store user message
    st.session_state.chat.append({
        "role": "user",
        "content": user_input
    })

    # ====================== LLM PROMPT ======================
    llm_prompt = f"""
You are a SQLite developer with 10 years of experience.

Table name: data
Table schema:
{df.dtypes.astype(str)}

Question:
{user_input}

Instructions:
- Generate ONLY a valid SQLite SQL query
- Do NOT add explanation
- Do NOT use markdown
- If query cannot be generated, output exactly: Error
"""

    # Invoke LLM
    result = llm.invoke(llm_prompt)
    sql_query = result.content.strip()

    # Store assistant message
    st.session_state.chat.append({
        "role": "assistant",
        "content": sql_query
    })

    # ====================== EXECUTE SQL ======================
    if sql_query.lower() != "error":
        try:
            query_result = sqldf(sql_query, {"data": df})

            query_result = query_result.reset_index(drop=True)
            query_result = query_result.astype(str)

            st.subheader("✅ Query Result")
            st.dataframe(query_result)

        except Exception as e:
            st.error(f"❌ SQL Execution Error: {e}")

    # ====================== EXPLAIN RESULT ======================
    explain_prompt = f"""
    You are a data analyst.

    User question:
    {user_input}

    SQL query used:
    {sql_query}

    Result:
    {query_result.to_string(index=False)}

    Explain the result in very simple English.
    Avoid technical terms.
    Do not mention SQL or databases.
    """

    explanation = llm.invoke(explain_prompt).content.strip()
    st.subheader("🧠 Explanation (Simple English)")
    st.write(explanation)
# ====================== DISPLAY CHAT ======================
st.divider()
st.subheader("💬 Conversation")

for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


