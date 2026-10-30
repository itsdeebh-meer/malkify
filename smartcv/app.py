from flask import Flask,request,render_template_string
app=Flask(__name__)
PAGE="""<!doctype html><meta name=viewport content='width=device-width,initial-scale=1'><title>SmartCV</title><style>body{font:16px system-ui;background:#edf1f7;padding:20px}.box{max-width:820px;margin:auto;background:white;padding:26px;border-radius:15px}input,textarea{width:100%;padding:10px;margin:6px 0 13px;border:1px solid #ccd4df;border-radius:7px}button{padding:11px;background:#315ee8;color:white;border:0;border-radius:8px}.resume{border-top:2px solid #315ee8;margin-top:22px;padding-top:15px}@media print{form,button,.hint{display:none}}</style><div class=box><h1>SmartCV — Resume Builder</h1><p class=hint>Enter details, preview, then Print → Save as PDF.</p><form method=post>{% for key,label in fields %}<label>{{label}}{% if key in ['summary','experience'] %}<textarea name={{key}} rows=4>{{data[key]}}</textarea>{% else %}<input name={{key}} value="{{data[key]}}" {% if key=='name' %}required{% endif %}>{% endif %}</label>{% endfor %}<button>Update preview</button></form><section class=resume><h1>{{data.name or 'Your Name'}}</h1><h3>{{data.headline}}</h3><p>{{data.email}}</p><h2>Profile</h2><p>{{data.summary}}</p><h2>Skills</h2><p>{{data.skills}}</p><h2>Education & Experience</h2><p style='white-space:pre-line'>{{data.experience}}</p><button onclick=print()>Save as PDF</button></section></div>"""
FIELDS=[('name','Full name'),('headline','Professional headline'),('email','Email'),('summary','Summary'),('skills','Skills (comma separated)'),('experience','Education / experience')]
@app.route('/',methods=['GET','POST'])
def home():
 d={k:'' for k,_ in FIELDS}
 if request.method=='POST':d.update({k:request.form.get(k,'').strip() for k,_ in FIELDS})
 return render_template_string(PAGE,data=d,fields=FIELDS)
if __name__=='__main__':app.run(debug=False)
