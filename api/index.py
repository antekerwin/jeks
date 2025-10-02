from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "status": "success",
        "groq_key": bool(os.getenv("GROQ_API_KEY"))
    })

@app.route('/generate', methods=['POST'])
def generate():
    try:
        from groq import Groq
        
        data = request.json
        project = data.get('project', 'Bitcoin')
        style = data.get('style', 'data-driven')
        
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        prompt = f"Generate a high-quality crypto Twitter content about {project} using {style} analysis style. Max 280 characters. Include relevant data/metrics."
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        
        return jsonify({
            "success": True,
            "content": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
