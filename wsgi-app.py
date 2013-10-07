#!/usr/bin/env python
from flask import Flask, Response
from atom_generator import (
    atom_generator,
    nya_sh,
    yousei_raws_org,
    kuroi_raws_ws,
)

app = Flask(__name__)

app.config.from_object("local_settings")
APPLICATION_ROOT = app.config["APPLICATION_ROOT"] or ""


@app.route("%s/" % APPLICATION_ROOT)
def hello():
    return "Hello World!"


@app.route("%s/nya.sh" % APPLICATION_ROOT)
@app.route("%s/nya.sh/<sub>" % APPLICATION_ROOT)
def nya_sh_feed(sub=""):
    try:
        feed = nya_sh.AtomGenerator("http://nya.sh/%s" % sub)
    except IOError as e:
        return Response(atom_generator.error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")


@app.route("%s/yousei-raws.org/<path:sub>" % APPLICATION_ROOT)
def yousei_raws_org_feed(sub=""):
    try:
        feed = yousei_raws_org.AtomGenerator("http://yousei-raws.org/%s" % sub)
    except IOError as e:
        return Response(atom_generator.error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")


@app.route("%s/kuroi.raws.ws/<path:sub>" % APPLICATION_ROOT)
def kuroi_raws_ws_feed(sub=""):
    try:
        feed = kuroi_raws_ws.AtomGenerator("http://kuroi.raws.ws/%s" % sub)
    except IOError as e:
        return Response(atom_generator.error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")


if __name__ == "__main__":
    app.run()
