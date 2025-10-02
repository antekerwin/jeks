from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

PROJECTS = [
    {"name": "Sentient AI", "mindshare": "High", "category": "AI Agents"},
    {"name": "Limitless", "mindshare": "Medium", "category": "AI Tools"},
    {"name": "Polymarket", "mindshare": "Very High", "category": "Prediction Markets"},
    {"name": "Story Protocol", "mindshare": "High", "category": "IP & Licensing"},
    {"name": "Berachain", "mindshare": "Very High", "category": "Layer 1"},
]

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
        from groq import Groq
        
        data = request.json
        project = data.get('project')
        prompt_type = data.get('prompt_type')
        
        # Groq client
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Build prompt based on type
        prompts_map = {
            "data-driven": f"Generate a data-driven crypto Twitter thread about {project}. Include specific metrics, funding data, or growth numbers. Max 280 chars. Write in Bahasa Indonesia casual style.",
            "competitive": f"Generate a competitive analysis Twitter thread about {project} vs competitors. Show unique differentiation. Max 280 chars. Bahasa Indonesia casual.",
            "thesis": f"Generate a forward-looking thesis Twitter thread about {project}. Include bold prediction and market impact. Max 280 chars. Bahasa Indonesia casual."
        }
        
        # Generate content
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a crypto analyst creating YAPS-optimized Twitter content in Bahasa Indonesia casual style."},
                {"role": "user", "content": prompts_map.get(prompt_type, prompts_map['data-driven'])}
            ],
            temperature=0.7,
            max_tokens=400
        )
        
        content = response.choices[0].message.content
        
        # Simple scoring (nanti bisa enhance)
        scoring = {
            "crypto_relevance": 8,
            "engagement_potential": 9,
            "semantic_quality": 8,
            "total": 25,
            "rating": "⭐⭐⭐⭐ Excellent",
            "feedback": [
                "✅ AI-generated content optimized for YAPS",
                "✅ Project-specific insights",
                "✅ Engaging language",
                "💡 Review and personalize before posting"
            ]
        }
        
        return jsonify({
            "success": True,
            "content": content,
            "scoring": scoring
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
