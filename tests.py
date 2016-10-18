import os
import unittest
import tempfile
import sep_app


class FlaskrTestCase(unittest.TestCase):

  def setUp(self):
    self.db_fd, sep_app.app.config['DATABASE'] = tempfile.mkstemp()
    sep_app.app.config['TESTING'] = True
    self.app = sep_app.app.test_client()
    with sep_app.app.app_context():
      sep_app.init_db()

  def tearDown(self):
    os.close(self.db_fd)
    os.unlink(sep_app.app.config['DATABASE'])

  def login(self, name, word):
    return self.app.post('/login', data=dict(username=name, password=word),follow_redirects=True)

  def logout(self):
    return self.app.get('/logout', follow_redirects=True)

  def add_report(self, name, creator, content):
    return self.app.post('/add_report', data=dict(report_name=name, creator=creator, content=content), follow_redirects=True)

  def remove_report(self, name):
    return self.app.post('/delete_report/name', data=dict(name=name), follow_redirects=True)

  def test_login_logout(self):
    rv = self.login(name='admin', word='default')
    #print rv.data
    assert 'Welcome,' in rv.data
    rv = self.logout()
    #print rv.data
    assert 'You were logged out' in rv.data
    rv = self.login('aadmin', 'default')
    #print rv.data
    assert 'Incorrect login' in rv.data
    rv = self.login('admin', 'wrong_password')
    #print rv.data
    assert 'Incorrect login' in rv.data

  def test_create_remove_report(self):
    rv = self.add_report("name", "creator", "content")
    #print rv.data
    assert 'Added!' in rv.data
    rv = self.remove_report("name")
    #print rv.data
    assert 'removed!' in rv.data

  def test_access_roles(self):
    rv = self.login(name='admin', word='default')
    #print rv.data
    assert 'employees' in rv.data
    assert 'events' in rv.data
    assert 'tasks' in rv.data
    assert 'reports' in rv.data
    assert 'clients' in rv.data

    rv = self.login(name='josh', word='kitten')
    #print rv.data
    assert not 'employees' in rv.data
    assert 'events' in rv.data
    assert not 'tasks' in rv.data
    assert 'reports' in rv.data
    assert not 'clients' in rv.data

if __name__ == '__main__':
  unittest.main()
