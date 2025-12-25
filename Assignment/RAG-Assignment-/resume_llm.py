# import all neccessary modules
from langchain.chat_models import init_chat_model

# Import devloper defined modules
from resume_embed import embedding_of_resume
from resume_vector import add_all_folders_of_dir
# ===================== LLM CONFIG ======================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://localhost:1234/v1",
    api_key="non-needed"
)
# =============================History of Chat===================
conversations = []

# ==================== input for a LLM =========================
while True:
    user_prompt = input("Ask your queries for resume RAG: ")

    conversations.append({"role" :"user", "content": user_prompt})






