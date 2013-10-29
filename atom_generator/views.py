from flask import Response
from atom_generator import (
    app,
    error_xml,
    nya_sh,
    yousei_raws_org,
    kuroi_raws_ws,
)

if app.config["REDIS"]:
    from redis import Redis
    from werkzeug.contrib.cache import RedisCache
    cache = RedisCache(Redis(**app.config["REDIS"]), default_timeout=60*60*24*7)
else:
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache(default_timeout=60*60*24*7)


@app.route("/nya.sh")
@app.route("/nya.sh/<sub>")
def nya_sh_feed(sub=""):
    try:
        feed = nya_sh.AtomGenerator("http://nya.sh/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), mimetype="text/xml")

    return Response(feed.feed(), mimetype="application/atom+xml")


@app.route("/yousei-raws.org/<path:sub>")
def yousei_raws_org_feed(sub=""):
    try:
        feed = yousei_raws_org.AtomGenerator("http://yousei-raws.org/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), mimetype="text/xml")

    return Response(feed.feed(), mimetype="application/atom+xml")


@app.route("/kuroi.raws.ws/<path:sub>")
def kuroi_raws_ws_feed(sub=""):
    try:
        feed = kuroi_raws_ws.AtomGenerator("http://kuroi.raws.ws/%s" % sub, cache)
    except IOError as e:
        return Response(error_xml(e), mimetype="text/xml")

    return Response(feed.feed(), mimetype="application/atom+xml")
