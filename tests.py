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

if __name__ == '__main__':
  unittest.main()
