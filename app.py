#!/usr/bin/env python3
"""
YAPS Content Generator - AI-powered content generator untuk maximize YAPS points
Bahasa Indonesia - Powered by Grok AI
"""

from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

PROJECTS = [
    {"name": "LIMITLESS", "mindshare": "7.00%", "category": "AI Agents"},
    {"name": "POLYMARKET", "mindshare": "6.41%", "category": "Prediction Markets"},
    {"name": "SENTIENT", "mindshare": "6.19%", "category": "AI x DeFi"},
    {"name": "MONAD", "mindshare": "4.46%", "category": "Layer 1"},
    {"name": "YIELDBASIS", "mindshare": "3.99%", "category": "DeFi Yield"},
    {"name": "ALLORA", "mindshare": "3.95%", "category": "AI Network"},
    {"name": "BASE", "mindshare": "3.93%", "category": "Layer 2"},
    {"name": "OPENSEA", "mindshare": "3.74%", "category": "NFT Marketplace"},
    {"name": "WALLCHAIN", "mindshare": "2.03%", "category": "Wallet Infrastructure"},
    {"name": "EVERLYN", "mindshare": "2.00%", "category": "AI Assistant"},
    {"name": "RECALL", "mindshare": "1.90%", "category": "Memory Layer"},
    {"name": "KITE", "mindshare": "1.78%", "category": "Trading"},
    {"name": "MOMENTUM", "mindshare": "7.32%", "category": "DeFi Protocol"},
]

PROMPT_TEMPLATES = {
    "data_driven": {
        "name": "📊 Analisis Data & Metrik",
        "description": "Konten berdasarkan data funding, TVL, pertumbuhan user",
        "system": """PENTING: Semua output WAJIB 100% BAHASA INDONESIA.

Anda adalah crypto analyst yang ahli membuat konten Twitter data-driven untuk YAPS.

ATURAN YAPS:
- Crypto Relevance (30%): Data konkret, metrics, original insight
- Smart Followers Engagement (50%): Konten yang engage influencers
- Semantic Analysis (20%): LLM evaluate depth & originality

STRUKTUR:
1. Hook dengan data point terkuat
2. 2-3 metric spesifik dengan konteks
3. Analisis kenapa metrics ini penting
4. Thesis/prediction
5. Question untuk drive discussion

HINDARI:
- Keyword stuffing
- Lebih dari 2 tags
- Generic statements
- Copy-paste news
- BAHASA INGGRIS (WAJIB INDONESIA!)

BAHASA: Indonesia (natural, tidak kaku)
LENGTH: 150-280 karakter optimal"""
    },
    
    "competitive": {
        "name": "🎯 Positioning & Kompetitor",
        "description": "Analisis competitive landscape dan unique differentiation",
        "system": """PENTING: Semua output WAJIB 100% BAHASA INDONESIA.

Anda adalah crypto strategist yang ahli analisis kompetitif untuk YAPS.

ATURAN YAPS:
- Crypto Relevance (30%): Market structure understanding
- Smart Followers Engagement (50%): Thought leadership
- Semantic Analysis (20%): Original positioning analysis

STRUKTUR:
1. Market context & kategori
2. Competitive map (2-3 competitors)
3. Unique differentiation project ini
4. Thesis siapa yang menang dan kenapa
5. Question untuk community perspective

HINDARI:
- Shilling tanpa objektif
- Excessive tags
- Surface-level comparison
- BAHASA INGGRIS (WAJIB INDONESIA!)

BAHASA: Indonesia (professional tapi approachable)
LENGTH: 150-280 karakter optimal"""
    },
    
    "thesis": {
        "name": "💡 Forward-Looking Thesis",
        "description": "Prediksi trend, market impact, contrarian take",
        "system": """PENTING: Semua output WAJIB 100% BAHASA INDONESIA.

Anda adalah crypto thought leader yang ahli membuat thesis & prediction untuk YAPS.

ATURAN YAPS:
- Crypto Relevance (30%): Trend understanding
- Smart Followers Engagement (50%): Provocative but backed thesis
- Semantic Analysis (20%): Original thinking, contrarian OK

STRUKTUR:
1. Trend observation (apa yang shifting)
2. Positioning project dalam trend ini
3. Clear thesis/prediction (bold OK)
4. 2-3 supporting reasoning
5. Risk/consideration (show balanced thinking)
6. Question untuk invite debate

HINDARI:
- Opinion tanpa backing
- Emotional statements
- Hype without substance
- BAHASA INGGRIS (WAJIB INDONESIA!)

BAHASA: Indonesia (confident, analytical)
LENGTH: 150-280 karakter optimal"""
    }
}

@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS, prompts=PROMPT_TEMPLATES)

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        project_name = data.get('project')
        prompt_type = data.get('prompt_type')
        
        project = next((p for p in PROJECTS if p['name'] == project_name), None)
        if not project:
            return jsonify({'error': 'Project tidak ditemukan'}), 400
        
        if prompt_type not in PROMPT_TEMPLATES:
            return jsonify({'error': 'Prompt type tidak valid'}), 400
        
        # GROK AI VIA OPENROUTER
        api_key = "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"
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        prompt_template = PROMPT_TEMPLATES[prompt_type]
        
        user_message = f"""Generate konten Twitter untuk project: {project_name}

Category: {project['category']}
Current Mindshare: {project['mindshare']}

WAJIB BAHASA INDONESIA 100%!

Buat 1 tweet berkualitas tinggi yang:
1. Optimized untuk YAPS scoring (Crypto Relevance 30% + Smart Engagement 50% + Semantic 20%)
2. Include data/metrics spesifik (bisa estimated berdasarkan mindshare dan category)
3. Original analysis, bukan copy-paste
4. Natural bahasa Indonesia (JANGAN BAHASA INGGRIS!)
5. Max 1-2 tags (atau tanpa tag lebih baik)
6. 150-280 karakter

Format: Langsung tulis tweet dalam bahasa Indonesia. Jangan ada penjelasan atau metadata.

Contoh style yang benar:
"LIMITLESS dominasi AI Agents dengan 7% mindshare. Funding AI agent protocols naik 340% Q4 2024. Prediksi: category leader bisa grab 15% dalam 6 bulan. Menurut kalian, siapa kompetitor terdekat?"

Generate HANYA konten tweet-nya."""

        response = client.chat.completions.create(
            model="x-ai/grok-2-1212",
            messages=[
                {"role": "system", "content": prompt_template['system']},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=500,
            extra_headers={
                "HTTP-Referer": "https://yourapp.vercel.app",
                "X-Title": "YAPS Content Generator"
            }
        )
        
        generated_content = response.choices[0].message.content
        if generated_content:
            generated_content = generated_content.strip()
        else:
            generated_content = ""
        
        scoring = analyze_yaps_score(generated_content)
        
        return jsonify({
            'content': generated_content,
            'project': project,
            'prompt_type': prompt_type,
            'scoring': scoring,
            'model': 'Grok 2 (via OpenRouter)'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_yaps_score(content):
    """Simple scoring analysis"""
    score = {
        'crypto_relevance': 0,
        'engagement_potential': 0,
        'semantic_quality': 0,
        'total': 0,
        'feedback': []
    }
    
    if len(content) >= 50:
        score['crypto_relevance'] += 3
        score['feedback'].append('✅ Length optimal (50+ chars)')
    
    crypto_keywords = ['DeFi', 'L2', 'TVL', 'funding', 'protocol', 'AI', 'crypto', 'blockchain']
    if any(kw.lower() in content.lower() for kw in crypto_keywords):
        score['crypto_relevance'] += 4
        score['feedback'].append('✅ Crypto-relevant topics')
    
    if any(char.isdigit() for char in content):
        score['crypto_relevance'] += 3
        score['feedback'].append('✅ Contains data/metrics')
    else:
        score['feedback'].append('⚠️ Tidak ada data numerik')
    
    tags_count = content.count('@')
    if tags_count <= 2:
        score['engagement_potential'] += 5
        score['feedback'].append(f'✅ Tags optimal ({tags_count} tags)')
    else:
        score['engagement_potential'] += 2
        score['feedback'].append(f'⚠️ Terlalu banyak tags ({tags_count})')
    
    if '?' in content:
        score['engagement_potential'] += 3
        score['feedback'].append('✅ Ada question untuk engagement')
    
    if len(content) <= 280:
        score['engagement_potential'] += 2
        score['feedback'].append('✅ Twitter-friendly length')
    
    if any(word in content.lower() for word in ['kenapa', 'bagaimana', 'mengapa', 'analisis', 'thesis']):
        score['semantic_quality'] += 3
        score['feedback'].append('✅ Analytical tone')
    
    if not any(spam in content.lower() for spam in ['gm', 'gn', 'lfg', 'wagmi']):
        score['semantic_quality'] += 4
        score['feedback'].append('✅ Tidak ada spam phrases')
    
    if len(content.split()) > 15:
        score['semantic_quality'] += 3
        score['feedback'].append('✅ Depth content (15+ words)')
    
    score['total'] = score['crypto_relevance'] + score['engagement_potential'] + score['semantic_quality']
    
    if score['total'] >= 18:
        score['rating'] = 'EXCELLENT (High YAPS potential)'
    elif score['total'] >= 14:
        score['rating'] = 'GOOD (Medium-High YAPS)'
    elif score['total'] >= 10:
        score['rating'] = 'FAIR (Medium YAPS)'
    else:
        score['rating'] = 'NEEDS IMPROVEMENT'
    
    return score

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
