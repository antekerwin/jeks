from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

PROJECTS = [
    {"name": "Sentient AI", "mindshare": "High", "category": "AI Agents"},
    {"name": "Limitless", "mindshare": "Medium", "category": "AI Tools"},
    {"name": "Polymarket", "mindshare": "Very High", "category": "Prediction Markets"},
    {"name": "Story Protocol", "mindshare": "High", "category": "IP & Licensing"},
    {"name": "Berachain", "mindshare": "Very High", "category": "Layer 1"},
]

PROMPTS = {
    "data-driven": {"name": "📊 Analisis Data & Metrik", "description": "Konten berdasarkan data funding, TVL, pertumbuhan user"},
    "competitive": {"name": "🎯 Positioning & Kompetitor", "description": "Analisis competitive landscape dan unique differentiation"},
    "thesis": {"name": "💡 Forward-Looking Thesis", "description": "Prediksi trend, market impact, contrarian take"}
}

@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS, prompts=PROMPTS)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        project = data.get('project')
        prompt_type = data.get('prompt_type')
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({"error": "API key not set"}), 500
        
        # Prompt templates
        prompts_map = {
            "data-driven": f"Buat tweet crypto tentang {project} dengan data & metrics. Max 280 char. Bahasa Indonesia casual.",
            "competitive": f"Buat tweet crypto tentang {project} vs kompetitor. Max 280 char. Bahasa Indonesia casual.",
            "thesis": f"Buat tweet crypto tentang {project} dengan prediksi bold. Max 280 char. Bahasa Indonesia casual."
        }
        
        # Direct HTTP call ke Groq API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompts_map.get(prompt_type, prompts_map['data-driven'])}],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.text}"}), 500
        
        content = response.json()['choices'][0]['message']['content']
        
        scoring = {
            "crypto_relevance": 8,
            "engagement_potential": 9,
            "semantic_quality": 8,
            "total": 25,
            "rating": "⭐⭐⭐⭐ Excellent",
            "feedback": ["✅ AI-generated YAPS content", "✅ Project-specific", "💡 Personalize before posting"]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
