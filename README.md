---

```markdown
# 📚 ML Research Team (RAG with Neon + Streamlit)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A **Retrieval-Augmented Generation (RAG)** application built with **Streamlit**, **Agno AI**, and **Neon (PostgreSQL + pgvector)**.

It answers Machine Learning questions using:
- 📖 **Textbook-grounded responses (with strict citations)**
- 🌐 **Fallback web research for recent topics (2025–2026)**

---

## 🚀 Features

- 🔐 Password-protected access
- 📚 RAG-based retrieval from PDF embeddings
- 🤖 Multi-agent system:
  - **Librarian Agent** → textbook answers
  - **Web Researcher Agent** → latest ML info
- 🧠 Strict citation enforcement
- 💬 Chat interface with session memory
- ⚡ Optimized Neon DB connections

---

## 🏗️ Architecture

```

User Question
↓
Team Agent
↓
Librarian Agent (RAG)
↓ (if no result)
Web Researcher Agent
↓
Final Answer (citations + sources)

```

---

## 📦 Tech Stack

- **Frontend:** Streamlit  
- **LLM:** OpenAI (`gpt-4o-mini`)  
- **Agents:** Agno AI  
- **Database:** Neon (PostgreSQL + pgvector)  
- **Search:** DuckDuckGo  
- **ORM:** SQLAlchemy  

---

## 📁 Project Structure

```

.
├── app.py
├── auth.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .streamlit/
└── secrets.toml

````

---

## 🐳 Docker Setup

### 1. Build the image
```bash
docker build -t rag-with-neon .
````

### 2. Run the app

```bash
docker-compose up
```

---

## ⚙️ docker-compose.yml

```yaml
version: "3.9"

services:
  app:
    build: .
    container_name: rag-app
    ports:
      - "8501:8501"
    volumes:
      - .:/app
    restart: always
```

---

## 🐋 Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 📦 requirements.txt

```txt
streamlit
agno
openai
sqlalchemy
psycopg2-binary
pgvector
duckduckgo-search
```

---

## 🔑 Environment Variables

Create `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-openai-api-key"
DB_URL = "your-neon-postgres-connection-string"
```

---

## 📚 Knowledge Base Setup

* PostgreSQL (Neon) with `pgvector`
* Table:

  * **Schema:** `ai`
  * **Table:** `pdf_documents`
* ⚠️ Embeddings must already be inserted (no ingestion pipeline included)

---

## 🤖 Agent Behavior

### 📖 Librarian Agent

* Searches textbook embeddings
* Enforces strict citation format:

  ```
  (intro-to-ml.pdf, p. <page_number>)
  ```
* If no answer:

  ```
  The textbook does not cover this topic.
  ```

---

### 🌐 Web Researcher Agent

* Activated only if Librarian fails
* Focus: **recent ML (2025–2026)**
* Requirements:

  * Every claim must include a URL
  * Output must include:

    * Inline citations
    * `External Sources` section

---

### 🧠 Team Rules

* Always call Librarian first
* Never fabricate citations
* Never guess page numbers
* Preserve citation formatting
* Append web results under **External Sources**

---

## 🖥️ UI Overview

* Chat-based interface
* Session-based memory
* Real-time spinner feedback
* Clean academic design

---

## 🔐 Authentication

```python
check_password("ML Concepts Instructor")
```

---

## ⚠️ Notes

* Ensure Neon DB has `pgvector` enabled
* Connection pooling settings:

  * `pool_pre_ping=True`
  * `pool_recycle=300`
* Designed for **read-only RAG (no ingestion)**

---

## 🧪 Example Query

```
What is gradient descent?
```

**Output:**

* 📖 Textbook explanation with citations
* 🌐 External sources (if needed)

---

## 📌 Future Improvements

* PDF ingestion pipeline
* Multi-document support
* Citation highlighting
* User authentication system
* Streaming responses
* UI enhancements

---

## 👨‍💻 Author

**John M.**
Built with Agno AI + Neon (RAG architecture)

---

## 📄 License

MIT License


