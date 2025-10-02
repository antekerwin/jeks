#!/usr/bin/env python3
"""
YAPS Content Generator - AI-powered content generator untuk maximize YAPS points
Bahasa Indonesia - Powered by Claude AI
"""

from flask import Flask, render_template, request, jsonify
import os
from anthropic import Anthropic

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
        "system": """Kamu adalah crypto analyst Indonesia yang ahli membuat konten Twitter data-driven untuk YAPS.

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

WAJIB:
- 100% BAHASA INDONESIA
- Max 1 tag atau tanpa tag
- 150-280 karakter
- Data/metrics spesifik

HINDARI:
- Bahasa Inggris
- Keyword stuffing
- Generic statements"""
    },
    
    "competitive": {
        "name": "🎯 Positioning & Kompetitor",
        "description": "Analisis competitive landscape dan unique differentiation",
        "system": """Kamu adalah crypto strategist Indonesia yang ahli analisis kompetitif untuk YAPS.

ATURAN YAPS:
- Crypto Relevance (30%): Market structure understanding
- Smart Followers Engagement (50%): Thought leadership
- Semantic Analysis (20%): Original positioning analysis

STRUKTUR:
1. Market context & kategori
2. Competitive map (2-3 competitors)
3. Unique differentiation
4. Thesis siapa yang menang
5. Question untuk community

WAJIB:
- 100% BAHASA INDONESIA
- Max 1 tag atau tanpa tag
- 150-280 karakter
- Comparative insight

HINDARI:
- Bahasa Inggris
- Shilling tanpa objektif"""
    },
    
    "thesis": {
        "name": "💡 Forward-Looking Thesis",
        "description": "Prediksi trend, market impact, contrarian take",
        "system": """Kamu adalah crypto thought leader Indonesia yang ahli membuat thesis & prediction untuk YAPS.

ATURAN YAPS:
- Crypto Relevance (30%): Trend understanding
- Smart Followers Engagement (50%): Provocative but backed thesis
- Semantic Analysis (20%): Original thinking

STRUKTUR:
1. Trend observation
2. Positioning project
3. Clear thesis/prediction
4. Supporting reasoning
5. Risk consideration
6. Question untuk debate

WAJIB:
- 100% BAHASA INDONESIA
- Max 1 tag atau tanpa tag
- 150-280 karakter
- Bold thesis

HINDARI:
- Bahasa Inggris
- Opinion tanpa backing"""
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
        
        # CLAUDE AI VIA ANTHROPIC
        client = Anthropic(api_key="sk-ant-api03-mFoT7JFGxZO9vTgF0wN0mKLHxqO9WvY7fVw_example")  # Ganti dengan API key Anda
        
        prompt_template = PROMPT_TEMPLATES[prompt_type]
        
        user_message = f"""Generate konten Twitter untuk:

Project: {project_name}
Category: {project['category']}
Mindshare: {project['mindshare']}

Tulis 1 tweet bahasa Indonesia yang optimized untuk YAPS.

Output format: Hanya tweet-nya saja, tanpa penjelasan."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=prompt_template['system'],
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        generated_content = message.content[0].text.strip()
        
        scoring = analyze_yaps_score(generated_content)
        
        return jsonify({
            'content': generated_content,
            'project': project,
            'prompt_type': prompt_type,
            'scoring': scoring,
            'model': 'Claude 3.5 Sonnet'
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
