from crypt import methods
from flask import Flask,render_template,request
import pyodbc
app = Flask(__name__)
sv = 'your_server'
db = 'your_database'
uname = 'username'
pw = 'password'
conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+sv+';DATABASE='+db+';UID='+uname+';PWD='+pw)
c = conn.cursor()

@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/task1',methods = ['GET','POST'])
def task1():
    if request.method == 'POST':
        mag = int(request.form.get('mag'))
        result = [['Fields','MAgnitude']]
        for i in range(1,mag+1):
            query = "SELECT COUNT(mag) from dbo.ds_2 WHERE mag BETWEEN "+str(i-1)+" AND "+str(i)
            c.execute(query)
            res = c.fetchone()
            result.append([str(i-1)+"-"+str(i),res[0]])
            # fields.append(str(i-1)+"-"+str(i))
            # values.append(res[0])
        print(result)
        return render_template('task1.html',result = result )
    return render_template('task1.html')

@app.route('/task2',methods = ['GET','POST'])
def task2():
    query = 'SELECT magType,COUNT(mag) FROM dbo.ds_2 GROUP BY magType'
    c.execute(query)
    data = c.fetchall()
    result = [['Magnitude Type','count']]
    for i in data:
        result.append([i[0],i[1]])
        # fields.append(i[0])
        # values.append(i[1])
    # print(data[:,1])
    return render_template('task2.html',result = result)

@app.route('/task3',methods = ['GET','POST'])
def task3():
    query = 'SELECT TOP 100 mag,depth from dbo.ds_2 ORDER BY DATE'
    c.execute(query)
    data = c.fetchall()
    result = [['Magnitude','Depth']]
    for i in data:
        result.append([i[0],i[1]])
    return render_template('task3.html',result = result)

if __name__ == '__main__':
   app.run(debug=True)