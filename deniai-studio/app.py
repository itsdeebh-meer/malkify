import os
from flask import Flask,request,jsonify,render_template_string
from dotenv import load_dotenv
from google import genai
load_dotenv();app=Flask(__name__)
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>DeniAI Studio</title><style>*{box-sizing:border-box}body{font:16px/1.6 Inter,system-ui;background:radial-gradient(ellipse at 80% 0%,#253d70,#0b1020 55%);color:#eef4ff;padding:22px}.box{max-width:850px;margin:38px auto;background:#151f34;border:1px solid #2b3b5a;padding:clamp(20px,4vw,36px);border-radius:22px;box-shadow:0 22px 70px #0005}h1{font-size:36px;letter-spacing:-.04em}textarea{width:100%;min-height:170px;padding:15px;border:1px solid #394b6b;border-radius:12px;background:#0e1729;color:white;font:inherit}button{padding:12px 20px;background:#9bb5ff;color:#101a31;border:0;border-radius:10px;font-weight:800;cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#0e1729;border:1px solid #283958;padding:18px;border-radius:12px;min-height:120px}</style><div class=box><h1>✨ DeniAI Studio</h1><p>Gemini-powered writing, brainstorming and coding assistant.</p><textarea id=prompt placeholder='Write your prompt…'></textarea><p><button onclick=ask()>Generate</button></p><pre id=result>Response appears here.</pre></div><script>async function ask(){result.textContent='Thinking…';try{let r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:prompt.value})}),d=await r.json();result.textContent=d.text||d.error||'No response'}catch(e){result.textContent=e.message}}</script>"""
@app.get('/')
def home():return PAGE
@app.post('/api/generate')
def generate():
 p=(request.json or {}).get('prompt','').strip()
 if not p:return jsonify(error='Enter a prompt.'),400
 if len(p)>8000:return jsonify(error='Prompt exceeds 8,000 characters.'),400
 key=os.getenv('GEMINI_API_KEY')
 if not key:return jsonify(error='Set GEMINI_API_KEY in .env.'),503
 try:
  response=genai.Client(api_key=key).models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.5-flash'),contents=p)
  return jsonify(text=response.text or '')
 except Exception:
  app.logger.exception('Gemini request failed')
  return jsonify(error='AI request failed. Check API key, model access and server logs.'),502
if __name__=='__main__':app.run(debug=False)
