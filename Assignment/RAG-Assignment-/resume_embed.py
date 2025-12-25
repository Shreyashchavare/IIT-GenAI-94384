
# Import neccessary modules
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# embedding model 
EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
# ============================= embedding_of_resume ==================================
def embedding_of_resume(dir_path):
    """
    Docstring for embedding_of_resume
    This function is used create vector embedding for give directory path of pdfs
    :param dir_path: directory path of pdfs where all pdf are present 
    :return texts: content of pdf chunk 
            embeddings: vector of pdf chunk
            metadatas: metadata of chunk
            ids: ids for vectors of chunks
    """

    # load all pdf 
    loader = DirectoryLoader(
        path=dir_path,
        glob= "**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents = loader.load()

    # creating metadata for each pdf at document level
    for doc in documents:
        doc.metadata["pdf_name"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["page_number"] = doc.metadata["page"] + 1

    # chunking of data
    splitter = RecursiveCharacterTextSplitter(
        chunk_overlap = 50,
        chunk_size = 800,
        separators=[" ", "\n", "\n\n"]
    )

    chunks = splitter.split_documents(documents=documents)

    # metadata for chunking level
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx
        chunk.metadata["chunk_size"] = len(chunk.page_content)


    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    embeddings = EMBED_MODEL.encode(texts)
    # ID for adding vector in DB
    ids = [
        f"{m['pdf_name']}_p{m['page_number']}_c{m['chunk_id']}"
        for m in metadatas
    ]

    return texts, embeddings, metadatas, ids

# ============================= query_embedding ==================================
def query_embedding(query):
    """
    Docstring for query_embedding
    This function used only for creating vector embedding of query
    :param query: Text query
    :return: Embedded vector
    """
    return EMBED_MODEL.encode(query)