from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os 
from dotenv import load_dotenv
load_dotenv()
# api_key = os.getenv("GROQ_API_KEY")
# llm = ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)

# api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key, content = "")
llm_url = "http://192.168.1.115:1234/v1"

llm = ChatOpenAI(
    base_url = llm_url,
    model="google/gemma-3-4b",
    api_key="dummy-key"
)

user_input = input("You: ")
# result = llm.stream(user_input)
# for chunk in result:
#     print(chunk.content, end="")


result = llm.invoke(user_input)
print("AI: ", result.content)

