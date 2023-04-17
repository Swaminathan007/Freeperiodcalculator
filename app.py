from flask import *
from WebScraper import Scraper
app = Flask(__name__)
Details,Timetable,Name = [],[],[]
count = 0
signedin = False
countupdated = False
s = Scraper()
app.config["SECRET_KEY"] = "1234"
@app.route("/",methods = ["GET","POST"])
def home():
    global count
    if(request.method == "POST"):
        count = int(request.form.get("count"))
        return redirect(url_for("getdetails",n=1))
    return render_template("home.html")
@app.route("/getdetails/<int:n>",methods = ["GET","POST"])
def getdetails(n):
    global Timetable,Name,Details,signedin,count
    signedin = False
    try:
        s.getcaptcha()
    except:
        pass
    if(n > count):
        return redirect(url_for("Frees"))
    if(request.method == "POST"):
        regno = request.form.get("Regno")
        pwd = request.form.get("DOB")
        captcha = request.form.get("Captcha")
        signedin = True
        if(s.login(regno,pwd,captcha)):
            details = s.get_details()
            timetable = s.get_timetable()
            if details not in Details:
                Details.append(details)
                Timetable.append(timetable)
                flash(details[0]+ " added successfully")
            else:
                flash("Person from same class added already")
            s.logout()
            return redirect(url_for("getdetails",n = n+1))
        else:
            flash("Incorrect regno or password")
            return redirect(url_for("getdetails",n=n))
    return render_template("login.html",number = n)
@app.route("/Frees")
def Frees():
    timings = ["8:45-9:45","9:45-10:45","11:00-12:00","12:00-1:00","1:00-2:00","2:00-3:00","3:15-4:15","4:15-5:15"]
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    freehrs = []
    daysandhrs = []
    for i in range(len(days)):
        for j in range(len(timings)):
            daysandhrs.append([i,j])
    for i in range(len(daysandhrs)):
        c = 0
        day = daysandhrs[i][0]
        time = daysandhrs[i][1]
        for j in range(len(Timetable)):
            if(Timetable[j][day][time] == ''):
                c+=1
        if(c == count):
            freehrs.append(daysandhrs[i])
    return render_template("frees.html",Details=Details,timings=timings,days=days,Timetable=Timetable,freehrs=freehrs,n=count+1)
@app.route("/updatecount")
def updatecount():
    global count,signedin,Details,countupdated
    countupdated = True
    count+=1
    return redirect(url_for("getdetails",n=count))
@app.route("/viewtimetable/<int:id>")
def viewtimetable(id):
    global Timetable,Details
    timetable = Timetable[id]
    details = Details[id]
    timings = ["8:45-9:45","9:45-10:45","11:00-12:00","12:00-1:00","1:00-2:00","2:00-3:00","3:15-4:15","4:15-5:15"]
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    return render_template("profile.html",timetable=timetable,details=details,timings=timings,days=days)
@app.route("/delete/<int:id>")
def deletestudent(id):
    global Timetable,Details,count
    if(count > 2):
        Timetable.pop(id)
        det = Details.pop(id)
        count-=1
        flash(det[0] + " deleted")
    else:
        flash("Minimum 2 students required")
    return redirect(url_for("Frees"))
app.run(debug=True,host="0.0.0.0")

