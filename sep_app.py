import os
import sys
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

### INIT ###

app = Flask(__name__)
ROLES = {"admin" : ["employee", "scs"]}
#Dicts mapping roles to user names
USERS = {"admin"}

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sep.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SEP_SETTINGS', silent=True)

### DATABASE SET UP ###
@app.before_first_request
def init_db():
  db = get_db()
  with app.open_resource('sep.sql', mode='r') as schema:
    db.cursor().executescript(schema.read())
  db.commit()

def get_db():
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db

def connect_db():
  rv = sqlite3.connect(app.config['DATABASE'], check_same_thread=False)
  rv.row_factory = sqlite3.Row
  return rv

### ENDPOINTS ###
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    username = request.form['username']
    if username not in USERS or request.form['pass'] != app.config['PASSWORD']:
      error = "Incorrect login"
    else:
      session['logged_in'] = True
      session['username'] = username
      flash('Welcome, '+username)
      return render_template("root.html", access=ROLES[username])
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/')
def root():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  return render_template("root.html")



### GET ENDPOINTS ###

@app.route('/employees') 
def view_employees():
  """ User Story: User should be able to list employees"""
  db = get_db()
  cur = db.execute('select * from employees')
  Emp = cur.fetchall()
  return render_template("list_entries.html", employees = Emp, addAction='/add_employee')
  #Get all entries in tale 'employees'
  #Return view with all the employees

  pass

@app.route('/tasks')
def view_tasks():
  """ User Story: Service/Product dept. can view tasks"""
  pass

@app.route('/task')
def view_task():
  """ USer story: user should be able to view and alter separate tasks """
  pass

@app.route('/clients')
def view_clients():
  """User Story: User can view clients """
  pass

@app.route('/events')
def list_events():
  """ User Story: User can list events"""

  #Get all entries in table 'events'
  #Return view with all the events

  pass


### POST ENDPOINTS ###

@app.route('/add_employee', methods=['POST'])
def add_employee():
  """ User Story: HR should be able to add employees """
  error = None
  if request.method == 'POST':
    username = request.form['name']
    password = request.form['password']
    position = request.form['position']

  db = get_db();
  db.execute('insert into employee (name, password, position) values (?, ?, ?)',[username, password, position])
  db.commit()
  flash("new employee added")

    
  redirect(url_for('employee'))
  #Parse event info input
  #Insert new employee to table 'employees'

  pass

@app.route('/add_event', methods=['POST'])
def create_event():
  """ User story: User can create event"""

  #Parse event info input
  #Insert new event in to table 'events'

  pass

@app.route('/add_report', methods=['POST'])
def make_report():
  """ User Story: User can create a report"""

  pass

@app.route('/add_task', methods=['POST'])
def create_task():
  """ User story: Service/Production manager can add tasks"""
  pass



class Employee:
  def __init__(self, name, position):
    self.name = name
    self.position = position

class Event:
  def __init__(self, client_name, date, event_name, budget):
    self.client_name = client_name
    self.date = date
    self.event_name = event_name
    self.budget = budget

class Task:
  def __init__(self, sub_team, name, description, budget):
    self.client_name = client_name
    self.date = date
    self.event_name = event_name
    self.budget = budget

class Report:
  def __init__(self, generated_by, content):
    self.client_name = client_name
    self.date = date
    self.event_name = event_name
    self.budget = budget

