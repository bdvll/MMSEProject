import os
import sys
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
#Dicts mapping roles to user names
logged_in_users = {}

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sep.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SEP_SETTINGS', silent=True)

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


@app.route('/')
def root():
  return "Succesfully served root of application!"

@app.route('/login')
def login():
  """ User story: User login"""
  pass

@app.route('/login')
def logout():
  """ User story: User logout"""
  pass

### GET ENDPOINTS ###

@app.route('/employees') 
def view_employees():
  """ User Story: User should be able to list employees"""

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

