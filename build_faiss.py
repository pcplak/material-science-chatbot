from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings  # Import LangChain's Embeddings wrapper
from sentence_transformers import SentenceTransformer
from langchain.docstore import InMemoryDocstore  # Import this for the docstore
import faiss
import numpy as np

# Load the text chunks from the file
with open('text_chunks_by_sentence.txt', 'r') as f:
    chunks = f.read().split('\n\n')
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

# Convert the chunks to Document objects
documents = [Document(page_content=chunk) for chunk in chunks]

# Load a pre-trained embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Wrap the SentenceTransformer model using LangChain's HuggingFaceEmbeddings class
embeddings_wrapper = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Create embeddings for your documents using the embeddings_wrapper
embeddings = np.array(embeddings_wrapper.embed_documents([d.page_content for d in documents]))

# Create FAISS index and add embeddings
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings.astype('float32'))

# Create an InMemoryDocstore from the documents
docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(documents)})

# Create a new index_to_docstore_id that matches the string keys used in docstore
index_to_docstore_id = [str(i) for i in range(len(documents))]  # Create string-based IDs

# Create the vector store using the wrapped embeddings and InMemoryDocstore
vector_store = FAISS(
    embedding_function=embeddings_wrapper,
    index=index,
    docstore=docstore,  # Pass the InMemoryDocstore here
    index_to_docstore_id=index_to_docstore_id  # Pass the mapping
)

# Save the vector store to the current directory, specifying index_name here
vector_store.save_local(".", index_name='vector_index')

print("FAISS vector database has been created and saved!")
