from flask import Flask, redirect, render_template, request, session, url_for

import google.generativeai as genai

GOOGLE_API_KEY="AIzaSyBQNVnxzVcR5dmS2DZ_B-GriOEw4o5h3GY"
genai.configure(api_key=GOOGLE_API_KEY)

gemini_pro = genai.GenerativeModel("gemini-pro")
 
app = Flask(__name__) 
app.config["SECRET_KEY"] = 'secret_key' 


@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if request.method == 'POST':

      session['name'] = request.form['name']
      session['century'] = request.form['century']
      session['gakki'] = request.form['gakki']
      session['type'] = request.form['type']
      session['sentaku'] = request.form['sentaku']

      name=session['name']
      century=session['century']
      gakki=session['gakki']
      type=session['type']
      sentaku=session['sentaku']
    
      if name == "" and century == "" and gakki == "" :
         prompt = type + "の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.その曲の作曲者も示してください.ヘッダーは省略してください．"

      elif name == "" and century == "" :
        prompt = type+"で"+gakki+sentaku+"曲の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.その曲の作曲者も示してください.ヘッダーは省略してください．"

      elif name == "" and gakki == "" :
        prompt = century+"世紀に作曲された" + type+ "の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.その曲の作曲者も示してください.ヘッダーは省略してください．"
      
      elif century == "" and gakki == "" :
        prompt = name+"が作曲した"+type+"の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.ヘッダーは省略してください．"
      
      elif name == "" :
        prompt = century+"世紀に作曲された"+type+"で"+gakki+sentaku+"曲の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.その曲の作曲者も示してください.ヘッダーは省略してください．"

      elif gakki == "" :
        prompt = century+"世紀に"+name+"が作曲した"+type+"の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.ヘッダーは省略してください．"

      elif century == "" :
        prompt = name+"が作曲した"+type+"で"+gakki+sentaku+"曲の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.ヘッダーは省略してください．"

      else:
        prompt = century+"世紀に"+name+"が作曲した"+type+"で"+gakki+sentaku+"曲の曲名を一曲だけ返してください.ただし、曲名は日本語で表記してください.ヘッダーは省略してください．"

      response = gemini_pro.generate_content(prompt)
      session['kyoku'] = response.text
      return redirect(url_for('anwser')) 
    return render_template('music.html') 

@app.route('/anwser') 
def anwser(): 
  return render_template('anwser.html') 
 
 
if __name__ == '__main__':
  app.run(debug=True,port=80) 
