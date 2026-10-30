import os,sqlite3,secrets,string
from flask import Flask,request,redirect,render_template_string,abort
app=Flask(__name__);DB=os.getenv('LINKIFY_DB','linkify.db')
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS links(code TEXT PRIMARY KEY,url TEXT NOT NULL,clicks INTEGER DEFAULT 0)')
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>Linkify</title><style>*{box-sizing:border-box}body{font:16px/1.6 Inter,system-ui;background:radial-gradient(ellipse at 80% 0%,#dce7ff,#f2f5fa 55%);padding:24px;color:#1b2942}.box{max-width:760px;margin:36px auto;background:white;padding:clamp(20px,4vw,34px);border:1px solid #e0e7f1;border-radius:22px;box-shadow:0 18px 55px #23395d18}h1{font-size:36px;letter-spacing:-.04em}input{width:100%;padding:13px;margin:10px 0;border:1px solid #ccd6e5;border-radius:10px;font:inherit}button{padding:12px 18px;background:#345ee8;color:white;border:0;border-radius:10px;font-weight:700;cursor:pointer}a{color:#3158cf;overflow-wrap:anywhere}</style><div class=box><h1>🔗 Linkify</h1><form method=post><input name=url type=url required placeholder='https://example.com'><button>Shorten URL</button></form>{% if code %}<p>Short link: <a href='/{{code}}'>{{base}}/{{code}}</a></p>{% endif %}<h2>Recent links</h2>{% for r in rows %}<p><a href='/{{r[0]}}'>{{base}}/{{r[0]}}</a> → {{r[1]}} · {{r[2]}} clicks</p>{% endfor %}</div>"""
@app.route('/',methods=['GET','POST'])
def home():
 code=None
 if request.method=='POST':
  url=request.form.get('url','').strip()
  if not url.startswith(('https://','http://')):abort(400)
  code=''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(7))
  with sqlite3.connect(DB) as c:c.execute('INSERT INTO links(code,url) VALUES(?,?)',(code,url))
 with sqlite3.connect(DB) as c:rows=c.execute('SELECT code,url,clicks FROM links ORDER BY rowid DESC LIMIT 25').fetchall()
 return render_template_string(PAGE,code=code,rows=rows,base=request.host_url.rstrip('/'))
@app.route('/<code>')
def go(code):
 with sqlite3.connect(DB) as c:r=c.execute('SELECT url FROM links WHERE code=?',(code,)).fetchone()
 if not r:abort(404)
 with sqlite3.connect(DB) as c:c.execute('UPDATE links SET clicks=clicks+1 WHERE code=?',(code,))
 return redirect(r[0])
if __name__=='__main__':app.run(debug=False)
