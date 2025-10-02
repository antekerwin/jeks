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
    {"name": "Monad", "mindshare": "High", "category": "Layer 1"},
]

PROMPTS = {
    "data-driven": {"name": "📊 Data & Metrics", "description": "Lead dengan data konkret, metrics, growth numbers"},
    "competitive": {"name": "🎯 Competitive Edge", "description": "Compare dengan kompetitor, highlight unique value"},
    "thesis": {"name": "💡 Bold Prediction", "description": "Forward-looking take, trend analysis, market impact"},
    "custom": {"name": "✏️ Custom Request", "description": "Tulis request konten Anda sendiri"}
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
        custom_request = data.get('custom_request', '')
        
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({"error": "API key not set"}), 500
        
        # YAPS Algorithm Base
        yaps_rules = """
YAPS ALGORITHM (Kaito AI):
✅ 150-280 characters optimal
✅ Include data/metrics (angka konkret)
✅ Original insight & analysis
✅ Educational value (explain why it matters)
✅ End dengan question untuk engagement
✅ Bahasa Indonesia casual, natural
❌ NO keyword stuffing, NO copy-paste style

Template: [Data/Event] + [Analysis] + [Why Matters] + [Question]
"""

        # Build prompt based on type
        if prompt_type == "custom" and custom_request:
            # Custom mode - user bebas request
            user_prompt = f"""{yaps_rules}

PROJECT: {project}

USER REQUEST: {custom_request}

Generate tweet YAPS-optimized sesuai request. Follow YAPS rules:
- 150-280 chars
- Include data/metrics
- Original analysis
- End dengan question
- Bahasa Indonesia casual

GENERATE tweet:"""
        else:
            # Preset prompts
            prompts_map = {
                "data-driven": f"""{yaps_rules}

PROJECT: {project}

Generate tweet dengan:
1. Lead: Specific data/metric (funding, TVL, growth %, users)
2. Analysis: 2-3 key insights kenapa data ini penting
3. Why Matters: Impact ke market/ecosystem
4. Question: Drive discussion

Bahasa Indonesia casual. 150-280 chars.

GENERATE tweet:""",

                "competitive": f"""{yaps_rules}

PROJECT: {project}

Generate tweet competitive analysis:
1. Market context dengan data
2. {project} vs competitors (objektif)
3. Unique differentiation/edge
4. Personal take: who wins & why
5. Question untuk community

Bahasa Indonesia casual. 150-280 chars.

GENERATE tweet:""",

                "thesis": f"""{yaps_rules}

PROJECT: {project}

Generate tweet bold thesis:
1. Trend observation (data-backed)
2. {project} positioning dalam trend
3. Prediction/contrarian take
4. Supporting reasons
5. Question untuk debate

Bahasa Indonesia casual. 150-280 chars.

GENERATE tweet:"""
            }
            user_prompt = prompts_map.get(prompt_type, prompts_map['data-driven'])
        
        # API Call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a crypto analyst expert. Always follow YAPS algorithm: [Data] + [Analysis] + [Why Matters] + [Question]. Output ONLY the tweet content."},
                {"role": "user", "content": user_prompt}
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
        
        # YAPS Scoring
        char_count = len(content)
        optimal_length = 150 <= char_count <= 280
        has_data = any(char.isdigit() for char in content)
        has_question = '?' in content
        
        quality = 7
        if optimal_length: quality += 1
        if has_data: quality += 1
        if has_question: quality += 1
        
        estimated_yaps = int(quality * 0.7 * 75)
        
        scoring = {
            "crypto_relevance": quality,
            "engagement_potential": 9 if has_question else 7,
            "semantic_quality": 9 if (has_data and optimal_length) else 7,
            "total": quality + (9 if has_question else 7) + (9 if has_data else 7),
            "rating": f"⭐⭐⭐⭐{'⭐' if quality >= 9 else ''} Quality: {quality}/10",
            "feedback": [
                f"📏 Length: {char_count} chars" + (" ✅" if optimal_length else " ⚠️ optimize to 150-280"),
                f"📊 Data/Metrics: {'✅ Yes' if has_data else '⚠️ Add numbers'}",
                f"💬 Engagement: {'✅ Question included' if has_question else '⚠️ Add question'}",
                f"🎯 Est. YAPS: ~{estimated_yaps} points",
                "✨ YAPS algorithm applied"
            ]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
