import sqlite3
from flask import Flask,request,render_template_string,redirect,url_for,flash
app=Flask(__name__);app.secret_key='replace-this-secret-before-deployment';DB='medibook.db'
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY,patient TEXT,email TEXT,provider TEXT,day TEXT,note TEXT)')
PROVIDERS=['General Consultation','Dental Care','Dermatology','Pediatrics']
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>MediBook</title><style>body{font:16px system-ui;background:#edf3f7;padding:24px}.box{max-width:760px;margin:auto;background:white;padding:25px;border-radius:15px}input,select,textarea{display:block;width:100%;padding:11px;margin:7px 0 14px;border:1px solid #cbd5df;border-radius:8px}button{padding:12px;background:#16836d;color:white;border:0;border-radius:8px}.item{border-top:1px solid #ddd;padding:12px 0}</style><div class=box><h1>🩺 MediBook</h1><p>Demo appointment request form. Do not enter sensitive health data.</p>{% for m in get_flashed_messages() %}<p>{{m}}</p>{% endfor %}<form method=post><label>Name<input name=patient required maxlength=100></label><label>Email<input name=email type=email required maxlength=200></label><label>Provider<select name=provider>{% for p in providers %}<option>{{p}}</option>{% endfor %}</select></label><label>Date<input name=day type=date required></label><label>Note<textarea name=note maxlength=500></textarea></label><button>Request appointment</button></form><h2>Saved demo requests</h2>{% for r in rows %}<div class=item><b>{{r[1]}}</b> — {{r[3]}}<br>{{r[4]}} · {{r[2]}}</div>{% else %}<p>No requests yet.</p>{% endfor %}<small>Local demo only. No provider is notified.</small></div>"""
@app.route('/',methods=['GET','POST'])
def home():
 if request.method=='POST':
  f=request.form;p=f.get('patient','').strip();e=f.get('email','').strip();d=f.get('provider','');day=f.get('day','')
  if not p or not e or d not in PROVIDERS or not day:flash('Complete all required fields.');return redirect(url_for('home'))
  with sqlite3.connect(DB) as c:c.execute('INSERT INTO appointments(patient,email,provider,day,note) VALUES(?,?,?,?,?)',(p,e,d,day,f.get('note','')[:500]))
  flash('Saved locally. No clinic was contacted.');return redirect(url_for('home'))
 with sqlite3.connect(DB) as c:rows=c.execute('SELECT id,patient,email,provider,day FROM appointments ORDER BY id DESC').fetchall()
 return render_template_string(PAGE,rows=rows,providers=PROVIDERS)
if __name__=='__main__':app.run(debug=False)
