"""
RAG Pipeline for PE Intelligence AI
Handles document processing, embedding generation, and retrieval
"""
from typing import List, Dict, Any, Optional
import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings

class RAGPipeline:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Initialize ChromaDB
        chroma_host = os.getenv("CHROMA_HOST", "localhost")
        chroma_port = int(os.getenv("CHROMA_PORT", "8001"))
        
        self.chroma_client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port
        )
        
    def create_collection(self, collection_name: str):
        """Create or get a ChromaDB collection"""
        try:
            return self.chroma_client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error creating collection: {e}")
            return None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI's text-embedding-3-large"""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model="text-embedding-3-large"
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ):
        """Add documents to vector database"""
        collection = self.create_collection(collection_name)
        if not collection:
            return False
        
        try:
            embeddings = self.generate_embeddings(documents)
            collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
    
    def retrieve(
        self,
        collection_name: str,
        query: str,
        top_k: int = 5
    ) -> Dict[str, Any]:
        """Retrieve relevant documents from vector database"""
        collection = self.create_collection(collection_name)
        if not collection:
            return {"documents": [], "metadatas": [], "distances": []}
        
        try:
            query_embedding = self.generate_embeddings([query])[0]
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return {"documents": [], "metadatas": [], "distances": []}
    
    def generate_response(
        self,
        query: str,
        context: List[str],
        system_prompt: str,
        model: str = "gpt-4"
    ) -> str:
        """Generate response using GPT-4 with retrieved context"""
        try:
            # Prepare context string
            context_str = "\n\n".join([f"[Source {i+1}]: {doc}" for i, doc in enumerate(context)])
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context_str}\n\nQuery: {query}"}
            ]
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""
    
    def rag_query(
        self,
        collection_name: str,
        query: str,
        system_prompt: str,
        top_k: int = 5,
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve + generate"""
        # Retrieve relevant documents
        results = self.retrieve(collection_name, query, top_k)
        
        if not results.get("documents") or not results["documents"][0]:
            return {
                "response": "No relevant information found.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Generate response
        context = results["documents"][0]
        response = self.generate_response(query, context, system_prompt, model)
        
        # Prepare sources with metadata
        sources = []
        if results.get("metadatas") and results["metadatas"][0]:
            for i, metadata in enumerate(results["metadatas"][0]):
                sources.append({
                    "source": metadata.get("source", f"Document {i+1}"),
                    "url": metadata.get("url"),
                    "page": metadata.get("page"),
                    "confidence": 1.0 - results["distances"][0][i] if results.get("distances") else 0.5
                })
        
        return {
            "response": response,
            "sources": sources,
            "confidence": 0.8  # Default confidence score
        }
