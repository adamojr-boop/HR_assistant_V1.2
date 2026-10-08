from .database import Database
from .document_processor import DocumentProcessor
from .config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI

db = Database()
processor = DocumentProcessor(db)
processor.sync_documents()
collection = db.get_collection()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

def get_database_stats() -> int:
    """Restituisce il numero di chunk nel database."""
    return collection.count()

def reindex_database() -> int:
    """Forza la risincronizzazione e restituisce il nuovo conteggio."""
    processor.sync_documents()
    return collection.count()

def ask_hr_assistant(user_query: str) -> str:
    """Gestisce la ricerca nei CV e l'interrogazione al LLM."""
    results = collection.query(query_texts=[user_query], n_results=10)
    retrieved_chunks = results.get("documents", [[]])[0]
    context = "\n\n".join(retrieved_chunks) if retrieved_chunks else "Nessun documento trovato."

    prompt = f"""
Sei un assistente HR esperto, preciso e rigoroso. 
Analizza il contesto dei curriculum forniti per rispondere alla domanda dell'utente.
... [resto del prompt] ...
Contesto (Curriculum): {context}
Domanda: {user_query}
"""
    response = llm.invoke(prompt)
    return response.content