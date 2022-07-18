from crypt import methods
from flask import Flask, render_template, request, url_for,redirect,jsonify
import time
# import numpy as np
app = Flask(__name__)

class Timer:
    def __init__(self, time):
        self.c_time = time

    def decrement(self):
        if self.c_time > 0:
            self.c_time = self.c_time - 1
        return self.c_time

teacherName = ''
studentName = ''
adminName = ''
hint = ''
error = ''
t = True
s = False
tot_ques = 0
score = 0
totalScore = 0
average = 0
question = ''
answer = ''
questions = []
answers = []
timer = Timer(time= 0)
@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/redirect',methods=['GET','POST'])
def redirect():
    global teacherName
    global studentName
    global adminName
    if request.method == 'POST':
        name = request.form.get('name')
        person = request.form.get('person')
        if person == 'student':
            studentName = name
            return render_template('student.html')
        elif person == 'teacher':
            teacherName = name
            return render_template('teacher.html')
        else:
            adminName  = name
            return render_template('admin.html')

@app.route('/student',methods = ['GET','POST'])
def student():
    global score
    global totalScore
    global average
    global answer
    global question
    global answers
    global error
    global s
    global t
    if request.method == 'POST' and s == True :
        answer = request.form.get('ans')
        answers.append(answer)
        s = False
        t = True
    else:
        error = 'Please let teacher ask the question!'
        time.sleep(10)
        error = ''
    return render_template('student.html')

@app.route('/teacher',methods = ['GET','POST'])
def teacher():
    global score
    global average
    global totalScore
    global tot_ques
    global question
    global answer
    global error
    global s
    global t
    global timer
    if request.method == 'POST' and t == True:
        if request.form.get('ques') != '':
            question = request.form.get('ques')
            a = int(request.form.get('time'))
            timer = Timer(time = a)
            questions.append(question)
            tot_ques += 1
            t = False
            s = True
        if request.form.get('score') != '':
            score = int(request.form.get('score'))
            totalScore += score
            average = totalScore/tot_ques
    else:
        error = 'Please let the student answer the previous question!'
        time.sleep(10)
        error = ''
    return render_template('teacher.html') 

@app.route('/admin',methods = ['GET','POST'])
def admin():
    global hint
    if request.method == 'POST':
        hint = request.form.get('hint')
    return render_template('admin.html')

@app.route('/get_data',methods = ['GET','POST'])
def get_data():
    global teacherName
    global studentName
    global hint
    global score
    global totalScore
    global average
    global question
    global answer
    global error
    global timer
    timer.decrement()
    if timer.c_time == 0:
        question = ''
        answer = ''
        t = True
        s = False
    # score = np.random.randint(0,100)
    # totalScore = np.random.randint(0,100)
    # average = np.random.randint(0,100)
    return jsonify(tname = teacherName,sname = studentName,hint = hint,score = score,total = totalScore,average = average,question = question,answer = answer,error = error,timer = timer.c_time)


if __name__ == '__main__':
    app.run(debug=True)