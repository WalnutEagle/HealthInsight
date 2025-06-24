from flask import Flask, request, jsonify, render_template
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VECTOR_STORE_PATH = "faiss_index"

embeddings = OpenAIEmbeddings()
db = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0.2), 
    chain_type="stuff", 
    retriever=retriever,
    return_source_documents=True
)

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handle the question from the user and return the AI's answer."""
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        result = qa_chain({"query": question})
        answer = result.get('result')
        
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HealthInsight Bot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        #chatbox { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: scroll; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h1>HealthInsight Bot</h1>
    <p>Ask a question about the CVS Health 2023 Report.</p>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="e.g., What is the Mindful Moments program?">
    <button onclick="askBot()">Ask</button>

    <script>
        async function askBot() {
            const userInput = document.getElementById('userInput');
            const chatbox = document.getElementById('chatbox');
            const question = userInput.value;

            if (!question) return;

            chatbox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
            
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            chatbox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;
            userInput.value = '';
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
        ''')
    app.run(debug=True)
