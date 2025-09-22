async function sendMessage() {
    const questionInput = document.getElementById('question');
    const chatDiv = document.getElementById('chat');

    const question = questionInput.value.trim();
    if (!question) return;

    // Display user question immediately
    chatDiv.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
    questionInput.value = '';

    try {
        // Send to backend
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        // Display bot answer
        let botAnswer = "";

        if (Array.isArray(data.answer)) {
            botAnswer = data.answer.map(a =>
                `<div style="margin-bottom:8px; padding:6px; border:1px solid #ddd; border-radius:6px;">
                    <p><strong>Source:</strong> ${a.source || "N/A"}</p>
                    <p><strong>Text:</strong> ${a.text || ""}</p>
                    <p><em>Score: ${a.score ? a.score.toFixed(3) : "N/A"}</em></p>
                </div>`).join("");
        } else {
            botAnswer = data.answer.replace(/\n/g, "<br>");
        }

        chatDiv.innerHTML += `<p><strong>Bot:</strong><br>${botAnswer}</p>`;
        chatDiv.scrollTop = chatDiv.scrollHeight; // auto-scroll
    } catch (error) {
        console.error("Error:", error);
        chatDiv.innerHTML += `<p><strong>Bot:</strong> Sorry, something went wrong.</p>`;
    }
}
