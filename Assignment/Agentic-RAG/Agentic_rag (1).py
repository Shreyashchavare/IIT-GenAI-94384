import chromadb
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

# =====================================================
# Streamlit UI
# =====================================================
st.title("🤖 AI Resume Handler (Agentic RAG)")

# =====================================================
# Embedding Model
# =====================================================
embed_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# ChromaDB
# =====================================================
client = chromadb.Client(
    settings=chromadb.Settings(persist_directory="./chroma_db")
)
collection = client.get_or_create_collection(name="demo")

# =====================================================
# Load Resumes (Only Once)
# =====================================================
if collection.count() == 0:
    loader = DirectoryLoader(
        path="D:/sunbeam_AI_notes/resume",
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    # Add metadata
    for doc in documents:
        doc.metadata["pdf_name"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["page_number"] = doc.metadata["page"] + 1

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=50,
        separators=["\n\n", "\n", " "]
    )
    chunks = splitter.split_documents(documents)

    texts, metadatas, ids = [], [], []

    for idx, chunk in enumerate(chunks):
        texts.append(chunk.page_content)
        chunk.metadata["chunk_id"] = str(idx)
        chunk.metadata["chunk_size"] = len(chunk.page_content)
        metadatas.append(chunk.metadata)
        ids.append(str(idx))

    embeddings = embed_model.embed_documents(texts)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    st.success("✅ Resumes indexed successfully")

# =====================================================
# Tool: Resume Retriever
# =====================================================
@tool
def resume_retrieval_tool(query: str) -> str:
    """
    Retrieve relevant resume information from ChromaDB.

    This tool performs semantic search over stored resume embeddings
    and returns the most relevant resume chunks as plain text.

    Args:
        query (str): User query related to resumes.

    Returns:
        str: Relevant resume content for grounding answers.
    """

    query_embedding = embed_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    formatted_chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted_chunks.append(
            f"""
            📄 Resume: {meta.get("pdf_name")}
            📑 Page: {meta.get("page_number")}
            🔹 Chunk ID: {meta.get("chunk_id")}

            {doc}
            """
        )

    return "\n\n".join(formatted_chunks)

# =====================================================
# LLM
# =====================================================
llm = init_chat_model(
    model="phi-3-mini-4k-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

# =====================================================
# Agent
# =====================================================
agent = create_agent(
    model=llm,
    tools=[resume_retrieval_tool],
    system_prompt="""
You are an experienced HR analyst.

Rules:
- ALWAYS use resume_retrieval_tool before answering.
- Answer strictly using resume content.
- Do not hallucinate.
- If information is missing, say: "Information not found in resumes."

Output format:
- Relevant candidates
- Matching skills
- Clear explanation
"""
)

# =====================================================
# User Query
# =====================================================
user_query = st.chat_input("Ask something about resumes...")

if user_query:
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]}
    )

    final_answer = response["messages"][-1].content
    st.markdown("### 🧠 Answer")
    st.write(final_answer)
