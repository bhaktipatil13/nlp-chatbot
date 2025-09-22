from app.chatbot_logic import answer_query

if __name__ == "__main__":
    print("📊 Bajaj Finserv Q&A Bot (CLI)")
    while True:
        q = input("You: ")
        if q.lower() in ["exit", "quit"]:
            break
        results = answer_query(q)
        for r in results:
            print(f"- (from {r['source']}) {r['text']}")
