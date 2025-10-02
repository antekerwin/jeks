from flask import Flask, render_template, request, jsonify
import os
import requests
import re
import random

app = Flask(__name__)

def fetch_kaito_projects():
    try:
        response = requests.get("https://yaps.kaito.ai/pre-tge", timeout=10)
        if response.status_code != 200:
            return get_fallback_projects()
        html = response.text
        pattern = r'(MOMENTUM|LIMITLESS|POLYMARKET|SENTIENT|MONAD|OPENSEA|BASE|ALLORA|YIELDBASIS|CYSIC|BILLIONS|MET|WALLCHAIN|IRYS|RECALL|KITE|MASK|EVERLYN|DZ|TALUS|BERACHAIN|STORY)'
        matches = re.findall(pattern, html)
        seen = set()
        projects = []
        for match in matches:
            if match not in seen and len(projects) < 20:
                projects.append({"name": match.title() if match != "MASK" else "MetaMask", "mindshare": "High", "category": get_category(match)})
                seen.add(match)
        return projects if projects else get_fallback_projects()
    except:
        return get_fallback_projects()

def get_fallback_projects():
    return [
        {"name": "Limitless", "mindshare": "High", "category": "AI Tools"},
        {"name": "Polymarket", "mindshare": "Very High", "category": "Prediction Markets"},
        {"name": "Sentient", "mindshare": "High", "category": "AI Agents"},
    ]

def get_category(project):
    categories = {
        "LIMITLESS": "AI Tools", "SENTIENT": "AI Agents", "POLYMARKET": "Prediction Markets",
        "MONAD": "Layer 1", "BASE": "Layer 2", "OPENSEA": "NFT Marketplace",
        "EVERLYN": "AI Assistant", "MET": "DeFi", "MOMENTUM": "DeFi"
    }
    return categories.get(project, "DeFi")

PROMPTS = {
    "data-driven": {"name": "📊 Data & Metrics", "description": "Lead dengan data konkret"},
    "competitive": {"name": "🎯 Competitive Edge", "description": "Compare kompetitor"},
    "thesis": {"name": "💡 Bold Prediction", "description": "Trend analysis"},
    "custom": {"name": "✏️ Custom Request", "description": "Request bebas"}
}

@app.route('/')
def home():
    projects = fetch_kaito_projects()
    return render_template('index.html', projects=projects, prompts=PROMPTS)

def translate_to_indonesian(text, api_key):
    """Force translate ke bahasa Indonesia jika masih Inggris"""
    # Check if already Indonesian
    indonesian_words = ['yang', 'dengan', 'ini', 'untuk', 'dari', 'adalah', 'pada', 'dalam', 'akan', 'menurut', 'kalian', 'kenapa', 'bagaimana', 'naik', 'turun']
    if any(word in text.lower() for word in indonesian_words):
        return text
    
    # Translate using OpenRouter
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jeks-delta.vercel.app",
        "X-Title": "YAPS Translator"
    }
    
    payload = {
        "model": "x-ai/grok-2-1212",
        "messages": [
            {"role": "system", "content": "Translate to natural Indonesian. Keep crypto terms. No explanation, just translation."},
            {"role": "user", "content": f"Translate to Indonesian:\n\n{text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=20
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
    except:
        pass
    
    return text

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        project = data.get('project')
        prompt_type = data.get('prompt_type')
        custom_request = data.get('custom_request', '')
        
        api_key = "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"
        
        # ULTRA STRONG INDONESIAN PROMPT
        system_prompt = """Kamu HARUS menulis HANYA dalam bahasa Indonesia.

Contoh yang BENAR:
"LIMITLESS dominasi AI Agents. Funding naik 340% Q4 2024, TVL $120M. Prediksi: bisa grab 15% mindshare dalam 6 bulan. Menurut kalian, siapa kompetitor terdekat?"

Contoh yang SALAH (jangan ikuti):
"LIMITLESS dominates AI Agents. Funding up 340% Q4 2024."

Gunakan kata Indonesia: dominasi, naik, turun, dengan, untuk, menurut kalian, siapa, kenapa, bagaimana."""

        category = get_category(project.upper())
        
        if prompt_type == "custom" and custom_request:
            user_prompt = f"""Project: {project} ({category})

Request: {custom_request}

Tulis tweet bahasa Indonesia untuk YAPS (150-280 char, data/metrics, ada pertanyaan).

Contoh format:
"{project} [analisis] dengan [data]. [Metric] naik [%]. Prediksi: [thesis]. Menurut kalian [question]?"

Tulis HANYA tweet Indonesia:"""
        else:
            user_prompt = f"""Project: {project} ({category})

Tulis tweet bahasa Indonesia untuk YAPS (150-280 char, data/metrics, ada pertanyaan).

Contoh format:
"{project} [analisis] dengan [data]. [Metric] naik [%]. Prediksi: [thesis]. Menurut kalian [question]?"

Tulis HANYA tweet Indonesia:"""
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://jeks-delta.vercel.app",
            "X-Title": "YAPS Generator"
        }
        
        payload = {
            "model": "x-ai/grok-2-1212",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.75,
            "max_tokens": 300
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({"error": f"API error: {response.status_code}"}), 500
        
        content = response.json()['choices'][0]['message']['content'].strip()
        
        # FORCE TRANSLATION jika masih Inggris
        content = translate_to_indonesian(content, api_key)
        
        # Remove hashtags (YAPS rule: max 1-2 tags atau tanpa tag lebih baik)
        content = re.sub(r'#\w+\s*', '', content).strip()
        
        # SCORING
        char_count = len(content)
        optimal_length = 150 <= char_count <= 280
        has_data = any(char.isdigit() for char in content)
        has_question = '?' in content
        is_indonesian = any(word in content.lower() for word in ['yang', 'dengan', 'untuk', 'menurut', 'kalian', 'naik', 'turun'])
        quality = 7 + (1 if optimal_length else 0) + (1 if has_data else 0) + (1 if has_question else 0) + (1 if is_indonesian else 0)
        
        scoring = {
            "crypto_relevance": quality,
            "engagement_potential": 9 if has_question else 7,
            "semantic_quality": 9 if (has_data and optimal_length) else 7,
            "total": quality + (9 if has_question else 7) + (9 if has_data else 7),
            "rating": f"⭐⭐⭐⭐{'⭐' if quality >= 9 else ''} Quality: {quality}/10",
            "feedback": [
                f"📏 {char_count} chars" + (" ✅" if optimal_length else " ⚠️"),
                f"📊 Data: {'✅' if has_data else '⚠️'}",
                f"💬 Engage: {'✅' if has_question else '⚠️'}",
                f"🇮🇩 Bahasa: {'✅ Indonesia' if is_indonesian else '⚠️ Inggris'}",
                f"🎯 Est. YAPS: ~{int(quality*0.7*75)} pts",
                f"🤖 Model: Grok 2 AI"
            ]
        }
        
        return jsonify({"success": True, "content": content, "scoring": scoring})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_content():
    """Analyze user's content berdasarkan Kaito YAPS algorithm"""
    try:
        data = request.json
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({"error": "Content required"}), 400
        
        char_count = len(content)
        optimal_length = 150 <= char_count <= 280
        min_length = char_count >= 50
        
        crypto_keywords = ['defi', 'layer', 'l2', 'ai', 'rwa', 'tvl', 'airdrop', 'protocol', 'chain', 'token', 'nft', 'dao', 'staking', 'yield', 'bridge', 'zk', 'rollup', 'evm', 'smart contract']
        content_lower = content.lower()
        keyword_count = sum(1 for kw in crypto_keywords if kw in content_lower)
        has_crypto_focus = keyword_count >= 1
        
        keyword_stuffing = keyword_count > 5
        
        generic_phrases = ['to the moon', 'lfg', 'gm', 'ser', 'ngmi', 'wagmi', 'bullish', 'bearish']
        generic_count = sum(1 for phrase in generic_phrases if phrase in content_lower)
        is_original = generic_count < 2
        
        content_opt_score = 0
        if min_length: content_opt_score += 2
        if optimal_length: content_opt_score += 3
        if has_crypto_focus: content_opt_score += 3
        if is_original: content_opt_score += 2
        content_opt_score = min(10, content_opt_score)
        
        has_question = '?' in content
        has_data = any(char.isdigit() for char in content)
        has_cta = any(word in content_lower for word in ['what', 'how', 'why', 'thoughts', 'think', 'opinion', 'menurut', 'kalian', 'kenapa', 'bagaimana'])
        
        engagement_score = 0
        if has_question: engagement_score += 4
        if has_data: engagement_score += 3
        if has_cta: engagement_score += 3
        engagement_score = min(10, engagement_score)
        
        has_metrics = bool(re.search(r'\d+[%$MBK]|\$\d+|\d+x', content))
        has_analysis = len(content.split()) > 15
        no_spam_pattern = not bool(re.search(r'(.)\1{3,}', content))
        
        quality_score = 0
        if has_metrics: quality_score += 4
        if has_analysis: quality_score += 3
        if no_spam_pattern: quality_score += 3
        quality_score = min(10, quality_score)
        
        content_types = []
        if 'tvl' in content_lower or 'revenue' in content_lower: content_types.append("Protocol analysis ✅")
        if has_metrics and ('vs' in content_lower or 'compare' in content_lower): content_types.append("Comparison ✅")
        if 'airdrop' in content_lower and 'risk' in content_lower: content_types.append("Airdrop strategy ✅")
        
        penalties = []
        if keyword_stuffing: penalties.append("⚠️ Keyword stuffing")
        if content.count('#') > 2: penalties.append("⚠️ Terlalu banyak hashtags (max 1-2)")
        if generic_count >= 3: penalties.append("⚠️ Too many generic phrases")
        if char_count < 50: penalties.append("⚠️ Too short (min 50 chars)")
        
        suggestions = []
        if not has_question: suggestions.append("💡 Add question untuk drive discussion")
        if not has_data: suggestions.append("💡 Include metrics/data")
        if char_count < 150: suggestions.append("💡 Expand to 150-280 chars")
        if content.count('#') > 2: suggestions.append("💡 Kurangi hashtags (max 1-2 atau tanpa tag)")
        
        total_score = (content_opt_score * 0.3) + (engagement_score * 0.5) + (quality_score * 0.2)
        total_score = round(total_score, 1)
        estimated_yaps = int(total_score * 0.7 * 75)
        
        if total_score >= 9:
            rating = "⭐⭐⭐⭐⭐ Excellent"
        elif total_score >= 7:
            rating = "⭐⭐⭐⭐ Good"
        elif total_score >= 5:
            rating = "⭐⭐⭐ Fair"
        else:
            rating = "⭐⭐ Poor"
        
        return jsonify({
            "success": True,
            "analysis": {
                "content_optimization": {"score": content_opt_score, "weight": "30%"},
                "engagement_strategy": {"score": engagement_score, "weight": "50%"},
                "content_quality": {"score": quality_score, "weight": "20%"},
                "content_types": content_types if content_types else ["ℹ️ Standard tweet"],
                "penalties": penalties if penalties else ["✅ No penalties"],
                "suggestions": suggestions if suggestions else ["✅ Well-optimized!"],
                "total_score": total_score,
                "estimated_yaps": estimated_yaps,
                "rating": rating
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
