import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from google import genai
load_dotenv()
app=Flask(__name__)
client=genai.Client(api_key=os.environ['GEMINI_API_KEY']) if os.getenv('GEMINI_API_KEY') else None
@app.get('/')
def home(): return render_template('index.html')
@app.post('/chat')
def chat():
    if client is None: return jsonify(error='Configure GEMINI_API_KEY on the server.'),503
    message=(request.json or {}).get('message','').strip()
    if not message or len(message)>4000: return jsonify(error='Enter a message up to 4000 characters.'),400
    try:
        response=client.models.generate_content(model='gemini-2.5-flash',contents=message)
        return jsonify(reply=response.text or 'No response generated.')
    except Exception:
        app.logger.exception('Gemini request failed')
        return jsonify(error='AI request failed. Check server configuration and logs.'),502
if __name__=='__main__': app.run(debug=os.getenv('FLASK_DEBUG')=='1')
