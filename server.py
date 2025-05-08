from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

KNOWLEDGE_FILE = "database.md"

# 初始化Gemini客户端
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

# 加载知识库文件
def load_knowledge():
    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"failed to load knowledge: {str(e)}"

# 上传知识库文件到Gemini
def get_knowledge_file():
    return client.files.upload(file=KNOWLEDGE_FILE)

# 预先上传知识库文件
knowledge_file = None
try:
    knowledge_file = get_knowledge_file()
except Exception as e:
    print(f"Failed to upload knowledge file: {str(e)}")

model = "gemini-2.5-flash-preview-04-17"

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global knowledge_file
    user_message = request.json.get("message", "")
    
    if not knowledge_file:
        try:
            knowledge_file = get_knowledge_file()
        except Exception as e:
            return jsonify({"response": f"Error loading knowledge base: {str(e)}"})
    
    # 准备Gemini请求内容
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=knowledge_file.uri,
                    mime_type=knowledge_file.mime_type,
                ),
                types.Part.from_text(text="""You are a helpful assistant who has full knowledge of all aspects of Cebu International School(CIS). All necessary knowledge is included in the markdown file provided, and it is your only reference to structure your answers. A link to the page of the school's official website is included before the information it has. You need to give a brief but detailed response to your customer's questions, including relevant links as included in the knowledge base with brief explanation on why the link is relevant. If the customer's questions are ambiguous, you need to include all possibilities. The link to the page where you got information from needs also to be included after your response. All links should be interactable. You should not respond to questions that is irrelevant to CIS, you should answer \"Sorry, I'm unable to respond\" instead."""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_message),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=0,
        ),
        response_mime_type="text/plain",
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8042, debug=True)