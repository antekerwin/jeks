from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Initialize Groq client (FREE)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY belum diset")

client = Groq(api_key=api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    project = data.get('project', 'Crypto project')
    style = data.get('style', 'data-driven')
    
    # Groq prompt
    prompt = f"Generate a high-quality crypto Twitter thread about {project} using {style} style. Max 280 chars."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # FREE model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return jsonify({"content": response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)
