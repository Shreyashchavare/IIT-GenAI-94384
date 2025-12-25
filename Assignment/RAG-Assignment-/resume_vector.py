# Import all neccessary modules
import chromadb

# Import devloper defined modules
from resume_embed import embedding_of_resume, query_embedding

# Create client 
db = chromadb.PersistentClient("./resume_rag")

#Create collection
collection = db.get_or_create_collection("resumes")

# ====================================== add_all_folders_of_dir ==============================
def add_all_folders_of_dir(dir_path):
    """
    Docstring for add_all_folders_of_dir
    This function add all pdf datas vectors to the Chroma DB ,
    but if update is neccessary then this is not ideal function.
    
    :param dir_path: path of directory where all pdf are present.
    :return True/False: return true if data added.
    """
    # Get embedding vector and information of pdfs 
    texts, embeddings, metadatas, ids = embedding_of_resume(dir_path=dir_path)

    try:
        # adding vectors in DB
        collection.add(ids=ids, metadatas=metadatas, embeddings=embeddings,documents=texts)
        return True
    except Exception as e:
        print(e)
        return False


# ====================================== query_processing ==============================

def query_processing(query):
    """
    Docstring for query_processing
    This function process the text query and returns result
    :param query: text query
    :return: result of query
    """

    query_embed = query_embedding(query=query)
    try:
        results = collection.query(query_embeddings=[query_embed], n_results= 3)
        return results
    except Exception as e:
        print(e)
        return None
