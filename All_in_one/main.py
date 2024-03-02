from flask import Flask , redirect , render_template , request , session , url_for , flash

from flask_sqlalchemy import SQLAlchemy 

import pyttsx3

import pyjokes

import speech_recognition as sr

import requests 

import speedtest



app = Flask(__name__)

app.secret_key="hello"


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    feedback = db.Column(db.String(1000))

    def __init__(self,name,email,feedback):
       self.name=name
       self.email=email
       self.feedback=feedback
       



def speak(x):
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[2].id)
    rate=engine.getProperty('rate')
    engine.setProperty('rate',130)
    engine.say(x)
    engine.runAndWait()



def sptext():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("please speak ")
        recognizer.adjust_for_ambient_noise(source , duration=1)
        audio = recognizer.listen(source)
        try:
            print("recognizing....")
            data= recognizer.recognize_google(audio)
            print(data)
            return data

        except sr.UnknownValueError:
            speak("nothing")




@app.route('/')
def home():
   return render_template("index.html")

@app.route('/speed')
def speed():
   if "name" in session:
      return render_template("speed.html")
   else:
      flash("You need to login first")
      return redirect(url_for("sign"))
   


@app.route('/speed_check')
def speed_check():
   if "name" in session:
      sp=speedtest.Speedtest()
      sp.get_servers()
      down = str( round(sp.download()/(10**6),3)) + "Mbps"
      up = str( round(sp.upload()/(10**6),3)) + "Mbps"
      print(down)
      return render_template("speed_check.html", download = down , upload = up)
   
   else:
      flash("You need to login first")
      return redirect(url_for("sign"))
   

@app.route('/sudoku')
def sudo():
   if "name" in session:
      return render_template("sudo.html")
   else:
      flash("You need to login first")
      return redirect(url_for("sign"))

   

@app.route("/joke")
def joke():
    j1=pyjokes.get_joke(language="en",category="neutral")
    speak(j1)
    print(j1)
    return render_template("joke.html",content=j1)


@app.route("/weather" ,methods=["POST","GET"] )
def weather():
   if "name" in session:
    if request.method == "POST":
       city = request.form["search"]
       print(city)
       data = data = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=c105902388d8a6b23e1a402006d1e80c").json()
       weather = data["weather"][0]["main"]
       des = data["weather"][0]["description"]
       temp= data["main"]["temp"]
       print(temp)
       mn= data["main"]["temp_min"]
       max = data["main"]["temp_max"]
       return render_template("display_weather.html", city=city , w= weather , t= temp , d=des , mx = max , min = mn)
      
   else:
      return render_template("weather.html")


    

@app.route('/user')
def user():
   feed=None
   if "name" in session: 
      p_name=session["name"]
     
      mail = session["email"]
      if "feedback" in session:
         feed=session["feedback"]
      return render_template("user.html" , name = p_name , email=mail, feedback=feed)
      

   flash("you need to login first", "info")   
   return redirect("login")



@app.route('/sign' , methods=["POST","GET"])
def sign():
   feed=None
   if request.method == "POST":

      if "name" in session:
       session.pop("name" , None)
       session.pop("email" , None)
       session.pop("feedback" , None)

      p_name = request.form["nm"]
      user_exist=User.query.filter_by(name=p_name).first()
      if user_exist:
         flash("username already exist")
         return render_template("sign.html")
      else:
         session["name"]=p_name
         email=request.form["em"]
         session["email"]=email
         usr=User(p_name,email,feed)
         flash(" account created successfully")
         db.session.add(usr)
         db.session.commit()
         return redirect(url_for("user"))
      
   return render_template("sign.html")
   



@app.route("/view")
def view():
   return render_template("view.html", values = User.query.all())

@app.route('/login', methods=["POST","GET"])
def login():
   if request.method=="POST":
      name = request.form["nm"]
      pswd = request.form["ps"]
      if name == "Rishabh" and pswd == "12345":
         return redirect(url_for("view"))
      else:
         flash(" Enter Admin's credentials ")
       
   
   return render_template("login.html")


@app.route('/feedback', methods=["POST", "GET"])
def feedback():
    if "name" in session:
        if request.method == "POST":
            feed = request.form["feed"]
            session["feedback"] = feed
            p_name = session["name"]
            email = session["email"]
            user_exist=User.query.filter_by(name=p_name).first()
            if user_exist:
               user_exist.feedback = feed
               db.session.commit()

            else:
                usr=User(p_name,email,feed)
                db.session.add(usr)
                db.session.commit()
            

            flash("Your feedback is saved !!!")
            return redirect(url_for("user"))
        
        speak("please speak as your feedback is being recorded")
        data =  sptext().lower()
        return render_template("feed.html" , hello = data)
    else:
        flash("Login to give feedback")
        return redirect(url_for("login"))

 


@app.route('/logout')
def logout():
   if "name" in session:
    session.pop("name" , None)
    session.pop("email" , None)
    session.pop("feedback" , None)
   
   flash("you have been logged out","info")
   return redirect("login")



if __name__ == "__main__":
   with app.app_context(): 
     db.create_all()

   app.run(debug=True)
