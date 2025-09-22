import os
from flask import Flask, render_template, request, jsonify
from app.chatbot_logic import answer_query

# Absolute path to templates folder (must be next to main.py)
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir, static_folder="static")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get("question")
    results = answer_query(question, top_k=3)  # get top 3 matches

    if isinstance(results, list) and len(results) > 0:
        # Return full list so frontend can render structured data
        return jsonify({"answer": results})
    elif isinstance(results, str):
        return jsonify({"answer": results})
    else:
        return jsonify({"answer": "Sorry, I couldn’t find an answer."})

if __name__ == '__main__':
    # Use Render's PORT env var, default to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
