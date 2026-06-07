import os
import re

DOCS_PATH = "./documents"

def clean_text(text):
    """Remove header and noisy lines, keep only review content."""
    # Skip everything before the first review
    marker = "QUALITY"
    idx = text.find(marker)
    if idx != -1:
        text = text[idx:]

    skip_phrases = [
        "Rate My Professors", "ratemyprofessors.com", "Advertisement",
        "Helpful", "Shop Now", "Site Guidelines", "Terms & Conditions",
        "Privacy Policy", "All Rights Reserved", "Do Not Sell",
        "COS -", "Discover Summer", "1:57 PM", "6/7/26",
        "Rate", "Compare", "Student Ratings",
    ]

    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if any(phrase in line for phrase in skip_phrases):
            continue
        if re.match(r'^\d+$', stripped):        # just a number
            continue
        if re.match(r'^\d+/\d+$', stripped):    # page number like 2/12
            continue
        if re.match(r'^\d+:\d+$', stripped):    # timestamp like 00:03
            continue
        cleaned.append(line)

    return "\n".join(cleaned)

def load_documents():
    """Load all .txt files from the documents folder."""
    documents = []
    for filename in sorted(os.listdir(DOCS_PATH)):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            text = clean_text(text)
            professor_name = filename.replace(".txt", "").replace("Land", "").strip()
            print(professor_name)
            documents.append({
                "professor": professor_name,
                "filename": filename,
                "text": text,
            })
    print(f"Loaded {len(documents)} document(s): {[d['professor'] for d in documents]}")
    return documents

def chunk_document(text, professor_name):
    """Split a document into chunks using a sliding window."""
    chunk_size = 250
    overlap = 50
    min_length = 50

    chunks = []
    prefix = professor_name.lower().replace(" ", "_")
    counter = 0
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end].strip()
        if len(chunk_text) >= min_length:
            chunks.append({
                "text": chunk_text,
                "professor": professor_name,
                "chunk_id": f"{prefix}_{counter}",
            })
            counter += 1
        start += chunk_size - overlap

    return chunks

if __name__ == "__main__":
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc["text"], doc["professor"])
        all_chunks.extend(chunks)
        print(f"{doc['professor']}: {len(chunks)} chunks")

    print("\n--- 5 Representative Chunks ---")
    sample_indices = [i * (len(all_chunks) // 5) for i in range(5)]
    for i, idx in enumerate(sample_indices):
        chunk = all_chunks[idx]
        print(f"\nChunk {i+1} [{chunk['professor']}] (id: {chunk['chunk_id']})")
        print(chunk["text"][:500] + "...")