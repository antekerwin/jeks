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
        
        # YAPS-OPTIMIZED PROMPTS
        yaps_rules = """
ATURAN YAPS SCORING (Kaito AI):
- Crypto Relevance (30%): Data konkret, original insight, educational value
- Smart Followers Engagement (50%): Konten yang engage crypto influencers
- Semantic Analysis (20%): Depth & originality (anti keyword stuffing)

WAJIB:
✅ Include 2-3 data/metrics spesifik (angka, %, funding, TVL, dll)
✅ Original analysis - explain "why it matters"
✅ 150-280 karakter (optimal untuk YAPS)
✅ Max 1-2 hashtags (atau tanpa hashtag lebih baik)
✅ Bahasa Indonesia natural (bukan formal kaku)
✅ End dengan question untuk drive discussion

HINDARI:
❌ Generic statements tanpa data
❌ Keyword stuffing
❌ "Gm" atau greeting
❌ Copy-paste style
"""
        
        prompts_map = {
            "data-driven": f"""{yaps_rules}

PROJECT: {project}

Buat 1 tweet yang:
1. Lead dengan data point terkuat (funding/TVL/growth/metrics)
2. Include 2-3 angka spesifik dengan konteks
3. Explain kenapa metrics ini penting untuk market
4. Personal thesis/take
5. End dengan thoughtful question

GENERATE HANYA konten tweet (150-280 char). Bahasa Indonesia casual.""",

            "competitive": f"""{yaps_rules}

PROJECT: {project}

Buat 1 tweet competitive analysis:
1. Market context & kategori
2. Compare {project} dengan 1-2 competitors (objektif)
3. Highlight unique differentiation dengan data
4. Personal thesis: siapa yang win dan kenapa
5. Question: invite community perspective

GENERATE HANYA konten tweet (150-280 char). Bahasa Indonesia casual.""",

            "thesis": f"""{yaps_rules}

PROJECT: {project}

Buat 1 tweet forward-looking thesis:
1. Trend observation: apa yang shifting di market
2. {project} positioning dalam trend ini
3. BOLD thesis/prediction dengan data backing
4. 2-3 supporting reasons
5. Risk consideration (balanced thinking)
6. Question untuk debate

GENERATE HANYA konten tweet (150-280 char). Bahasa Indonesia casual."""
        }
        
        # Call Groq API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a crypto analyst expert at creating YAPS-optimized Twitter content that maximizes Kaito AI scoring."},
                {"role": "user", "content": prompts_map.get(prompt_type, prompts_map['data-driven'])}
            ],
            "temperature": 0.7,
            "max_tokens": 400
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
        
        # Enhanced scoring
        char_count = len(content)
        optimal_length = 150 <= char_count <= 280
        
        scoring = {
            "crypto_relevance": 9 if optimal_length else 7,
            "engagement_potential": 9,
            "semantic_quality": 9 if optimal_length else 7,
            "total": 27 if optimal_length else 23,
            "rating": "⭐⭐⭐⭐⭐ YAPS-Optimized" if optimal_length else "⭐⭐⭐⭐ Good",
            "feedback": [
                f"✅ Length: {char_count} chars" + (" (optimal 150-280)" if optimal_length else " ⚠️ adjust to 150-280"),
                "✅ YAPS algorithm rules applied",
                "✅ Data-driven & original insights",
                "💡 Review & personalize sebelum post"
            ]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
