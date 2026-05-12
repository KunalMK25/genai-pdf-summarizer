import gradio as gr
from transformers import pipeline
from pypdf import PdfReader

# Load lightweight models
summarizer = pipeline(
    "summarization",
    model="Falconsai/text_summarization"
)

sentiment = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_pdf(pdf_file):
    text = ""

    # Read PDF
    reader = PdfReader(pdf_file)

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Prevent huge inputs
    text = text[:1000]

    # Generate summary
    summary = summarizer(
        text,
        max_length=60,
        min_length=20,
        do_sample=False
    )

    # Sentiment
    sentiment_result = sentiment(text[:500])

    return (
        summary[0]["summary_text"],
        sentiment_result[0]["label"]
    )

# Gradio UI
app = gr.Interface(
    fn=analyze_pdf,
    inputs=gr.File(label="Upload PDF"),
    outputs=[
        gr.Textbox(label="Summary"),
        gr.Textbox(label="Sentiment")
    ],
    title="GenAI PDF Summarizer",
    description="Upload a PDF to generate summary and sentiment analysis."
)

app.launch(server_name="0.0.0.0", server_port=7860)