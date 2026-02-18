# Enterprise AI Analytics Copilot
 

🟢 Production Deployed on Streamlit Cloud  
Auto-deploy enabled via GitHub integration.

A sophisticated MVP application that converts the natural language queries to SQL using OpenAI, with RAG-powered schema awareness and security validation.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Features

- **Natural Language to SQL**: Convert plain English questions to SQL queries using OpenAI GPT-3.5
- **RAG Architecture**: Retrieval-Augmented Generation with Chroma vector database for schema-aware SQL generation
- **Security Validation**: SQL Guard module blocks dangerous operations (DROP, DELETE, UPDATE, ALTER, etc.)
- **SQLite Warehouse**: Mock analytics warehouse with the sample schema
- **Streamlit UI**: Interactive web interface for query building and execution
- **Modular Design**: Clean separation of concerns with dedicated modules

## 📋 Architecture

```
enterprise-ai-analytics-copilot/
├── app.py              # Main Streamlit application
├── rag.py              # RAG system with Chroma vector DB
├── sql_guard.py        # SQL validation and security checks
├── sample_schema.txt   # Database schema definition
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── analytics.db       # SQLite database (generated)
```

### Module Breakdown

| Module | Purpose |
|--------|---------|
| `app.py` | Streamlit UI, orchestrates copilot workflow |
| `rag.py` | SchemaRAG class for vector-based schema retrieval |
| `sql_guard.py` | SQLGuard class for SQL validation and sanitization |
| `sample_schema.txt` | CREATE TABLE statements for sample database |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/enterprise-ai-analytics-copilot.git
   cd enterprise-ai-analytics-copilot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up an OpenAI API key**
   - You'll be prompted to enter your API key in the Streamlit sidebar when running the app

### Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Initialize the system**
   - Open the app in your browser (typically `http://localhost:8501`)
   - Paste your OpenAI API key in the sidebar
   - Click "Initialize System" to load the schema into the RAG system

3. **Ask questions**
   - Type your natural language query (e.g., "Show me top 10 customers by total spend")
   - Click "Generate SQL" to convert to SQL
   - Review the generated SQL
   - Click "Execute" to run the query against the SQLite database

## 📊 Sample Queries

Try these natural language queries:

- "How many customers do we have from each country?"
- "Show me the top 5 products by revenue"
- "What is the average order value by subscription tier?"
- "How many orders were placed in the last 30 days?"
- "Show me customer email addresses for orders over $1000"

## 🛡️ Security Features

### SQL Guard Protections

The SQLGuard module provides:
- ✅ **Whitelist approach**: Only SELECT queries allowed
- ✅ **Keyword blocking**: Prevents DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, GRANT, REVOKE
- ✅ **Query validation**: Checks for SQL syntax compliance
- ✅ **Sanitization**: Removes extra whitespace and normalizes queries

### How It Works

1. User submits natural language query
2. OpenAI converts to SQL
3. SQLGuard validates the query
4. Only safe queries execute against the database
5. Results returned to user

## 📦 Database Schema

The sample schema includes:

- **customers**: Customer information and subscription details
- **orders**: Order records with totals and status
- **products**: Product catalog with pricing and inventory
- **order_items**: Line items for each order
- **suppliers**: Supplier information and ratings
- **analytics_events**: User activity events

See `sample_schema.txt` for full CREATE TABLE statements.

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.28.1 | Web UI framework |
| openai | 0.27.8 | GPT API access |
| chromadb | 0.3.21 | Vector database for RAG |
| pydantic | 2.0.0 | Data validation |
| requests | 2.31.0 | HTTP requests |

## 📝 Configuration

### Environment Variables

Optional (can be set in `.env` file):
```bash
OPENAI_API_KEY=your-api-key-here
CHROMA_DB_PATH=./chroma_db
SQLITE_DB_PATH=./analytics.db
```

### Streamlit Configuration

Create a `~/.streamlit/config.toml` for custom settings:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
maxUploadSize = 200
```

## 🧪 Testing

### Manual Testing

1. Test with simple queries:
   ```
   "Show all customers"
   "How many orders are there?"
   ```

2. Test SQL Guard protection:
   ```
   "Delete all customers"  # Should be blocked
   "Drop the orders table" # Should be blocked
   ```

3. Test schema awareness:
   ```
   "Show me data from non-existent table xyz"  # Should generate valid SQL for real tables
   ```

## 🚀 Future Enhancements

- [ ] Multi-table JOIN optimization with RAG
- [ ] Query history and saved queries
- [ ] Custom prompt templates
- [ ] Support for multiple warehouse types (PostgreSQL, Snowflake)
- [ ] Real-time query performance insights
- [ ] Advanced RAG with few-shot examples
- [ ] User authentication and audit logging
- [ ] Caching for frequently asked questions
- [ ] Export results to CSV/Excel

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Use Black for formatting
- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Include type hints

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔐 Security Notice

- **Never commit API keys** or sensitive credentials
- Use environment variables for sensitive data
- Review generated SQL before execution in production
- Implement proper authentication in production deployments
- The SQLGuard provides basic protection but should be supplemented with database-level permissions

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Provide detailed description of the problem
- Include error messages and steps to reproduce

## Acknowledgments

- OpenAI for the GPT-3.5 API
- Streamlit for the fantastic web framework
- Chroma for the vector database
- The Python community

---

**Version**: 1.0.0 MVP  
**Last Updated**: February 2026  
**Status**: Production Ready
