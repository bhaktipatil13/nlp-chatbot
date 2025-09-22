from flask import Flask, render_template, request, jsonify
from app.chatbot_logic import answer_query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get("question")
    results = answer_query(question, top_k=3)  # get top 3 matches

    if isinstance(results, list) and len(results) > 0:
        # Format all matches into a clean string
        answers = [f"- {r.get('text', '')}" for r in results]
        best_answer = "\n".join(answers)
    elif isinstance(results, str):
        best_answer = results
    else:
        best_answer = "Sorry, I couldn’t find an answer."

    return jsonify({"answer": best_answer})

if __name__ == '__main__':
    app.run(debug=True)
