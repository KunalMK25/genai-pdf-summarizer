from transformers import pipeline
from pypdf import PdfReader

# =========================
# LOAD PDF
# =========================

reader = PdfReader("sample.pdf")

text = ""

for page in reader.pages:
    extracted = page.extract_text()

    if extracted:
        text += extracted

# =========================
# LIGHTWEIGHT SUMMARIZER
# =========================

summarizer = pipeline(
    "summarization",
    model="Falconsai/text_summarization"
)

# =========================
# SENTIMENT ANALYSIS
# =========================

sentiment = pipeline(
    "sentiment-analysis"
)

# =========================
# GENERATE SUMMARY
# =========================

summary = summarizer(
    text[:1000],
    max_length=60,
    min_length=20,
    do_sample=False
)

# =========================
# SENTIMENT RESULT
# =========================

sentiment_result = sentiment(text[:500])

# =========================
# OUTPUT
# =========================

print("\n========== SUMMARY ==========\n")

print(summary[0]["summary_text"])

print("\n========== SENTIMENT ==========\n")

print(sentiment_result)