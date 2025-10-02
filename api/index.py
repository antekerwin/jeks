from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Data projects dari Pre-TGE Arena
PROJECTS = [
    {"name": "Sentient AI", "mindshare": "High", "category": "AI Agents"},
    {"name": "Limitless", "mindshare": "Medium", "category": "AI Tools"},
    {"name": "Polymarket", "mindshare": "Very High", "category": "Prediction Markets"},
    {"name": "Story Protocol", "mindshare": "High", "category": "IP & Licensing"},
    {"name": "Berachain", "mindshare": "Very High", "category": "Layer 1"},
    {"name": "Monad", "mindshare": "High", "category": "Layer 1"},
    {"name": "Movement Labs", "mindshare": "Medium", "category": "Layer 2"},
    {"name": "Injective", "mindshare": "High", "category": "DeFi"},
]

# Prompt templates
PROMPTS = {
    "data-driven": {
        "name": "📊 Analisis Data & Metrik",
        "description": "Konten berdasarkan data funding, TVL, pertumbuhan user"
    },
    "competitive": {
        "name": "🎯 Positioning & Kompetitor",
        "description": "Analisis competitive landscape dan unique differentiation"
    },
    "thesis": {
        "name": "💡 Forward-Looking Thesis",
        "description": "Prediksi trend, market impact, contrarian take"
    }
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
        
        # Mock response (nanti ganti ke Groq)
        content = f"🚀 {project} sedang membangun infrastruktur {PROMPTS[prompt_type]['description'].lower()}. Data menunjukkan pertumbuhan solid dengan community engagement tinggi. Ini bisa jadi game-changer di spacenya! DYOR 📊"
        
        # Mock scoring
        scoring = {
            "crypto_relevance": 8,
            "engagement_potential": 9,
            "semantic_quality": 8,
            "total": 25,
            "rating": "⭐⭐⭐⭐ Excellent",
            "feedback": [
                "✅ Project mention yang relevant",
                "✅ Engaging language",
                "✅ Call-to-action included",
                "⚠️ Could add more specific metrics"
            ]
        }
        
        return jsonify({
            "success": True,
            "content": content,
            "scoring": scoring
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
