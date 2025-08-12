###########################################
# Utility for setting up the vector store #
###########################################
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#############################
# 1. Load a couple of docs  #
#############################
# Sample blogs on RAG that we can add to vector database
def create_loader():
    loader = DirectoryLoader('./', glob="**/*.txt")
    docs = loader.load()
    return loader

######################
# 2. Chunk the blogs #
######################
def create_chunks(chunk_size=300, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size, chunk_overlap)
    chunked_documents = text_splitter.split_documents(docs)
    return chunked_documents

#################################
# 3. Add chunks to the ChromaDB #
#################################
from langchain_community.vectorstores import Chroma
# from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def create_chroma(collection_name = 'sample-blog'):
    # load it into Chroma using default embedding all-MiniLM-L6-v2
    collection_metadata = {'embedding': 'all-MiniLM-L6-v2'}
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = Chroma(collection_name=collection_name, collection_metadata=collection_metadata, embedding_function=embedding_function)

    return vector_store
    # vector_store.add_documents(chunked_documents)

    # Used in the notebook
    #retriever = vector_store.as_retriever()