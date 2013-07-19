#!/usr/bin/env python
from flask import Flask, Response
from nya_sh import nya_sh

app = Flask(__name__)

app.config.from_object('rss-generator_config')
APPLICATION_ROOT = app.config['APPLICATION_ROOT'] or ''


@app.route("%s/" % APPLICATION_ROOT)
def hello():
    return "Hello World!"


@app.route("%s/nya.sh" % APPLICATION_ROOT)
@app.route("%s/nya.sh/<sub>" % APPLICATION_ROOT)
def nya_sh_feed(sub=""):
    return Response(nya_sh(sub), content_type="text/xml; charset=UTF-8")


if __name__ == "__main__":
    app.run()
