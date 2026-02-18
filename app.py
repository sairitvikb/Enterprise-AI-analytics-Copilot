"""
Enterprise AI Analytics Copilot - Main Application
Streamlit UI for natural language to SQL conversion with RAG and security validation.
"""

import os
import sqlite3
import streamlit as st
from typing import Optional, Tuple
import openai

from rag import SchemaRAG
from sql_guard import SQLGuard


# Configure page
st.set_page_config(
    page_title="Enterprise AI Analytics Copilot",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
    <style>
    .stTitle {
        color: #1f77b4;
    }
    .query-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


class AnalyticsCopilot:
    """Main application class for the Analytics Copilot."""
    
    def __init__(self):
        """Initialize the copilot application."""
        self.rag = SchemaRAG()

        self.sql_guard = SQLGuard()
        self.db_path = "analytics.db"
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize SQLite database with sample data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Create tables from schema
            with open("sample_schema.txt", 'r') as f:
                schema_content = f.read()
            
            # Execute schema creation (SQLite doesn't need all CREATE TABLE syntax)
            for statement in schema_content.split(";"):
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except sqlite3.OperationalError as e:
                        if "already exists" not in str(e):
                            pass  # Table already exists
            
            conn.commit()
        except Exception as e:
            st.warning(f"Database initialization note: {e}")
        finally:
            conn.close()
    
    def load_schema_to_rag(self) -> None:
        """Load database schema into RAG system."""
        try:
            self.rag.load_schema_from_file("sample_schema.txt")
            st.success("✅ Schema loaded into RAG system")
        except Exception as e:
            st.error(f"Error loading schema: {e}")
    
    def convert_nl_to_sql(self, natural_language_query: str, api_key: str) -> Optional[str]:
        """
        Convert natural language query to SQL using OpenAI.
        
        Args:
            natural_language_query: User's natural language question
            api_key: OpenAI API key
            
        Returns:
            Generated SQL query or None if error
        """
        try:
            openai.api_key = api_key
            
            # Get relevant schema context
            schema_context = self.rag.get_context_for_sql_generation(natural_language_query)
            
            # Create prompt for SQL generation
            prompt = f"""You are a SQL expert. Convert the following natural language query to a valid SQL query.

{schema_context}

Natural Language Query:
{natural_language_query}

Requirements:
- Only use tables and columns from the schema provided above
- Return ONLY the SQL query, no explanations
- The query must be a SELECT statement
- Use proper SQL syntax for SQLite

SQL Query:"""
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a SQL expert that converts natural language to SQL queries. Always return only the SQL query without markdown formatting or explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            sql_query = response['choices'][0]['message']['content'].strip()
            
            # Remove markdown code blocks if present
            if sql_query.startswith("```"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return sql_query
        
        except openai.error.AuthenticationError:
            st.error("❌ Invalid OpenAI API key. Please check your credentials.")
            return None
        except openai.error.RateLimitError:
            st.error("❌ Rate limit exceeded. Please try again later.")
            return None
        except Exception as e:
            st.error(f"❌ Error generating SQL: {str(e)}")
            return None
    
    def validate_and_execute_sql(self, sql_query: str) -> Tuple[bool, Optional[list], str]:
        """
        Validate SQL query for security and execute it.
        
        Args:
            sql_query: SQL query to validate and execute
            
        Returns:
            Tuple of (success: bool, results: list, message: str)
        """
        # Validate query safety
        is_safe, validation_message = self.sql_guard.is_safe_query(sql_query)
        
        if not is_safe:
            return False, None, f"🚫 Security Check Failed: {validation_message}"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            conn.close()
            
            return True, results, f"✅ Query executed successfully. {len(results)} rows returned."
        
        except sqlite3.Error as e:
            return False, None, f"❌ Database Error: {str(e)}"
        except Exception as e:
            return False, None, f"❌ Error executing query: {str(e)}"


def main():
    """Main Streamlit application."""
    st.title("🔍 Enterprise AI Analytics Copilot")
    st.markdown("Convert natural language queries to SQL with RAG and security validation")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key for natural language to SQL conversion"
        )
        
        if st.button("🔄 Initialize System", use_container_width=True):
            with st.spinner("Initializing..."):
                copilot = AnalyticsCopilot()
                copilot.load_schema_to_rag()
                st.session_state.copilot = copilot
        
        st.divider()
        st.info(
            "**How to use:**\n"
            "1. Enter your OpenAI API key\n"
            "2. Click 'Initialize System'\n"
            "3. Ask a natural language question about the data\n"
            "4. Review the generated SQL\n"
            "5. Execute the query"
        )
    
    # Initialize copilot if not in session state
    if "copilot" not in st.session_state:
        copilot = AnalyticsCopilot()
        copilot.load_schema_to_rag()
        st.session_state.copilot = copilot
    else:
        copilot = st.session_state.copilot
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Natural Language Query")
        natural_language_query = st.text_area(
            "Ask a question about your data:",
            placeholder="e.g., 'Show me total sales by customer country for the last 30 days'",
            height=120
        )
    
    with col2:
        st.subheader("Actions")
        if st.button("🚀 Generate SQL", use_container_width=True, key="generate"):
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar")
            elif not natural_language_query:
                st.error("Please enter a natural language query")
            else:
                with st.spinner("Generating SQL..."):
                    sql_query = copilot.convert_nl_to_sql(natural_language_query, api_key)
                    if sql_query:
                        st.session_state.generated_sql = sql_query
    
    # Display generated SQL
    if "generated_sql" in st.session_state:
        st.divider()
        st.subheader("🔧 Generated SQL Query")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            sql_display = st.text_area(
                "Review and edit the SQL query:",
                value=st.session_state.generated_sql,
                height=200,
                key="sql_editor"
            )
        
        with col2:
            if st.button("▶️ Execute", use_container_width=True, key="execute"):
                with st.spinner("Executing query..."):
                    success, results, message = copilot.validate_and_execute_sql(sql_display)
                    st.session_state.execution_success = success
                    st.session_state.execution_results = results
                    st.session_state.execution_message = message
        
        # Display execution results
        if "execution_message" in st.session_state:
            st.divider()
            st.subheader("📊 Results")
            st.info(st.session_state.execution_message)
            
            if st.session_state.execution_success and st.session_state.execution_results:
                st.write(st.session_state.execution_results)
    
    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("🛡️ SQL Guard: DROP, DELETE, UPDATE blocked")
    with col2:
        st.caption("🧠 RAG: Schema-aware SQL generation")
    with col3:
        st.caption("🔐 SQLite: Mock analytics warehouse")


if __name__ == "__main__":
    main()
