from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        from groq import Groq
        
        data = request.json
        project = data.get('project', '')
        style = data.get('style', 'data-driven')
        
        if not project:
            return jsonify({'error': 'Project name required'}), 400
        
        # Groq client
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured'}), 500
            
        client = Groq(api_key=api_key)
        
        # Generate content
        prompt = f"Generate a high-quality crypto Twitter content about {project} using {style} analysis style. Focus on data, metrics, and insights. Maximum 280 characters."
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a crypto analyst creating YAPS-optimized Twitter content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        content = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'content': content
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
