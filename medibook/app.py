import os,sqlite3,secrets
from flask import Flask,request,render_template_string,redirect,url_for,flash
app=Flask(__name__);app.secret_key=os.getenv('FLASK_SECRET_KEY') or secrets.token_hex(32);DB=os.getenv('MEDIBOOK_DB','medibook.db')
with sqlite3.connect(DB) as c:c.execute('CREATE TABLE IF NOT EXISTS appointments(id INTEGER PRIMARY KEY,patient TEXT,email TEXT,provider TEXT,day TEXT,note TEXT)')
PROVIDERS=['General Consultation','Dental Care','Dermatology','Pediatrics']
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>MediBook</title><style>*{box-sizing:border-box}body{font:16px/1.6 Inter,system-ui;background:linear-gradient(135deg,#e6f5f2,#f4f7fb);padding:24px;color:#18313a}.box{max-width:800px;margin:18px auto;background:white;padding:clamp(20px,4vw,36px);border:1px solid #dcebe8;border-radius:22px;box-shadow:0 18px 55px #1a54401a}h1{font-size:36px;letter-spacing:-.04em}input,select,textarea{display:block;width:100%;padding:12px;margin:7px 0 15px;border:1px solid #cbdedb;border-radius:10px;font:inherit}button{padding:12px 18px;background:#147c69;color:white;border:0;border-radius:10px;font-weight:700;cursor:pointer}.item{border-top:1px solid #e1ece9;padding:14px 0}small{color:#647b78}</style><div class=box><h1>🩺 MediBook</h1><p>Demo appointment request form. Do not enter sensitive health data.</p>{% for m in get_flashed_messages() %}<p>{{m}}</p>{% endfor %}<form method=post><label>Name<input name=patient required maxlength=100></label><label>Email<input name=email type=email required maxlength=200></label><label>Provider<select name=provider>{% for p in providers %}<option>{{p}}</option>{% endfor %}</select></label><label>Date<input name=day type=date required></label><label>Note<textarea name=note maxlength=500></textarea></label><button>Request appointment</button></form><h2>Saved demo requests</h2>{% for r in rows %}<div class=item><b>{{r[1]}}</b> — {{r[3]}}<br>{{r[4]}} · {{r[2]}}</div>{% else %}<p>No requests yet.</p>{% endfor %}<small>Local demo only. No provider is notified.</small></div>"""
@app.route('/',methods=['GET','POST'])
def home():
 if request.method=='POST':
  f=request.form;p=f.get('patient','').strip();e=f.get('email','').strip();d=f.get('provider','');day=f.get('day','')
  if not p or len(p)>100 or not e or len(e)>200 or d not in PROVIDERS or not day:flash('Complete all required fields.');return redirect(url_for('home'))
  with sqlite3.connect(DB) as c:c.execute('INSERT INTO appointments(patient,email,provider,day,note) VALUES(?,?,?,?,?)',(p,e,d,day,f.get('note','')[:500]))
  flash('Saved locally. No clinic was contacted.');return redirect(url_for('home'))
 with sqlite3.connect(DB) as c:rows=c.execute('SELECT id,patient,email,provider,day FROM appointments ORDER BY id DESC').fetchall()
 return render_template_string(PAGE,rows=rows,providers=PROVIDERS)
if __name__=='__main__':app.run(debug=False)
