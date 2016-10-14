import os
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application, StaticFileHandler
from sep_app import app

class MainHandler(RequestHandler):
  def get(self):
    self.write("Tornado msg")

settings = {
  "static_path": os.path.join(os.getcwd(), "static")
}

tr = WSGIContainer(app)
application = Application([(r"/tornado", MainHandler),
(r".*", FallbackHandler, dict(fallback=tr))
])

if __name__ == "__main__":
  port = 8080
  application.listen(port)
  print "Started Tornado containing sep_app running on port "+str(port)
  IOLoop.instance().start()