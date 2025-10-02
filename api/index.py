from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_file('static/index.html')

@app.route('/generate', methods=['POST'])
def generate():
    from groq import Groq
    data = request.json
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Crypto tweet about {data['project']}. Max 280 chars."}],
        max_tokens=300
    )
    return jsonify({"content": response.choices[0].message.content})
