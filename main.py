import os  # <-- this was missing
from flask import Flask, render_template, request, jsonify
from app.chatbot_logic import answer_query

# Absolute path to templates folder
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get("question")
    results = answer_query(question, top_k=3)  # get top 3 matches

    if isinstance(results, list) and len(results) > 0:
        answers = [f"- {r.get('text', '')}" for r in results]
        best_answer = "\n".join(answers)
    elif isinstance(results, str):
        best_answer = results
    else:
        best_answer = "Sorry, I couldn’t find an answer."

    return jsonify({"answer": best_answer})

if __name__ == '__main__':
    # Use Render's PORT environment variable, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
