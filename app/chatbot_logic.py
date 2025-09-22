import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Define project paths
project_root = Path(__file__).resolve().parent.parent
from pathlib import Path
import os

# Use current working directory as base for Render deployment
data_dir = Path(os.getcwd()) / "data"

print("Data folder path:", data_dir)
print("Exists?", data_dir.exists())
print("PDF files:", list(data_dir.glob("*.pdf")))



# Collect PDF files
pdf_files = list(data_dir.glob("*.pdf"))
if not pdf_files:
    raise FileNotFoundError(f"No PDF files found in '{data_dir}'. Make sure you include them in deployment.")

# Function to extract text from a single PDF
def extract_text_from_pdf(path):
    text = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
    except Exception as e:
        print(f"Warning: Could not read '{path}': {e}")
    return "\n".join(text)

# Build corpus and sources safely
corpus = []
sources = []
for pdf in pdf_files:
    text = extract_text_from_pdf(pdf)
    if not text.strip():
        print(f"Warning: PDF '{pdf.name}' is empty or could not extract text.")
        continue
    # Split into paragraphs longer than 50 chars
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
    if not paragraphs:
        print(f"Warning: PDF '{pdf.name}' has no paragraphs longer than 50 chars.")
        continue
    corpus.extend(paragraphs)
    sources.extend([pdf.name] * len(paragraphs))

if not corpus:
    raise ValueError("Corpus is empty! Make sure your PDFs contain readable text.")

# Vectorize corpus
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)

# Query function
def answer_query(query, top_k=3):
    if not query.strip():
        return [{"score": 0.0, "source": None, "text": "Please enter a valid query."}]
    
    q_vec = vectorizer.transform([query])
    sims = cosine_similarity(q_vec, X).flatten()
    idxs = sims.argsort()[::-1][:top_k]
    results = []
    for i in idxs:
        results.append({
            "score": float(sims[i]),
            "source": sources[i],
            "text": corpus[i]
        })
    return results
