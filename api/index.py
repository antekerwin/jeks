from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "success",
        "message": "YAPS Generator API is running!",
        "groq_key_exists": bool(os.getenv("GROQ_API_KEY"))
    })

@app.route('/test')
def test():
    try:
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return jsonify({"error": "GROQ_API_KEY not set"}), 500
        
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=50
        )
        
        return jsonify({
            "status": "success",
            "response": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    from flask import request
    from groq import Groq
    
    data = request.json
    project = data.get('project', 'Bitcoin')
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Write a crypto tweet about {project}. Max 280 chars."}],
        max_tokens=300
    )
    
    return jsonify({"content": response.choices[0].message.content})
