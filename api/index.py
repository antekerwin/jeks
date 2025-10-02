from flask import Flask, render_template, request, jsonify
import os
import requests
import re
import random

app = Flask(__name__)

def fetch_kaito_projects():
    """Fetch top 20 projects dari Kaito Pre-TGE realtime"""
    try:
        response = requests.get("https://yaps.kaito.ai/pre-tge", timeout=10)
        if response.status_code != 200:
            return get_fallback_projects()
        
        html = response.text
        
        # Parse projects dari HTML
        projects = []
        
        # Pattern untuk extract project names & mindshare
        pattern = r'(MOMENTUM|LIMITLESS|POLYMARKET|SENTIENT|MONAD|OPENSEA|BASE|ALLORA|YIELDBASIS|CYSIC|BILLIONS|MET|WALLCHAIN|IRYS|RECALL|KITE|MASK|EVERLYN|DZ|TALUS|BERACHAIN|STORY)'
        matches = re.findall(pattern, html)
        
        # Deduplicate & get unique top 20
        seen = set()
        for match in matches:
            if match not in seen and len(projects) < 20:
                projects.append({
                    "name": match.title() if match != "MASK" else "MetaMask",
                    "mindshare": "High",
                    "category": get_category(match)
                })
                seen.add(match)
        
        return projects if projects else get_fallback_projects()
        
    except:
        return get_fallback_projects()

def get_fallback_projects():
    """Fallback jika fetch gagal"""
    return [
        {"name": "Limitless", "mindshare": "High", "category": "AI Tools"},
        {"name": "Polymarket", "mindshare": "Very High", "category": "Prediction Markets"},
        {"name": "Sentient", "mindshare": "High", "category": "AI Agents"},
        {"name": "Monad", "mindshare": "High", "category": "Layer 1"},
        {"name": "Base", "mindshare": "Very High", "category": "Layer 2"},
    ]

def get_category(project):
    """Get category untuk project"""
    categories = {
        "LIMITLESS": "AI Tools", "SENTIENT": "AI Agents", "POLYMARKET": "Prediction Markets",
        "MONAD": "Layer 1", "BASE": "Layer 2", "OPENSEA": "NFT Marketplace",
        "ALLORA": "AI Infrastructure", "YIELDBASIS": "DeFi", "CYSIC": "ZK Infra",
        "BILLIONS": "AI Agents", "MET": "Metaverse", "WALLCHAIN": "DeFi",
        "IRYS": "Data Storage", "RECALL": "AI Memory", "KITE": "DeFi",
        "MASK": "Wallet", "EVERLYN": "AI Agents", "DZ": "Gaming", "TALUS": "AI",
        "BERACHAIN": "Layer 1", "STORY": "IP Protocol", "MOMENTUM": "DeFi"
    }
    return categories.get(project, "DeFi")

PROMPTS = {
    "data-driven": {"name": "📊 Data & Metrics", "description": "Lead dengan data konkret, metrics, growth"},
    "competitive": {"name": "🎯 Competitive Edge", "description": "Compare kompetitor, unique value"},
    "thesis": {"name": "💡 Bold Prediction", "description": "Trend analysis, market impact"},
    "custom": {"name": "✏️ Custom Request", "description": "Request konten bebas"}
}

@app.route('/')
def home():
    projects = fetch_kaito_projects()
    return render_template('index.html', projects=projects, prompts=PROMPTS)

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
        
        # YAPS Algorithm
        yaps_base = """
YAPS ALGORITHM (Kaito AI):
✅ 150-280 chars optimal
✅ Data/metrics konkret
✅ Original insight
✅ Educational (why it matters)
✅ End dengan question
✅ Bahasa Indonesia natural
❌ NO keyword stuffing

Template: [Data] + [Analysis] + [Why Matters] + [Question]
"""
        
        # VARIASI PROMPT - Random style untuk konten berbeda
        styles = [
            "gaya casual trader yang suka data",
            "gaya analyst professional tapi approachable",
            "gaya community-focused yang suka diskusi",
            "gaya contrarian yang berani beda pendapat",
            "gaya technical deep-dive tapi mudah dipahami"
        ]
        
        chosen_style = random.choice(styles)
        
        if prompt_type == "custom" and custom_request:
            user_prompt = f"""{yaps_base}

PROJECT: {project}
STYLE: {chosen_style}
REQUEST: {custom_request}

Generate tweet YAPS-optimized dengan style di atas. Variasikan approach & tone. 150-280 chars. Bahasa Indonesia.

GENERATE tweet:"""
        else:
            prompts_map = {
                "data-driven": f"""{yaps_base}

PROJECT: {project}
STYLE: {chosen_style}

Generate 1 tweet data-driven:
1. Lead: Data spesifik (funding/TVL/growth)
2. Analysis: Insight original
3. Why Matters: Impact
4. Question: Engage community

VARIASI: Gunakan {chosen_style}. Jangan template kaku.

150-280 chars. Bahasa Indonesia.

GENERATE tweet:""",

                "competitive": f"""{yaps_base}

PROJECT: {project}
STYLE: {chosen_style}

Generate competitive analysis:
1. Market context + data
2. Compare objektif vs competitors
3. Unique edge {project}
4. Personal take
5. Question

VARIASI: {chosen_style}. Fresh perspective.

150-280 chars. Bahasa Indonesia.

GENERATE tweet:""",

                "thesis": f"""{yaps_base}

PROJECT: {project}
STYLE: {chosen_style}

Generate bold thesis:
1. Trend observation (data)
2. {project} positioning
3. Prediction/contrarian
4. Reasoning
5. Question

VARIASI: {chosen_style}. Be creative & original.

150-280 chars. Bahasa Indonesia.

GENERATE tweet:"""
            }
            user_prompt = prompts_map.get(prompt_type, prompts_map['data-driven'])
        
        # API Call - VARIASI TEMPERATURE untuk hasil beda
        temp = random.uniform(0.7, 0.95)  # Random temperature
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": f"You are a crypto analyst with style: {chosen_style}. Always follow YAPS algorithm but be creative & varied. Output ONLY tweet."},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temp,
            "max_tokens": 400,
            "top_p": 0.9
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
        
        # Scoring
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
                f"📏 {char_count} chars" + (" ✅" if optimal_length else " ⚠️ 150-280"),
                f"📊 Data: {'✅' if has_data else '⚠️ add metrics'}",
                f"💬 Engage: {'✅' if has_question else '⚠️ add question'}",
                f"🎯 Est. YAPS: ~{estimated_yaps} pts",
                f"🎨 Style: {chosen_style}"
            ]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
