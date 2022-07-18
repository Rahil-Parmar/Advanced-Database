from itertools import permutations
import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request
import string
from itertools import permutations

app = Flask(__name__)
allowed_extension = {'txt'}
path = 'static/'

def allowed_file(filename):
  return "." in filename and \
    filename.rsplit(".", 1)[1].lower() in allowed_extension

@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')



@app.route("/search",methods = ['GET','POST'])
def search():
    directory = os.listdir('preprocessed/')
    if request.method=='POST':
        word = request.form.get('word')
        # word = lemmatizer.lemmatize(word,pos = 'v')
        message = []
        w = []
        for files in directory:
            file = open("preprocessed/"+files, encoding="utf8")
            for line_number, line in enumerate(file, start=1):  
                if word in line:
                    w.append(word)
                    message.append(line_number)
                    print(f"Word '{word}' found on line {line_number}")
        return render_template('search.html',message = message,word = w)
    return render_template('search.html')

@app.route("/searchCombine",methods = ['GET','POST'])
def searchCombine():
    directory = os.listdir('preprocessed/')
    if request.method=='POST':
        word = request.form.get('word')
        w_list = list(word.split())
        w_list = permutations(w_list)
        message = []
        w = []
        for files in directory:
            file = open("preprocessed/"+files, encoding="utf8")
            for line_number, line in enumerate(file, start=1):
                for permute in  w_list:
                    plist = list(permute)
                    plist = " ".join(plist)
                    print(plist)
                    print(line)   
                    if plist in line:
                        w.append(plist)
                        message.append(line_number)
                            # print(f"Word '{word}' found on line {line_number}")
        return render_template('searchCombine.html',message = message,word = w)
    return render_template('searchCombine.html')

if __name__ == '__main__':
    app.config["upload_folder"] = "static/"
    app.run(debug=True)