import chromadb
import glob
import logging
import os
import csv

logging.basicConfig(level=logging.INFO, format='%(message)s',)


def get_text(file_path):
    data = None
    try:
        with open(file_path) as file:
            data = file.read()
    except Exception as e:
        logging.error(f'Cannot read file {file_path}, {e}')
        return None

    return data


chroma_client = chromadb.PersistentClient(path="C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/DB")
collection = chroma_client.get_or_create_collection(name="summarized_collection")

# Build metadata dict
reader = csv.DictReader(open("C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/Metadata/metadata.csv", "r"))
metadata = {}

for row in reader:
    key = row.pop('Document IDs')
    metadata[key] = row


# Add summarized documents to ChromaDB
summarized_documents = glob.glob("C:/Users/ecunningham01/OneDrive - Nuix.com/Desktop/Chat to Code Base/Summarized/*.txt")
for summarized_file_path in summarized_documents:
    id = str(os.path.basename(summarized_file_path)).split(".")[0]
    document = get_text(summarized_file_path)
    document_metadata = metadata[id]

    collection.add(
        documents=[document],
        metadatas=[document_metadata],
        ids=[id]
    )

    logging.info("Loaded " + str(id) + " into ChromaDB")
