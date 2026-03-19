# ingest.py

import os
from dotenv import load_dotenv

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.reader.pdf_reader import PDFReader

# -----------------------
# Load env (LOCAL only)
# -----------------------
load_dotenv()

DB_URL = os.getenv("DB_URL")
PDF_PATH = "data/intro-to-ml.pdf"

reader = PDFReader(
    chunk=True,
    chunk_size=800,
    split_on_pages=True
)

def main():
    kb = Knowledge(
        vector_db=PgVector(
            table_name="pdf_documents",
            schema="ai",  # IMPORTANT (my table is here)
            db_url=DB_URL,
        ),
    )

    print("🚀 Starting ingestion...")

    kb.insert(
        path=PDF_PATH,
        skip_if_exists=False,  # force fresh load if needed
        reader=reader
    )

    print("✅ Ingestion complete!")

if __name__ == "__main__":
    main()