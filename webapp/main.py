#-*-coding:utf-8-*-  
#qpy:webapp:PyConChina2015
#qpy://127.0.0.1:8080/
"""
PyConChina2015 App's sourcecode

@Author river
"""

from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template, redirect

import urllib2
import os
import json
#### 常量定义 #########
ASSETS = "/assets/"
ROOT = os.path.dirname(os.path.abspath(__file__))


#### 安装WebApp依赖包 ####
def _setup_webapp_denps():
    pass

try:
    _setup_qpyapp_denps()
except:
    pass

from jsonconv import *


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

def fonts_static(filepath):
    return static_file(filepath, root=ROOT+'/fonts')


def server_static(filepath):
    return static_file(filepath, root=ROOT+'/assets')

########################################
PAGE_TEMP = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<meta name="description" content="">
<meta name="author" content="">
<script src="{{assets}}jquery.min.js"></script>
<link href="{{assets}}bootstrap.min.css" rel="stylesheet" />
<script src="{{assets}}bootstrap.min.js"></script>   
<script language='javascript'>
$(document).ready(function(){
%s
});
</script>
<style>
ul{ list-style-type: none; margin:0px;padding:0px }
tbody tr th:first-child{ width:80px }
table.nolimit tbody tr th:first-child{ width:auto }
.tt { padding-left:10px; }
.float-right { float:right }
.center { text-align:center }
.p5 { padding:5px }
</style>
</head>  
<body>
%s
</body>
</html>
""".replace("{{assets}}",ASSETS)

######### WEBAPP ROUTERS ###############

def _get_json_content():
    jurl = 'http://cn.pycon.org/2015/pycon.json'
    jfile = ROOT+'/pycon.json'
    if not os.path.exists(jfile):
        data = urllib2.urlopen(jurl)
        fd = open(jfile,'w')
        content = data.read()
        fd.write(content)
        data.close()
        fd.close()
    else:
        fd = open(jfile)
        content =fd.read()
        fd.close()
        
    return content

def home():
    JS = ""
    CONTENT = """
<nav class="navbar-inverse" role="navigation" id="navigation" style="background:#f9f9f9;border-bottom:1px solid #eee">
    <div class="container" >
        <ul>
            <a class="navbar-brand" style='color: #000;font-size: 23px;font-weight: bold;padding:10px;margin-left:0px' href="/a/qpython">
                <img src="http://pyconcn.qiniucdn.com/zoomquiet/res/logo/150801-cnpycon-barnner-h80.png" height="32">
                <span></span>                      
            </a>     
            <div style="float:right;margin: 10px 10px 0 0;" >
                <button onclick="milib.openUrl('http://cn.pycon.org/2015/donators.html')" class="btn btn-info" >
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
<div style='text-align:center;padding:10px'>
    <button onclick="location.href='/beijing/agenda'" class="btn btn-lg btn-success" >
        PyCon 北京 
    </button>
</div>
<div style='text-align:center;padding:10px'>
    <button onclick="location.href='/shanghai/agenda'" class="btn btn-lg btn-success" >
        PyCon 上海 
    </button>
</div>
<div style='text-align:center;padding:10px'>
    <button onclick="location.href='/shanghai/agenda'" class="btn btn-lg btn-success" >
        PyCon 广州 
    </button>
</div>


<script language='javascript'>milib.showDrawerMenu('{"menu":[{"title":"北京","url":"http://127.0.0.1:8080/beijing/agenda","icon":""},{"title":"上海","url":"http://127.0.0.1:8080/shanghai/agenda","icon":""},{"title":"广州","url":"http://127.0.0.1:8080/guangzhou/agenda","icon":""}]}')</script>
"""

    return template(PAGE_TEMP % (JS, CONTENT))


#############
def show_speakers():
    content = _get_json_content()
    jdata = json.loads(content)
    T = u"<h4 class='tt'>演讲者</h4>%s" % json2html.convert(json=jdata['speakers'], table_attributes="class=\"table table-bordered table-hover\"")
    return template(PAGE_TEMP % ('',T))

def get_speakers():
    content = _get_json_content()
    jdata = json.loads(content)
    speakers = jdata['speakers']
    return speakers
    
def beijing():
    return _agenda('beijing',u'PyCon 北京日程', u'http://event.31huiyi.com/118591776')

def shanghai():
    return _agenda('shanghai',u'PyCon 上海日程', u'http://event.31huiyi.com/118022165')

def guangzhou():
    return _agenda('guangzhou',u'PyCon 广州日程', u'http://event.31huiyi.com/118545334')

def _agenda(wh, title, url):
    content = _get_json_content()
    jdata = json.loads(content)
    agd = jdata['agenda'][wh]
    J = u"""
$.get('/speakers/', null, function(data){
$('th').each(function(){
    var val = $(this).html()
    if (val=='speaker') {
        $(this).html('主题')
    } else if (val == 'time') {
        $(this).html('时间')
    } else if (val == 'topic') {
        $(this).html('')
    }
});
$('td').each(function(){
    var val = $(this).html()
    if (typeof(data[val])!="undefined") {
        //console.log(data[val]['topic']['title'])
        $(this).html(data[val]['topic']['title']+" - "+data[val]['name']+"<div style='color:grey'>"+data[val]['topic']['preview']+"</div>")
    }
})
});"""
    O = u"""<h4 class='tt'>%s</h4>
<table class="table table-bordered table-hover">
<tr><th>日期</th><td>%s</td></tr>
<tr><th>地点</th><td>%s<br />%s</td></tr>
<tr><th>交通</th><td>%s</td></tr>
<tr><th>事件</th><td>%s</td></tr>
<tr><th>注意</th><td>%s</td></tr>
</table>
""" % (title, 
    agd['date'],
    agd['address'], 
    agd["maplink"], 
    agd['traffic'],
    agd['venue'], 
    agd['notices']
)

    L = u"""<div style='text-align:center;padding:10px'><button onclick="milib.openUrl('%s')" class="btn btn-lg btn-success" >报名参加</button></div>""" % url
    M = u"<h5 class='tt'>早上</h5>"
    
    for item in agd['morning']:
        M = M+json2html.convert(json=item, table_attributes="class=\"table table-bordered table-hover\"")

    M = M+u"<h5 class='tt'>中午</h5>"
    for item in agd['noon']:
        M = M+json2html.convert(json=item, table_attributes="class=\"table table-bordered table-hover\"")
    M = M+u"<h5 class='tt'>下午</h5>"
    for item in agd['afternoon']:
        M = M+json2html.convert(json=item, table_attributes="class=\"table table-bordered table-hover\"")
    M = M+u"<h5 class='tt'>闪电演讲</h5>"
    for item in agd['lightening_talks']:
        M = M+json2html.convert(json=item, table_attributes="class=\"table table-bordered table-hover\"")
    M = M+u"<h5 class='tt'>已取消</h5>"
    for item in agd['cancel_talks']:
        M = M+json2html.convert(json=item, table_attributes="class=\"table table-bordered table-hover\"")





    O = O+M
    
    return template(PAGE_TEMP % (J,O+L))

def work():
    redirect("https://qwork.quseit.cn")

######### WEBAPP ROUTERS ###############
app = Bottle()
app.route('/', method='GET')(home)
app.route('/work', method='GET')(work)
app.route('/speakers/', method='GET')(get_speakers)
app.route('/speakers/show/', method='GET')(show_speakers)
app.route('/beijing/agenda', method='GET')(beijing)
app.route('/shanghai/agenda', method='GET')(shanghai)
app.route('/guangzhou/agenda', method='GET')(guangzhou)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
app.route('/assets/<filepath:path>', method='GET')(server_static)
app.route('/fonts/<filepath:path>', method='GET')(fonts_static)

try:
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except Exception,ex:
    print "Exception: %s" % repr(ex)
