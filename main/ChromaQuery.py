import chromadb
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s',)

chroma_client = chromadb.PersistentClient(path="C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/DB")
collection = chroma_client.get_or_create_collection(name="summarized_collection")

results = collection.query(
    query_texts=["Emails where Carol talks about a waiver"],
    n_results=5,
    where={"Kind": "Email"},
    where_document={"$contains":"Carol"}
)

print(results)
document_ids = results['ids'][0]

nuix_query = []
for doc_id in document_ids:
    nuix_query.append(doc_id)

print(f'document-id:({" OR ".join(nuix_query)})')
