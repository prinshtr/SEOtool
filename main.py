from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Allow your WordPress site to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/audit")
def audit_url(url: str):
    if not url.startswith('http'):
        url = f"https://{url}"
        
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        report = {
            "url": url,
            "status": "Success",
            "ssl": url.startswith('https'),
            "title": soup.title.string if soup.title else "Missing",
            "h1": soup.find('h1').get_text() if soup.find('h1') else "Missing",
            "page_size_kb": round(len(response.content) / 1024, 2)
        }
        return report
    except Exception as e:
        return {"status": "Error", "message": str(e)}