import os
from flask import Flask,request,jsonify,render_template_string
from dotenv import load_dotenv
from google import genai
load_dotenv();app=Flask(__name__)
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>DeniAI Studio</title><style>body{font:16px system-ui;background:#101827;color:#eef4ff;padding:20px}.box{max-width:760px;margin:35px auto;background:#1b2940;padding:25px;border-radius:16px}textarea{width:100%;min-height:120px;padding:12px;border-radius:8px}button{padding:12px 18px;background:#91adff;border:0;border-radius:8px}pre{white-space:pre-wrap;background:#111b2c;padding:16px;border-radius:8px}</style><div class=box><h1>✨ DeniAI Studio</h1><p>Gemini-powered writing, brainstorming and coding assistant.</p><textarea id=prompt placeholder='Write your prompt…'></textarea><p><button onclick=ask()>Generate</button></p><pre id=result>Response appears here.</pre></div><script>async function ask(){result.textContent='Thinking…';try{let r=await fetch('/api/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({prompt:prompt.value})}),d=await r.json();result.textContent=d.text||d.error||'No response'}catch(e){result.textContent=e.message}}</script>"""
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
