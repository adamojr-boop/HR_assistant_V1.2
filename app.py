import chainlit as cl
from langchain_openai import ChatOpenAI
from hr_assistant.database import Database
from hr_assistant.document_processor import DocumentProcessor
from hr_assistant.config import OPENAI_API_KEY

db = Database()
processor = DocumentProcessor(db)
processor.sync_documents()

collection = db.get_collection()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=OPENAI_API_KEY)

@cl.on_message
async def main(message: cl.Message):
    user_query = message.content

    results = collection.query(
        query_texts=[user_query],
        n_results=10
    )
    
    retrieved_chunks = results.get("documents", [[]])[0]
    context = "\n\n".join(retrieved_chunks) if retrieved_chunks else "Nessun documento trovato."

    prompt = f"""
Sei un assistente HR esperto, preciso e rigoroso. 
Analizza il contesto dei curriculum forniti per rispondere alla domanda dell'utente.

REGOLE FONDAMENTALI:
1. Basati ESCLUSIVAMENTE sulle informazioni presenti nel contesto. Non inventare mai candidati, esperienze o competenze che non compaiono nei testi.
2. Estrai sempre il nome e cognome reale del candidato leggendolo dal testo o dal nome del file di origine.
3. Se la risposta non è presente nei documenti o il requisito non è soddisfatto, rispondi chiaramente che non ci sono candidati con quei requisiti nel database.
4. Concentrati sull'accuratezza e sull'estrazione puntuale delle competenze del candidato o dei candidati pertinenti trovati nel contesto.

Struttura la risposta in questo modo:
- **Candidato/i Individuati:** (Nome e Cognome reali, oppure "Nessuno")
- **Competenze Rilevanti / Analisi:** (Elenco puntato delle competenze estratte dai testi coerenti con la domanda)
- **Motivazione:** (Spiegazione chiara del perché il profilo è idoneo o perché non sono presenti risposte)

Contesto (Curriculum):
{context}

Domanda: {user_query}
"""

    response = llm.invoke(prompt)

    await cl.Message(content=response.content).send()
    
 #poetry run chainlit run app.py -w ---> Avvia L'app in Chainlit con interfaccia web