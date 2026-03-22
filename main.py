from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/audit")
def audit_url(url: str):
    if not url.startswith('http'):
        url = f"https://{url}"
        
    try:
        headers = {'User-Agent': 'SEO-Audit-Bot-Pro-2026'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Social Media Readiness (Open Graph)
        og_title = soup.find('meta', property='og:title')
        
        # 2. Canonical Check (Duplicate Content Protection)
        canonical = soup.find('link', rel='canonical')
        
        # 3. AI Bot Check (robots.txt)
        try:
            domain = url.split('//')[-1].split('/')[0]
            robots_res = requests.get(f"https://{domain}/robots.txt", timeout=5)
            ai_friendly = "gptbot" not in robots_res.text.lower()
        except:
            ai_friendly = True

        return {
            "status": "Success",
            "url": url,
            "ssl": url.startswith('https'),
            "title": soup.title.string if soup.title else "Missing",
            "h1": soup.find('h1').get_text().strip() if soup.find('h1') else "Missing",
            "og_status": "✅ Optimized" if og_title else "❌ Missing Social Tags",
            "canonical": "✅ Set" if canonical else "❌ Missing Canonical",
            "ai_status": "✅ AI-Search Ready" if ai_friendly else "⚠️ Blocking AI",
            "page_size_kb": round(len(response.content) / 1024, 2)
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}