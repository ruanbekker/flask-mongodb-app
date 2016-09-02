from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import time

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mongodb_database'
app.config['MONGO_URI'] = 'mongodb://user:pass@host.domain.com:12345/mongodb_database'

mongo = PyMongo(app) # instantiate the db connection

@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')	

    return render_template('login.html')    


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.usersessions
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('redirect.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.usersessions
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Username Already Exists'
    
    return render_template('register.html')

@app.route('/add/<string:userid>/<string:name>/<string:surname>/<int:age>/<string:job>', methods=['GET'])
def add(userid, name, surname, age, job):
    if 'username' in session:
        user = mongo.db.users0
        users = user.insert(
            {
                '_id': userid,
                'name': name,
                'surname': surname,
                'age': age,
                'job': job
            }
        )
        return render_template('add.html', userid=userid, name=name, surname=surname, age=age, job=job)

    return redirect(url_for('index'))

@app.route('/get/')
def get_all(name=None):
    if 'username' in session:
        user = mongo.db.users0
        users = user.find({})
        count = user.count({})

        return render_template('index.html', namevalues=users, number=count)

    return redirect(url_for('index'))

@app.route('/get/<string:userid>')
def get_userid(userid):
    if 'username' in session:
        user = mongo.db.users0
        users = user.find(
            {
                '_id': userid
            }
        )
    
        count = users.count()
        return render_template('index.html', namevalues=users, number=count)
    
    return redirect(url_for('index'))

@app.route('/get/job/<string:job>')
def get_job(job):
    if 'username' in session:
        user = mongo.db.users0
        users = user.find(
            {
                'job': job
            }
        )

        count = users.count()
        return render_template('index.html', namevalues=users, number=count)

    return redirect(url_for('index'))

@app.route('/get/name/<string:name>')
def get_name(name):
    if 'username' in session:
        user = mongo.db.users0
        users = user.find(
            {
                'name': name
            }
        )

        count = users.count()
        return render_template('index.html', namevalues=users, number=count)

    return redirect(url_for('index'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/query_userid', methods=['GET', 'POST'])
def search_userid():
    user = mongo.db.users0
    userid = request.form['userid']
    query = user.find({'_id': userid})
    count = query.count()

    return render_template('search2.html', query=query, number=count)

@app.route('/query_name', methods=['GET', 'POST'])
def search_name():
    user = mongo.db.users0
    name = request.form['name']
    query = user.find({'name': name})
    count = query.count()

    return render_template('search2.html', query=query, number=count)


@app.route('/query_job', methods=['GET', 'POST'])
def search_job():
    user = mongo.db.users0
    job = request.form['job']
    query = user.find({'job': job})
    count = query.count()

    return render_template('search2.html', query=query, number=count)


if __name__ == '__main__':
    app.secret_key = 'sekret'
    app.run(debug=True)
