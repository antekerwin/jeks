from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return "Error: GROQ_API_KEY belum diset di Vercel", 500
        return render_template('index.html')
    except ImportError:
        return "Error: Groq library not installed", 500

@app.route('/generate', methods=['POST'])
def generate():
    from groq import Groq
    
    data = request.json
    project = data.get('project', 'Crypto project')
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Generate crypto Twitter content about {project}. Max 280 chars."}],
        temperature=0.7,
        max_tokens=300
    )
    
    return jsonify({"content": response.choices[0].message.content})
