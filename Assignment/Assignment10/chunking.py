from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
# 1. Basic Fixed-Size Chunking
#text_splitter =CharacterTextSplitter(chunk_size = 300, chunk_overlap = 40)#separator=["", " ", "\n", "\n\n"]

# 2. Recursive Character Chunking
# text_splitter= RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, 
# separators=["\n\n", "\n", " ", ""])

# 3. Token-Based Chunking
# text_splitter= TokenTextSplitter(chunk_size=300, chunk_overlap=50)

# 4. Markdown-Aware Chunking
# headers_to_split_on = [ ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3") ]
# text_splitter= MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 5. Code-Aware Chunking
# code_splitter= RecursiveCharacterTextSplitter.from_language(language="python", 
# chunk_size=500, chunk_overlap=50)

# 6. Sentence-Based Chunking (NLP-Style)
text_splitter= SentenceTransformersTokenTextSplitter(chunk_size=256, chunk_overlap=20)


text = """A computer is a machine that can be programmed to automatically carry out sequences of arithmetic or logical operations (computation). Modern digital electronic computers can perform generic sets of operations known as programs, which enable computers to perform a wide range of tasks. The term computer system may refer to a nominally complete computer that includes the hardware, operating system, software, and peripheral equipment needed and used for full operation; or to a group of computers that are linked and function together, such as a computer network or computer cluster.

A broad range of industrial and consumer products use computers as control systems, including simple special-purpose devices like microwave ovens and remote controls, and factory devices like industrial robots. Computers are at the core of general-purpose devices such as personal computers and mobile devices such as smartphones. Computers power the Internet, which links billions of computers and users.

Early computers were meant to be used only for calculations. Simple manual instruments like the abacus have aided people in doing calculations since ancient times. Early in the Industrial Revolution, some mechanical devices were built to automate long, tedious tasks, such as guiding patterns for looms. More sophisticated electrical machines did specialized analog calculations in the early 20th century. The first digital electronic calculating machines were developed during World War II, both electromechanical and using thermionic valves. The first semiconductor transistors in the late 1940s were followed by the silicon-based MOSFET (MOS transistor) and monolithic integrated circuit chip technologies in the late 1950s, leading to the microprocessor and the microcomputer revolution in the 1970s. The speed, power, and versatility of computers have been increasing dramatically ever since then, with transistor counts increasing at a rapid pace (Moore's law noted that counts doubled every two years), leading to the Digital Revolution during the late 20th and early 21st centuries.

Conventionally, a modern computer consists of at least one processing element, typically a central processing unit (CPU) in the form of a microprocessor, together with some type of computer memory, typically semiconductor memory chips. The processing element carries out arithmetic and logical operations, and a sequencing and control unit can change the order of operations in response to stored information. Peripheral devices include input devices (keyboards, mice, joysticks, etc.), output devices (monitors, printers, etc.), and input/output devices that perform both functions (e.g. touchscreens). Peripheral devices allow information to be retrieved from an external source, and they enable the results of operations to be saved and retrieved. """

code = """import streamlit as st
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
    base_url="http://localhost:1234/v1",
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
"""
# chunks = text_splitter.split_text(text)
chunks = text_splitter.create_documents([text])
# chunks = code_splitter.create_documents([code])

for chunk in chunks:
    print("\nChunk", chunk )
