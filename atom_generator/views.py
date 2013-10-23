from flask import Response
from redis import StrictRedis
from atom_generator import (
    app,
    error_xml,
    nya_sh,
    yousei_raws_org,
    kuroi_raws_ws,
)

if app.config["REDIS"]:
    cache = StrictRedis(**app.config["REDIS"])
else:
    cache = None


@app.route("/nya.sh")
@app.route("/nya.sh/<sub>")
def nya_sh_feed(sub=""):
    try:
        feed = nya_sh.AtomGenerator("http://nya.sh/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")


@app.route("/yousei-raws.org/<path:sub>")
def yousei_raws_org_feed(sub=""):
    try:
        feed = yousei_raws_org.AtomGenerator("http://yousei-raws.org/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")


@app.route("/kuroi.raws.ws/<path:sub>")
def kuroi_raws_ws_feed(sub=""):
    try:
        feed = kuroi_raws_ws.AtomGenerator("http://kuroi.raws.ws/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), content_type="text/xml; charset=UTF-8")

    return Response(feed.feed(), content_type="text/xml; charset=UTF-8")