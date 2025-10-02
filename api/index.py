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
    {"name": "Movement Labs", "mindshare": "Medium", "category": "Layer 2"},
]

PROMPTS = {
    "data-driven": {"name": "📊 Analisis Data & Metrik", "description": "Protocol analysis dengan metrics"},
    "competitive": {"name": "🎯 Positioning & Kompetitor", "description": "Market insights dengan data backing"},
    "thesis": {"name": "💡 Forward-Looking Thesis", "description": "Technical explainers & predictions"}
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
        
        # ALGORITMA YAPS - CHECKLIST LENGKAP
        yaps_algorithm = """
📝 ALGORITMA YAPS (Kaito AI):
Formula: YAPS Points = Content Quality × Smart Followers Engagement × 75 × Tier Bonus

CHECKLIST CONTENT QUALITY:
✅ Crypto-focused (DeFi, L2, protocols, market analysis)
✅ Original insight - NO copy-paste
✅ Data-driven: Include angka, metrics, facts
✅ Educational: Jelaskan "why it matters"
✅ 150-280 characters (optimal)

TEMPLATE WINNING:
[Specific Data/Event] + [Your Analysis] + [Why It Matters] + [Question/CTA]

CONTOH:
"Base TVL hit $2.8B (+15% this week) 🔵

Key drivers:
• Coinbase institutional flows
• Lower gas vs Ethereum
• Growing DeFi ecosystem

This positions Base as the L2 for mainstream adoption.

What protocols are you watching on Base? 👇"

TARGET ENGAGEMENT (50% score):
- Smart followers: 3000+ followers, high crypto ratio
- Value-add replies: Technical insights
- Build relationships: Regular interaction
- Community focus: Help others, share knowledge

HINDARI (Penalty):
❌ Keyword stuffing
❌ Copy-paste content
❌ Low-effort tanpa context
❌ Emotional tanpa data
❌ Tag Kaito di every post
"""

        # YAPS-OPTIMIZED PROMPTS
        prompts_map = {
            "data-driven": f"""{yaps_algorithm}

PROJECT: {project}

Generate 1 tweet YAPS-optimized mengikuti template:

1. LEAD dengan specific data/metrics:
   - Funding amount, TVL, growth %, user numbers
   - Format: "[Project] [metric] [timeframe]"

2. YOUR ANALYSIS (2-3 bullet points):
   - Key drivers/reasons
   - Technical insights
   - Market positioning

3. WHY IT MATTERS:
   - Broader impact
   - Positioning dalam ecosystem
   - Trend yang dibentuk

4. QUESTION/CTA:
   - Thoughtful question untuk drive engagement
   - Invite community perspective

RULES:
- 150-280 characters WAJIB
- Include 2-3 data points konkret
- Original analysis (bukan generic)
- End dengan question
- Bahasa Indonesia casual
- Max 1 emoji atau tanpa emoji

GENERATE HANYA tweet content:""",

            "competitive": f"""{yaps_algorithm}

PROJECT: {project}

Generate 1 tweet competitive analysis YAPS-optimized:

1. MARKET CONTEXT dengan data:
   - Category overview
   - Market size/trend

2. COMPETITIVE COMPARISON:
   - {project} vs 1-2 competitors
   - Metrics objektif
   - Unique differentiation

3. WHY IT MATTERS:
   - Who wins and why
   - Market implications

4. QUESTION:
   - Community perspective invite

RULES:
- 150-280 chars
- Objektif analysis dengan data
- Personal thesis yang backed
- End dengan debate question
- Bahasa Indonesia casual

GENERATE HANYA tweet:""",

            "thesis": f"""{yaps_algorithm}

PROJECT: {project}

Generate 1 tweet forward-looking thesis YAPS-optimized:

1. TREND OBSERVATION dengan data:
   - What's shifting in market
   - Specific metrics/signals

2. PROJECT POSITIONING:
   - {project} dalam trend ini
   - Unique advantage

3. BOLD THESIS:
   - Prediction dengan backing
   - 2-3 supporting reasons
   - Risk consideration (balanced)

4. QUESTION:
   - Debate-worthy question

RULES:
- 150-280 chars
- Contrarian OK jika data-backed
- Show original thinking
- Technical depth
- Bahasa Indonesia casual

GENERATE HANYA tweet:"""
        }
        
        # API Call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a crypto analyst expert yang mengikuti YAPS algorithm (Kaito AI) untuk maximize points. Selalu ikuti template: [Data/Event] + [Analysis] + [Why Matters] + [Question]."},
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
        
        # YAPS SCORING (Simulate algorithm)
        char_count = len(content)
        optimal_length = 150 <= char_count <= 280
        has_data = any(char.isdigit() for char in content)  # Check for numbers/data
        has_question = '?' in content
        
        # Content Quality Score (0-10)
        content_quality = 8
        if optimal_length: content_quality += 1
        if has_data: content_quality += 1
        
        # Smart Followers Engagement (assume 0.5-0.9)
        engagement_factor = 0.7
        
        # Calculate YAPS Points (simplified)
        # Real: Quality × Engagement × 75 × Tier
        estimated_yaps = int(content_quality * engagement_factor * 75)
        
        scoring = {
            "crypto_relevance": content_quality,
            "engagement_potential": 9 if has_question else 7,
            "semantic_quality": 9 if (has_data and optimal_length) else 7,
            "total": content_quality + (9 if has_question else 7) + (9 if has_data else 7),
            "rating": "⭐⭐⭐⭐⭐ YAPS Algorithm Applied" if optimal_length and has_data else "⭐⭐⭐⭐ Good",
            "feedback": [
                f"✅ Length: {char_count} chars" + (" (optimal)" if optimal_length else " ⚠️ adjust to 150-280"),
                f"✅ Data-driven: {'Yes' if has_data else 'Add metrics'}",
                f"✅ Engagement hook: {'Yes' if has_question else 'Add question'}",
                f"📊 Estimated YAPS: ~{estimated_yaps} points",
                "💡 Template applied: [Data] + [Analysis] + [Why Matters] + [Question]"
            ]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
