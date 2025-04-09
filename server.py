from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

KNOWLEDGE_FILE = "database.md"
global_prompt = "You are a helpful assistant of all knowledge about Cebu International School. Your job is to answer the user questions as best as you can, based on the following information. Do not think or look for any online sources. Use only the information you are given. Find the most suitable information from below to construct your answer.\n\n"

def load_knowledge():
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read() + "\n\n"
    except Exception as e:
        return f"failed to load knowledge: {str(e)}\n\n"

global_knowledge = load_knowledge()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    full_prompt = global_prompt + global_knowledge + "\nUSER: " + user_message + "\nASSISSTANT: "
    payload = {
        "prompt": full_prompt,
        "n_predict": 1024,
        "temperature": 0.7
    }
    response = requests.post("http://localhost:8080/completion", json=payload)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000)