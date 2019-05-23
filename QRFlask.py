from flask import Flask, render_template, request , url_for , send_from_directory , send_file,redirect
from qrtools.qrtools import QR
import os
import warnings
import time
#import warnings
#warnings.filterwarnings("ignore")
UP_FOLDER = os.path.join('static', 'QRcode')      #to configure the folder to upload images. under folder static there is a foler QRcode.
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UP_FOLDER           #again, configure!


@app.route("/")
def home():
    return render_template("terror.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/form", methods = ["POST","GET"])
def form():
    if request.method == "POST":
        form_name = request.form["name"]
        form_phone = request.form["phone"]
        form_email = request.form["email"]
        form_fname = request.form["fname"]
        """ """
        warnings.filterwarnings("ignore")
        final_data = [('N',form_name),('TEL',str("+91"+form_phone)),('EMAIL',form_email)]
        qr = QR(data=final_data,data_type='phonebook',level='h',margin_size=10,pixel_size=10)
        qr.encode()

        if not form_fname:                  #checks string is null or no    #the user may or maynot give the filename, so we do this to store it.
            form_fname = "temp"

        form_fname = form_fname+str(time.time())        #this is done to work around the caching problem of flask.

        os.system("mv " + qr.filename + str(" /home/AdityaSingh17/flask_onweb/static/QRcode/"+form_fname+".png "))           #relative moving, easy when we deploy. note /front_end will cause error


        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], (form_fname+".png"))    #under folder QRcode, there is a .png file.

        #return render_template("upload.html" , user_image = full_filename)   

        app.config['THEFILE'] = form_fname+".png"           #made a config to be used futher in my file (for app.route("/form/QR"))

        app.config['THEURL'] = form_fname

        #return render_template("QR.html", user_image = full_filename)   #user_image is a variable in html file, so we just give the path to it.

        return render_template("QR.html", user_image = full_filename , fname=app.config['THEFILE'])   #fname was given for uniquely identifying the url!

        #return qr.filename

        #return send_from_directory(app.config['UPLOAD_FOLDER'], filename=form_fname+".png", as_attachment=True) #use this function to directly enable the user to download the qr code!

    elif request.method == "GET":
        return render_template("form.html")


@app.route("/reach")
def reach():
    return render_template("reach.html")

@app.route("/upload")                                                 #new additon! also changed in terror.html about this upload ref link.
def upload():
    return render_template("upload.html")
   #this thing creates a damn html page and renders it. tf. return """  <html> hello world lol i am new to this thing</html>   """


@app.route("/QR/<p>")                                           #used to redirect direct download! sending the file as download from the same file it is viewd, QR!
def QRdown(p):                      #the <p> is used to send a arguemnt, which is the filename of the file to be downloaded, this is used along with the folder
                                    #to enable download, the url will be /form/ORIMAGE/filename(p)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=p, as_attachment=True)

@app.route("/QRIMG/<p>")
def QRIMG(p):
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], p)
    #return render_template("QRIMG.html" , user_image=full_filename )

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], p)

    #return send_file(full_filename , attachment_filename="lol.png")     #used to send the file from directory to web.
    #try replacing this with render template.

    return render_template("QRIMG.html",user_image=str("/"+full_filename),fname=p)   #this motherfucker is working!!!!!
    #just had to add that extra "/" before the static file to make it working lol. whatastupid i am lol. wasted 2 hrs lol.

@app.route("/suggestion",methods = ["POST","GET"])
def suggestion():
    if request.method == "POST":                                #send data to flask
        form_fb = request.form["feedback"]
        form_fname = request.form["name"]
        form_score = request.form["rating"]
        f = open("feedback.txt","a")
        f.write("\n \nFFEEDBACK AT "+str(time.ctime()))       #time.ctime() gives op as  Sun Sep 10 01:19:25 2017
        f.write("\nFEEDBACK FROM : "+form_fname)
        f.write("\nFEEDBACK SCORE : "+form_score+"\n")
        f.write(form_fb)
        f.write("\nDONE")
        f.close
        return redirect("/")

    elif request.method == "GET":                               #send the template onto html.
        return render_template("suggestion.html")

if __name__ == '__main__':
    app.run(debug = True)


