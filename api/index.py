from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    project = data.get('project', 'Example Project')
    
    # Mock response dulu (nanti ganti pakai Groq)
    mock_content = f"🚀 {project} is revolutionizing crypto with innovative technology. Early signals show strong community engagement and technical fundamentals. This could be a game-changer in the space. DYOR! 📊"
    
    return jsonify({
        'success': True,
        'content': mock_content
    })

if __name__ == '__main__':
    app.run(debug=True)
