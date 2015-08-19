#-*-coding:utf-8-*-  
#qpy:webapp:PyConChina2015
#qpy://127.0.0.1:8080/
"""
PyConChina2015 App's sourcecode

@Author river
"""

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, redirect


######### QPYTHON WEB SERVER ###############

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() 
        print "# QWEBAPPEND"


######### BUILT-IN ROUTERS ###############
def __exit():
    global server
    server.stop()

def __ping():
    return "ok"

def server_static(filepath):
    return static_file(filepath, root='/sdcard')

######### WEBAPP ROUTERS ###############
def home():
    return template("""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="/assets/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <script src="/assets/static/jquery.min.js"></script>   
  </head>  
  <body>
      <nav class="navbar-inverse" role="navigation" id="navigation" style="background:#f9f9f9;border-bottom:1px solid #eee">
        <div class="container" >
          <div class="navbar-header">
             <ul style="margin-left:-30px;">
                  <a class="navbar-brand" style='color: #000;font-size: 23px;font-weight: bold;padding:10px;margin-left:0px' href="/a/qpython">
                      <img src="http://pyconcn.qiniucdn.com/zoomquiet/res/logo/150801-cnpycon-barnner-h80.png" height="32">
                      <span></span>                      
                  </a>     
                  <div style="float:right;margin: 10px 10px 0 0;" >
                    <button onclick="milib.openUrl('http://cn.pycon.org/2015/donators.html')" class="btn btn-info" ><span class="glyphicon glyphicon-plus-sign"></span>
                      赞助大会
                    </button>                    
                 </div>             
                  <div style="clear:both"></div>
             </ul>
             
             <div style="clear:both"></div>
             <div style="padding:0px 15px 10px 15px">
                  PyCon 是全球 Pythoneer 最盛大的年度聚会,由 PSF(Python 基金会)支持,致力于营造愉快的多元化的 Python 技术主题大会. PyConChina 是由 CPyUG(华蠎用户组)获得授权举办的 中国PyCon 年会. 迄今已是第五届, 由 PyChina.org 发起,CPyUG/TopGeek 等社区协同,在 9月13~27日 (程序员节 前后), 北京/上海/广州 联办.
             </div>
          </div>          
      </nav>
    <script language='javascript'>milib.showDrawerMenu('{"menu":[{"title":"议题","url":"/topics","icon":""},{"title":"讲师","url":"/speakers","icon":""}]}')</script>
  </body>
</html>
""")

def work():
    redirect("https://qwork.quseit.cn")

######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/work', method='GET')(work)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/assets/<filepath:path>', method='GET')(server_static)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except Exception,ex:
    print "Exception: %s" % repr(ex)
