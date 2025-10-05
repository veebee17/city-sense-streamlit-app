import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from pinecone import Pinecone, ServerlessSpec
import openai
import google.generativeai as genai
from config import Config

class VectorService:
    def __init__(self):
        self.pc = None
        self.index = None
        self.embedding_service = None
        self.embedding_model = None
    
    def is_available(self) -> bool:
        """Check if vector service is available and properly configured"""
        return self.pc is not None and self.index is not None and self.embedding_service is not None
    
    def setup_pinecone(self) -> bool:
        """Setup Pinecone connection"""
        try:
            api_key = os.getenv('PINECONE_API_KEY')
            if not api_key:
                return False
                
            self.pc = Pinecone(api_key=api_key)
            
            # Create index if it doesn't exist
            index_name = Config.PINECONE_INDEX_NAME
            if index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=index_name,
                    dimension=Config.EMBEDDING_DIMENSION,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            
            self.index = self.pc.Index(index_name)
            return True
            
        except Exception as e:
            print(f"Error setting up Pinecone: {e}")
            return False
    
    def setup_embedding_service(self, provider: str = "openai") -> bool:
        """Setup embedding service (OpenAI or Gemini)"""
        try:
            if provider == "openai":
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    return False
                openai.api_key = api_key
                self.embedding_service = "openai"
                self.embedding_model = "text-embedding-ada-002"
                
            elif provider == "gemini":
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    return False
                genai.configure(api_key=api_key)
                self.embedding_service = "gemini"
                self.embedding_model = "models/embedding-001"
                
            return True
            
        except Exception as e:
            print(f"Error setting up embedding service: {e}")
            return False
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for text"""
        try:
            if self.embedding_service == "openai":
                response = openai.embeddings.create(
                    model=self.embedding_model,
                    input=text
                )
                return response.data[0].embedding
                
            elif self.embedding_service == "gemini":
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document"
                )
                return result['embedding']
                
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def store_conversation_chunk(self, conversation_id: str, chunk_text: str, 
                               metadata: Dict[str, Any]) -> bool:
        """Store conversation chunk in vector database"""
        try:
            if not self.index:
                return False
                
            embedding = self.get_embedding(chunk_text)
            if not embedding:
                return False
            
            # Create unique ID for this chunk
            chunk_id = f"{conversation_id}_{metadata.get('chunk_index', 0)}"
            
            # Prepare metadata
            vector_metadata = {
                "conversation_id": conversation_id,
                "text": chunk_text,
                "timestamp": datetime.now().isoformat(),
                **metadata
            }
            
            # Store in Pinecone
            self.index.upsert([(chunk_id, embedding, vector_metadata)])
            return True
            
        except Exception as e:
            print(f"Error storing conversation chunk: {e}")
            return False
    
    def search_conversations(self, query: str, top_k: int = 5, 
                           conversation_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for relevant conversation chunks"""
        try:
            if not self.index:
                return []
                
            query_embedding = self.get_embedding(query)
            if not query_embedding:
                return []
            
            # Prepare filter
            filter_dict = {}
            if conversation_id:
                filter_dict["conversation_id"] = conversation_id
            
            # Search
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "id": match.id,
                    "score": match.score,
                    "text": match.metadata.get("text", ""),
                    "conversation_id": match.metadata.get("conversation_id", ""),
                    "timestamp": match.metadata.get("timestamp", ""),
                    "metadata": match.metadata
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about stored conversations"""
        try:
            if not self.index:
                return {"error": "Index not initialized"}
                
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
            
        except Exception as e:
            return {"error": f"Error getting stats: {e}"}
    
    def clear_conversation_history(self, conversation_id: Optional[str] = None) -> bool:
        """Clear conversation history from vector database"""
        try:
            if not self.index:
                return False
            
            if conversation_id:
                # Delete specific conversation
                # Note: Pinecone doesn't support delete by metadata filter directly
                # We need to query first, then delete by IDs
                results = self.search_conversations("", top_k=10000, conversation_id=conversation_id)
                if results:
                    ids_to_delete = [result["id"] for result in results]
                    self.index.delete(ids=ids_to_delete)
            else:
                # Clear all vectors
                self.index.delete(delete_all=True)
            
            return True
            
        except Exception as e:
            print(f"Error clearing conversation history: {e}")
            return False