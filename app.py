import streamlit as st
from auth import check_password

# -----------------------
# Password protection
# -----------------------
if not check_password("ML Concepts Instructor"):
    st.stop()

# -----------------------
# Imports
# -----------------------
import uuid
from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.tools.duckduckgo import DuckDuckGoTools
from sqlalchemy import create_engine # You DO need this now

# -----------------------
# Config
# -----------------------
st.set_page_config(page_title="ML Research Team", page_icon="📚")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
DB_URL = st.secrets["DB_URL"]

LLM = OpenAIChat(id="gpt-4o-mini", api_key=OPENAI_API_KEY)

# -----------------------
# Knowledge base (NO INSERT)
# -----------------------
@st.cache_resource
def get_knowledge():
    # 1. Create a custom engine that handles the Neon/Pooler timeouts
    custom_engine = create_engine(
        DB_URL,
        pool_pre_ping=True,  # Checks the connection before using it
        pool_recycle=300,    # Refreshes the connection every 5 minutes
    )

    # 2. Pass the engine directly to PgVector
    return Knowledge(
        vector_db=PgVector(
            table_name="pdf_documents",
            schema="ai",
            db_engine=custom_engine, # Use db_engine instead of db_url
        )
    )

knowledge_base = get_knowledge()

# -----------------------
# Agents
# -----------------------
@st.cache_resource
def build_team():

    # 📚 Librarian (RAG agent)
    librarian = Agent(
        name="Librarian",
        role="Machine Learning Textbook Expert",
        model=LLM,
        knowledge=knowledge_base,
        search_knowledge=True,
        add_knowledge_to_context=True,
        instructions=[
            "Search the 'pdf_documents' table in the ai schema.",
            "You MUST cite the textbook explicitly.",
            "Every factual statement must include a citation.",
            "Use this format exactly: (intro-to-ml.pdf, p. <page_number>)",
            "Do not answer without page citations.",
            "If no relevant content is found, say: 'The textbook does not cover this topic.'"
        ],
    )

    web_researcher = Agent(
        name="Web Researcher",
        role="ML Industry Trends Expert",
        model=LLM,
        tools=[DuckDuckGoTools()],
        instructions=[
            "Search for recent (2025–2026) machine learning info.",
            "For every claim you make, you MUST provide the source URL in parentheses.", # Added emphasis
            "At the end of your response, provide a bulleted 'Source List' with full URLs.",
            "Clearly separate this section as 'External Sources'.",
        ],
    )

    return Team(
        name="ML Research Team",
        model=LLM,
        members=[librarian, web_researcher],
        instructions=[
            "Always call Librarian first.",
            "Do NOT answer directly.",
            "Return Librarian's answer exactly as is.",

            "If Librarian says the textbook does not cover the topic:",
            "Then call Web Researcher.",

            "Never fabricate citations.",
            "Never guess page numbers.",
            "Preserve Librarian citations exactly.",

            "Append Web Researcher output under 'External Sources'."
            
        ],
        markdown=True,
    )

research_team = build_team()

# -----------------------
# UI
# -----------------------
st.title("📚 Understand ML Fundamentals")
st.markdown(
    '<p style="font-size:10px; color:gray; text-align:left;">© 2026 Developed by John M. using Agno AI and Neon (RAG)</p>',
    unsafe_allow_html=True,
) 
st.write("Ask ML questions with grounded textbook answers.")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# Chat
# -----------------------
user_input = st.chat_input("Ask a machine learning question...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("🔍 Researching..."):
        try:
            response = research_team.run(
                user_input,
                session_id=st.session_state.session_id
            )
            final_answer = response.content
        except Exception as e:
            final_answer = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(final_answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer
    })
