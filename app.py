from ingest import load_documents, chunk_document
from retriever import get_collection, embed_and_store, retrieve

def ingest():
    collection = get_collection()
    if collection.count() > 0:
        print(f"Vector store already populated ({collection.count()} chunks). Skipping ingestion.")
        return
    
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["professor"])
        all_chunks.extend(chunks)
    
    embed_and_store(all_chunks)

if __name__ == "__main__":
    ingest()
    
    # Test retrieval
    query = "Is Fineschi a good professor?"
    print(f"\nTest query: {query}")
    results = retrieve(query)
    for r in results:
        print(f"\n[{r['professor']}] (dist: {r['distance']:.3f})")
        print(r['text'][:150])