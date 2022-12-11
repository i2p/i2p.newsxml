#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
#
import flask
import logging
import sys
import os

app = flask.Flask(__name__)

def hit(x):
    pass
try:
    import stats
    hit = stats.engine.hit
except ImportError:
    stats = None

# this is the root path for news.xml server, must end it /
# i.e. http://news.psi.i2p/news/
# defaults to /
ROOT='/'
port=9696
if len(sys.argv) > 1:
    ROOT=sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

def has_lang(lang):
    """
    :return True if we have news for a language:
    """
    logging.info("Checking for language: " + lang)
    if '.' in lang or '/' in lang:
        return False
    return os.path.exists(os.path.join(app.static_folder, 'news_{}.su3'.format(lang)))

def serve_platform_feed(osname, branch):
    logging.info("Serving: "+ osname + " Branch: " + branch)
    lang = flask.request.args.get('lang', 'en')
    lang = lang.split('_')[0]
    hit(lang)
    fname = os.path.join(osname, branch, 'news.su3')
    if has_lang(lang):
        fname = os.path.join(osname, branch, 'news_{}.su3'.format(lang))
    return serveFile(os.path.join(app.static_folder, fname))

def serveFile(path):
    logging.info("Serving file: "+ path)
    return flask.send_file(path)

@app.route('/')
def index():
    """
    serve news stats page
    """
    logging.info("Serving news stats page")
    return flask.render_template('index.html',root=ROOT)

@app.route('/news.su3')
def news_su3():
    """
    serve news.su3
    """
    logging.info("Serving standard newsfeed")
    return serve_platform_feed("", "")

@app.route('/mac-arm64/stable/news.su3')
def news_mac_arm_stable_su3():
    """
    serve mac-arm64/stable/news.su3
    """
    return serve_platform_feed("mac-arm64", "stable")

@app.route('/mac/stable/news.su3')
def news_mac_stable_su3():
    """
    serve mac/stable/news.su3
    """
    return serve_platform_feed("mac", "stable")

@app.route('/win/beta/news.su3')
def news_win_beta_su3():
    """
    serve win/beta/news.su3
    """
    return serve_platform_feed("win", "beta")

@app.route('/netsize.svg')
def netsize_svg():
    """
    generate and serve network size svg
    """
    if stats:
        args = flask.request.args
        try:
            window = int(args['window'])
            tslice = int(args['tslice'])
            mult = int(args['mult'])
            resp = flask.Response(stats.engine.netsize(tslice, window, mult))
            resp.mimetype = 'image/svg+xml'
            return resp
        except Exception as e:
            print (e)
            flask.abort(503)
    # we don't have stats to show, stats module not imported
    flask.abort(404)


@app.route('/requests.svg')
def requests_svg():
    """
    generate and serve requests per interval graph 
    """
    args = flask.request.args
    if stats:
        try:
            window = int(args['window'])
            tslice = int(args['tslice'])
            mult = int(args['mult'])
            resp = flask.Response(stats.engine.requests(tslice, window, mult))
            resp.mimetype = 'image/svg+xml'
            return resp
        except Exception as e:
            print (e)
            flask.abort(503)
    flask.abort(404)

if __name__ == '__main__':
    # run it
    logging.basicConfig(level=logging.INFO)
    app.run('127.0.0.1', port)
