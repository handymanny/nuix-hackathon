import sys
import chromadb
import argparse

# Parse arguments passed down from script
parser = argparse.ArgumentParser()
parser.add_argument('--query')
parser.add_argument('--results')
parser.add_argument('--containstext')
parser.add_argument('--metadatafield')
parser.add_argument('--metadatavalue')
args = parser.parse_args()

text_query = str(args.query)
results = int(args.results)
contains_text = str(args.containstext)
metadata_field = str(args.metadatafield)
metadata_value = str(args.metadatavalue)

# Initialize connection to DB
chroma_client = chromadb.PersistentClient(path="C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/DB")
collection = chroma_client.get_or_create_collection(name="summarized_collection")

# Generate query
where_metadata = {}
if metadata_field is not None and metadata_value is not None:
    where_metadata[metadata_field] = metadata_value
else:
    where_metadata = None

where_document = {}
if contains_text is not None:
    where_document["$contains"] = contains_text
else:
    where_document = None

results = collection.query(
    query_texts=[text_query],
    n_results=results,
    where=where_metadata,
    where_document=where_document
)

# Get results as Nuix query string
document_ids = results['ids'][0]

nuix_query = []
for doc_id in document_ids:
    nuix_query.append(doc_id)

print(f'document-id:({" OR ".join(nuix_query)})')
