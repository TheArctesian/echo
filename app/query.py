import os
from typing import List, Dict, Any
from langchain_ollama import OllamaEmbeddings, Ollama
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

# Configuration
VECTOR_DB_PATH = "/storage/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "deepseek-r1:14b"  # or any other model you have in Ollama

class ObsidianRAG:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
        self.vectordb = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=self.embeddings
        )
        
        self.retriever = self.vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        self.llm = Ollama(
            model=LLM_MODEL,
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        )
        
        # Create the RAG prompt
        self.prompt = ChatPromptTemplate.from_template("""
        Answer the question based on the following context from your personal notes:
        
        {context}
        
        Question: {question}
        
        Answer:
        """)
        
        # Create the RAG chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the RAG system with a question"""
        result = self.chain.invoke(question)
        
        # Get the retrieved documents for reference
        docs = self.retriever.get_relevant_documents(question)
        sources = [doc.metadata.get('source', 'Unknown') for doc in docs]
        
        return {
            "answer": result.content,
            "sources": sources
        }
    
    def similarity_search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Perform a similarity search without using the LLM"""
        docs = self.vectordb.similarity_search(query, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]