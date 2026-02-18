"""
RAG Module
Implements Retrieval-Augmented Generation using Chroma vector database.
Helps convert natural language queries to SQL by retrieving relevant schema information.
"""

import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings


class SchemaRAG:
    """
    Retrieval-Augmented Generation for SQL schema.
    Uses Chroma vector database to store and retrieve schema information.
    """
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize the RAG system with Chroma vector database.
        
        Args:
            persist_dir: Directory for persisting Chroma database
        """
        self.persist_dir = persist_dir
        
        # Create persistent Chroma client
        settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
        
        import chromadb

class SchemaRAG:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="schema_collection"
        )

        
        # Get or create collection for schema information
        self.collection = self.client.get_or_create_collection(
            name="database_schema",
            metadata={"hnsw:space": "cosine"}
        )
    
    def load_schema_from_file(self, schema_file: str) -> None:
        """
        Load database schema from a file and add to vector database.
        
        Args:
            schema_file: Path to the schema file
        """
        if not os.path.exists(schema_file):
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
        
        with open(schema_file, 'r') as f:
            schema_content = f.read()
        
        # Parse schema into individual table definitions
        table_blocks = schema_content.split("CREATE TABLE")
        
        documents = []
        ids = []
        metadatas = []
        
        for i, block in enumerate(table_blocks[1:]):  # Skip first empty split
            block = "CREATE TABLE" + block
            
            # Extract table name
            table_match = block.split('\n')[0].replace('CREATE TABLE', '').strip()
            table_name = table_match.split('(')[0].strip()
            
            documents.append(block)
            ids.append(f"table_{table_name}_{i}")
            metadatas.append({"table": table_name, "type": "table_definition"})
        
        # Add to Chroma collection
        if documents:
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
    
    def retrieve_relevant_schema(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Retrieve relevant schema information based on natural language query.
        
        Args:
            query: Natural language query
            n_results: Number of results to retrieve
            
        Returns:
            List of relevant schema documents
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, len(self.collection.get()['ids']) or 1)
        )
        
        retrieved_info = []
        
        if results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                retrieved_info.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else None
                })
        
        return retrieved_info
    
    def get_context_for_sql_generation(self, natural_language_query: str) -> str:
        """
        Get schema context for SQL generation based on natural language query.
        
        Args:
            natural_language_query: User's natural language question
            
        Returns:
            Formatted schema context for the LLM
        """
        retrieved = self.retrieve_relevant_schema(natural_language_query)
        
        context = "# Relevant Database Schema\n\n"
        
        for item in retrieved:
            context += f"```sql\n{item['content']}\n```\n\n"
        
        return context
    
    def clear_collection(self) -> None:
        """Clear the schema collection."""
        try:
            self.client.delete_collection(name="database_schema")
            self.collection = self.client.get_or_create_collection(
                name="database_schema",
                metadata={"hnsw:space": "cosine"}
            )
        except Exception as e:
            print(f"Error clearing collection: {e}")
