import os
import sys
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

### INIT ###
Roles = {"admin": ["employees", "events", "tasks", "reports", "clients"],
        "marketing": ["events", "reports"],
        "HR": ["employees"],
        "scs": ["clients", "events"] }

app = Flask(__name__)
#Dicts mapping roles to user names
USERS = {"admin": "admin", "josh": "marketing", "mike": "HR", "Hannah": "scs"}

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sep.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SEP_SETTINGS', silent=True)

### DATABASE SET UP ###
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
      return redirect(url_for('root'))
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


  username = session.get('username')
  access_rights = Roles[USERS[username]]
  return render_template("root.html", access_rights=access_rights, role = USERS[username], username = username)



### GET ENDPOINTS ###

@app.route('/employees') 
def view_employees():
  """ User Story: User should be able to list employees"""

  #Get all entries in tale 'employees'
  #Return view with all the employees
  #return render_template("list_entries.html", employees=employees)
  db = get_db()
  cur = db.execute('select name, position from employees order by id desc')
  employees = cur.fetchall()
  return render_template("list_employees.html", entries = employees, list_object ="Employees")
  pass

@app.route('/tasks')
def view_tasks():
  """ User Story: Service/Product dept. can view tasks"""
  db = get_db()
  cur = db.execute('select client_name, task_date, task_name, budget from tasks order by id desc')
  tasks = cur.fetchall()
  return render_template("list_tasks.html", entries = tasks, list_object ="Tasks")

  pass

@app.route('/reports')
def view_reports():
  """ User Story: HR/Marketing can view reports"""
  db = get_db()
  cur = db.execute('select report_name, creator from reports order by id desc')
  reports = cur.fetchall()
  return render_template("list_reports.html", entries = reports, list_object ="Reports")

@app.route('/clients')
def view_clients():
  """User Story: User can view clients """
  db = get_db()
  cur = db.execute('select client_name, client_status, number_of_events from clients order by id desc')
  clients = cur.fetchall()
  return render_template("list_clients.html", entries = clients, list_object ="Clients")
  pass

@app.route('/events')
def list_events():
  """ User Story: User can list events"""

  #Get all entries in table 'events'
  #Return view with all the events
  db = get_db()
  cur = db.execute('select event_name, event_date, client_name, budget from events order by id desc')
  events = cur.fetchall()
  return render_template("list_events.html", entries = events, list_object ="Events")
  pass

@app.route('/task/<name>')
def view_task(name):
  """ USer story: user should be able to view and alter separate tasks """
  db = get_db()
  cur = db.execute('select client_name, task_date, task_name, budget, sub_team from tasks where name = \''+name+'\'')
  task = cur.fetcone()
  return render_template("single_view.html", entry = task)
  pass

@app.route('/employee/<name>')
def view_employee(name):
  """ USer story: user should be able to view and alter separate tasks """
  db = get_db()
  cur = db.execute('select name, position from employees where name = \''+name+'\'')
  employee = cur.fetchone()
  return render_template("single_view.html", entry = employee)
  pass

@app.route('/report/<name>')
def view_report(name):
  """ USer story: user should be able to view and alter separate tasks """
  db = get_db()
  cur = db.execute('select report_name, creator, content from reports where name = \''+name+'\'')
  report = cur.fetcone()
  return render_template("single_view.html", entry = report)
  pass

@app.route('/event/<name>')
def view_event(name):
  """ USer story: user should be able to view and alter separate tasks """
  db = get_db()
  cur = db.execute('select event_name, event_date, client_name from events where name = \''+name+'\'')
  event = cur.fetcone()
  return render_template("single_view.html", entry = event)
  pass

@app.route('/client/<name>')
def view_client(name):
  """ USer story: user should be able to view and alter separate tasks """
  db = get_db()
  cur = db.execute('select client_name, client_status, number_of_events from clients where name = \''+name+'\'')
  client = cur.fetcone()
  return render_template("single_view.html", entry = client)
  pass



### POST ENDPOINTS ###

@app.route('/add_employee', methods=['POST'])
def create_employee():
  """ User Story: HR should be able to add employees """

  #Parse event info input
  #Insert new employee to table 'employees'
  db = get_db()
  cur = db.execute('insert into employees name, position from employees order by id desc')
  pass

@app.route('/add_event', methods=['POST'])
def create_event():
  """ User story: User can create event"""

  #Parse event info input
  #Insert new event in to table 'events'
  pass

@app.route('/add_report', methods=['POST'])
def create_report():
  """ User Story: User can create a report"""

  pass

@app.route('/add_task', methods=['POST'])
def create_task():
  """ User story: Service/Production manager can add tasks"""
  pass

@app.route('/add_client', methods=['POST'])
def create_client():
  """ User story: Service/Production manager can add tasks"""
  pass


if __name__ == "__main__":
  app.run()
  init_db()


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

