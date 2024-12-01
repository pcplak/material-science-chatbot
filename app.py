from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from langchain.embeddings import HuggingFaceEmbeddings  # Import LangChain's Embeddings wrapper
from sentence_transformers import SentenceTransformer

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Wrap the SentenceTransformer model using LangChain's HuggingFaceEmbeddings class
embeddings_wrapper = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# Load the vector store using the embeddings wrapper
loaded_vector_store = FAISS.load_local(
    '.', embeddings_wrapper, index_name='vector_index', allow_dangerous_deserialization=True
)

retriever = loaded_vector_store.as_retriever()

# Load Hugging Face model
HUGGINGFACEHUB_API_TOKEN = "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"
llm = HuggingFaceEndpoint(
    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_length=512,
    temperature=0.5,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

# Initialize RetrievalQA
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    try:
        response = rag_chain.run(question)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
