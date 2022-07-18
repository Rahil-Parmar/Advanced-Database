from crypt import methods
from flask import Flask,render_template,request
import pandas as pd
import pyodbc
from geopy import distance
app = Flask(__name__)
sv = 'your_server'
db = 'your_database'
uname = 'username'
pw = 'password'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+sv+';DATABASE='+db+';UID='+uname+';PWD='+pw)
c = conn.cursor()
@app.route('/',methods = ['GET', 'POST',])
def index():
    return render_template('index.html')


@app.route('/search',methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('In post')
        mag = request.form.get('mag')
        query = 'SELECT * from dbo.all_month WHERE mag>'+mag
        c.execute(query)
        row = c.fetchall()
        df = pd.DataFrame((tuple(t) for t in row))
        print(df.head())
        columns = [' ','time', 'latitude', 'longitude', 'depth', 'mag', 'magType', 'nst', 'gap', 'dmin', 'rms', 'net', 'id', 'updated', 'place', 'type',  'horizontalError', 'depthError', 'magError', 'magNst', 'status', 'locationSource', 'magSource', 'date']
        return render_template('search.html',tables =[df.to_html(classes='data', header="true")],titles=columns )        
    return render_template('search.html')


@app.route('/SearchDate',methods = ['GET', 'POST',])
def SearchDate():
    if request.method == 'POST':
        mag1 = request.form.get('mag1')
        mag2 = request.form.get('mag2')
        day = request.form.get('day')
        query = 'SELECT * from dbo.all_month WHERE mag>'+mag1+" AND mag<"+mag2+" AND datediff(d,date,GETDATE()) <"+day 
        c.execute(query)
        row = c.fetchall()
        df = pd.DataFrame((tuple(t) for t in row))
        return render_template('SearchDate.html',tables =[df.to_html(classes='data', header="true")],titles=df.columns )
    return render_template('SearchDate.html')


@app.route('/eqInRange',methods = ['GET', 'POST',])
def eqInRange():
    if request.method == 'POST':
        lat = float(request.form.get('lat'))
        lon = float(request.form.get('lon'))
        query = 'SELECT * from dbo.all_month'
        c.execute(query)
        row = c.fetchall()
        df = pd.DataFrame.from_records(row, columns=[col[0] for col in c.description])
        longlat = zip(df['latitude'],df['longitude'])
        df['dist'] = [distance.distance(x,(lat,lon)).miles for x in longlat]
        data = df[df['dist']<1000]
        return render_template('eqInRange.html',tables =[data.to_html(classes='data', header="true")],titles=data.columns.values )
    return render_template('eqInRange.html')

@app.route('/cluster',methods=['GET','POST'])
def cluster():
    if request.method == 'POST':
        n = int(request.form.get('num'))
    return render_template('cluster.html')
if __name__ == '__main__':
   app.run(debug=True)