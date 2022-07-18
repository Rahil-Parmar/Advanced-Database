from crypt import methods
from flask import Flask,render_template,request
import pyodbc
import redis
import time
import hashlib
import random
app = Flask(__name__)
sv = 'your_server'
db = 'your_database'
uname = 'username'
pw = 'password'
Hostname = 'adb.redis.cache.windows.net'
passw = 'redis_password'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+sv+';DATABASE='+db+';UID='+uname+';PWD='+pw)
c = conn.cursor()

cache = redis.Redis(host=Hostname,port=6380, ssl=True, db=0, password=passw)

@app.route('/',methods = ['GET', 'POST',])
def index():
    return render_template('index.html')


@app.route('/t1woc',methods = ['GET', 'POST'])
def t1woc():
    if request.method == 'POST':
        try:
            n = int(request.form.get('num'))
            start = time.time()
            for i in range(n):
                mag = random.randrange(1,4)
                query = 'SELECT * from dbo.ds_2 WHERE mag<'+str(mag)
                c.execute(query)
            end = time.time()
            return render_template('t1woc.html',time = end-start , num = n)        
        except Exception as e:
            print(e)
    return render_template('t1woc.html')


@app.route('/t1wc',methods = ['GET', 'POST'])
def t1wc():
    if request.method == 'POST':
        try:
            n = int(request.form.get('num'))
            total_time = 0
            for i in range(n):
                mag = random.randrange(1,9)
                query = 'SELECT * from dbo.ds_2 WHERE mag<'+str(mag)
                key = hashlib.sha224(query.encode('utf-8')).hexdigest()
                if cache.get(key):
                    start = time.time()
                    q = cache.get(key)
                    end = time.time()
                    total_time = total_time + (end-start)
                else:
                    start = time.time()
                    c.execute(query)
                    q = c.fetchall()
                    end = time.time()
                    cache.set(key, len(q))
                    cache.expire(key,30)
                    total_time = total_time + (end-start)
            return render_template('t1wc.html',time = total_time,num = n)
        except Exception as e:
            print(e)
    return render_template('t1wc.html')


@app.route('/t2woc',methods = ['GET', 'POST'])
def t2woc():
    if request.method == 'POST':
        try:
            n = int(request.form.get('num'))
            place = request.form.get('place')
            start = time.time()
            for i in range(n):
                mag = random.randrange(1,4)
                query = 'SELECT * from dbo.ds_2 WHERE mag<'+str(mag)+" AND place='"+place+"'"
                c.execute(query)
            end = time.time()
            return render_template('t2woc.html',time = end-start , num = n)        
        except Exception as e:
            print(e)
    return render_template('t2woc.html')


@app.route('/t2wc',methods = ['GET', 'POST'])
def t2wc():
    if request.method == 'POST':
        try:
            n = int(request.form.get('num'))
            place = request.form.get('place')
            total_time = 0
            for i in range(n):
                mag = random.randrange(1,4)
                query = 'SELECT * from dbo.ds_2 WHERE mag<'+str(mag)+" AND place='"+place+"'"
                key = hashlib.sha224(query.encode('utf-8')).hexdigest()
                if cache.get(key):
                    start = time.time()
                    q = cache.get(key)
                    end = time.time()
                    total_time = total_time + (end-start)
                else:
                    start = time.time()
                    c.execute(query)
                    q = c.fetchall()
                    end = time.time()
                    cache.set(key, len(q))
                    cache.expire(key,30)
                    total_time = total_time + (end-start)
            return render_template('t2wc.html',time = total_time,num = n)
        except Exception as e:
            print(e)
    return render_template('t2wc.html')
if __name__ == '__main__':
   app.run(debug=True)