import gradio as gr
from rag_hf import answer

def chat(message, history):
    return answer(message)

app = gr.ChatInterface(
    fn=chat,
    title="Medical RAG Chatbot — HuggingFace + Llama 3",
    description="Ask medical questions. Powered by HuggingFace embeddings and Llama 3.",
    examples=[
        "What is the function of the heart?",
        "How does the nervous system work?",
        "What are the types of muscle tissue?"
    ]
)

if __name__ == "__main__":
    app.launch(server_port=7861)