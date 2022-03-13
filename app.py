# C:/py_prj/app.py:
"""
Project skeleton: --------------------------
C:/py_prj/src:
.... passenger_wsgi.py
.... start_server.bat
.... [v] src 
........ __init__.py (empty file)
........ app.py 
........ [v] mymodule 
............ myutils.py 
........ __init__.py (empty file)
........[v] static
............ some stuff here (views, js, css) ...
-------------------------------------------------
"""

import sys
import os
import json
import cgi

from wsgiref import simple_server, util
from wsgiref.simple_server import make_server
from src.mymodule import myutils

def render(tpl):
    header_file = 'src/static/views/common/header.html'
    with open(header_file, 'r') as file:
        html_header = file.read().rstrip()

    navbar_file = 'src/static/views/common/navbar.html'
    with open(navbar_file, 'r') as file:
        html_navbar = file.read().rstrip()

    with open(tpl, 'r') as file:
        html_tpl = file.read().rstrip()
    
    footer_file = 'src/static/views/common/footer.html'
    with open(footer_file) as file:
        html_footer = file.read().rstrip()

    html = html_header + html_navbar + html_tpl + html_footer
    return html

def test1(environ, response):
    if environ['PATH_INFO'] == '/test1':
        index_file = 'src/static/views/templates/index.html'         
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        return util.FileWrapper(open(index_file, 'rb'))
    else:
        return None

def handle_favicon(environ, response):
    if environ['PATH_INFO'] == '/favicon.ico':  
        status = '200 OK'
        headers = [('Content-Type', 'image/x-icon')]
        response(status, headers)
        response = ''.join([''])
        return [response.encode()]
    else:
        return None

def handle_not_found(environ, response):
    myutils.dd('testttt')
    response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'not found']

def handle_about(environ, response):
    if environ['PATH_INFO'] == '/about':
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        #return util.FileWrapper(open(about_file, 'rb'))
        html = render('src/static/views/templates/about.html')
        response = ''.join([html]).encode()
        return [response]
    else:
        return None

def test2(environ, response):
    if environ['PATH_INFO'] == '/test2':
        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        response(status, headers)
        msg = 'TEST 1'
        message = '<html><body><h1>' + msg + '</h1><body></html>'
        response = '\n'.join([message])
        return [response.encode()]

def handle_home(environ, response):
    if environ['PATH_INFO'] == '/':
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        html = render('src/static/views/templates/home_tpl.html')
        response = '\n'.join([html])
        return [response.encode()]
    else: 
        return None

app_routes = {
    '/': handle_home,
    '/favicon.ico': handle_favicon,
    '/not_found': handle_not_found,
    '/about': handle_about,
    '/test1': test1
}

class App:

    def __init__(self, routes):
        self.routes = routes
    
    def __call__(self, environ, response):
        handler = self.routes.get(environ.get('PATH_INFO')) or self.routes.get('/not_found')
        return handler(environ, response)

application = App(app_routes)

httpd = make_server('localhost', 8000, application)
httpd.serve_forever()

