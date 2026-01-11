from ingestion.loaders.filesystem import load_folder
from ingestion.loaders.github import load_github_repo

def ingest(source: str, source_type: str):
    if source_type == "folder":
        return load_folder(source)

    if source_type == "github":
        return load_github_repo(source)

    raise ValueError("Unsupported source type")



docs = ingest("/Users/muhamedadil/gitea/chatbot", "folder")
print(len(docs))
print(docs[0].metadata)
