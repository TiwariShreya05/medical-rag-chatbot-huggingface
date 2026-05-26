import gradio as gr
from rag import answer

def chat(message, history):
    return answer(message)

app = gr.ChatInterface(
    fn=chat,
    title="Medical RAG Chatbot",
    description="Ask medical questions. Answers come from your uploaded textbooks.",
    examples=[
        "What is the function of the heart?",
        "What are symptoms of diabetes?",
        "How does the brain control movement?"
    ]
)

if __name__ == "__main__":
    app.launch()