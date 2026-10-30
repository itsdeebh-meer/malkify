import sqlite3,secrets,string
from flask import Flask,request,redirect,render_template_string,abort
app=Flask(__name__);DB='linkify.db'
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS links(code TEXT PRIMARY KEY,url TEXT NOT NULL,clicks INTEGER DEFAULT 0)')
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>Linkify</title><style>body{font:16px system-ui;background:#edf2f8;padding:24px}.box{max-width:680px;margin:40px auto;background:white;padding:25px;border-radius:15px}input{width:95%;padding:12px;margin:10px 0;border:1px solid #ccd4df;border-radius:8px}button{padding:12px;background:#315ee8;color:white;border:0;border-radius:8px}</style><div class=box><h1>🔗 Linkify</h1><form method=post><input name=url type=url required placeholder='https://example.com'><button>Shorten URL</button></form>{% if code %}<p>Short link: <a href='/{{code}}'>{{base}}/{{code}}</a></p>{% endif %}<h2>Recent links</h2>{% for r in rows %}<p><a href='/{{r[0]}}'>{{base}}/{{r[0]}}</a> → {{r[1]}} · {{r[2]}} clicks</p>{% endfor %}</div>"""
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
