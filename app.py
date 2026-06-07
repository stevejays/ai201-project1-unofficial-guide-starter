import gradio as gr
from ingest import load_documents, chunk_document
from retriever import get_collection, embed_and_store, retrieve
from generator import generate_response

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

def handle_query(question):
    chunks = retrieve(question)
    result = generate_response(question, chunks)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

# Run ingestion on startup
ingest()

with gr.Blocks() as demo:
    gr.Markdown("# 🎓 UChicago Unofficial Professor Guide")
    inp = gr.Textbox(label="Your question")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()