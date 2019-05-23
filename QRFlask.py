from flask import Flask, render_template, request , url_for , send_from_directory , send_file , flash, redirect
from qrtools.qrtools import QR
import os
import warnings
import time

UP_FOLDER = os.path.join('static', 'QRcode')       #to configure the folder to upload images. under folder static there is a foler QRcode.

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'           #For flashing a message
app.config['UPLOAD_FOLDER'] = UP_FOLDER            #configuring it to flask varibale.


@app.route("/")                                    #Home page
def home():
    return render_template("terror.html")

@app.route("/about")                               #About page
def about():
    return render_template("about.html")

@app.route("/reach")                               #Reach us page
def reach():
   return render_template("reach.html")

@app.route("/QR/<p>")                                           
def QRdown(p):                      #the <p> is used to send a arguemnt, which is the filename of the file to be downloaded, this is used along with the folder
                                    #to enable download, the url will be /OR/p   #where p is the filename.
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=p, as_attachment=True)

@app.route("/QRIMG/<p>")
def QRIMG(p):

    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], p)  #to get the filename (by combining the folder and url variable p)

    #return send_file(full_filename , attachment_filename="lol.png")     #used to send the file from directory to web.
    #try replacing this with render template.

    return render_template("QRIMG.html",user_image=str("/"+full_filename),fname=p)   #Note the extra "/" before the filename, that is used to get the correct path.


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
        f.close()
        return redirect("/")                                #Will redirect the user to the home page.

    elif request.method == "GET":                               #send the template onto html.
        return render_template("suggestion.html")


@app.route("/upload",methods=['GET', 'POST'])                   #get = user gets onto the page, post = user wants to post in the page.
def upload():
    return render_template("upload.html")
   #return """  <html> hello world lol i am new to this thing</html>   """  #works as equivalent of an HTML page.


@app.route("/form", methods = ["POST","GET"])
def form():
    if request.method == "POST":                #If the user wants to post on this page.
       
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

        ####os.system("mv " + qr.filename + str(" Front_end/static/QRcode/"+form_fname+".png "))   #FOR LOCAL       
        #we moved the temp qr file to static folder, we used relative addressing from the PWD.

        os.system("mv " + qr.filename + str(" /home/AdityaSingh17/flask_onweb/static/QRcode/"+form_fname+".png ")) #FOR WEB APP
        
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], (form_fname+".png"))    #under folder QRcode, there is a .png file.

        #return render_template("QR.html", user_image = full_filename)   #user_image is a variable in html file, so we just give the path to it.
        #return send_from_directory(app.config['UPLOAD_FOLDER'], filename=form_fname+".png", as_attachment=True) #use this function to directly enable the user to download the qr code!

        return render_template("QR.html", user_image = full_filename , fname=app.config['THEFILE'])   #fname was given for uniquely identifying the url!
        
    elif request.method == "GET":               #If the user "gets: onto this page.
        return render_template("form.html")


if __name__ == '__main__':
    app.run(debug = True)                          #debug=true will always reload the code when changes are made to the python file.


