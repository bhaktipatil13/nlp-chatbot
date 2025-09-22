import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path


project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"
pdf_files = list(data_dir.glob("*.pdf"))

def extract_text_from_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)


corpus = []
sources = []
for pdf in pdf_files:
    text = extract_text_from_pdf(pdf)
    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]
    corpus.extend(paragraphs)
    sources.extend([pdf.name] * len(paragraphs))


vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(corpus)

def answer_query(query, top_k=3):
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



