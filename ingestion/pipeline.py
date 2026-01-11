from ingestion.loaders.filesystem import load_folder
from ingestion.loaders.github import load_github_repo
from ingestion.chunking import chunk_document
from indexing.indexer import Indexer

def ingest_and_index(source: str, source_type: str):
    if source_type == "folder":
        docs = load_folder(source)
    elif source_type == "github":
        docs = load_github_repo(source)
    else:
        raise ValueError("Unsupported source type")

    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_document(doc))

    indexer = Indexer()
    indexer.index_chunks(all_chunks)

    return len(all_chunks)


num_chunks = ingest_and_index("https://github.com/adilzubair/scripts", "github")
print(f"Successfully ingested and indexed {num_chunks} chunks.")
