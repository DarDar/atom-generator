from flask import Flask
from feedgen.feed import FeedGenerator
from lxml import etree
import urllib2
import hashlib
import re


def error_xml(e):
    error = etree.Element("error")
    error.text = str(e)
    return etree.tostring(error, pretty_print=True, xml_declaration=True, encoding="utf-8")


class YouTube(object):
    def __init__(self, url=None):
        self._video_id = self._extract_id(url)

    @property
    def video_id(self):
        return self._video_id

    @video_id.setter
    def video_id(self, url):
        self._video_id = self._extract_id(url)

    def _extract_id(self, url=None):
        """Extract youtube video ID

        Based on `youtube_dl` code
        """
        if not url:
            return None

        YOUTUBE_URL = r"""^
(?:
    (?:https?://)?                      # http(s):// (optional)
    (?:(?:(?:
        (?:\w+\.)?youtube(?:-nocookie)?\.com/|
        tube\.majestyc\.net/|
        youtube\.googleapis\.com/)      # the various hostnames, with wildcard subdomains
    (?:.*?\#/)?                         # handle anchor (#/) redirect urls
    (?:                                 # the various things that can precede the ID:
        (?:(?:v|embed|e)/)|             # v/ or embed/ or e/
        (?:                             # or the v= param in all its forms
            (?:
                (?:watch|movie)(?:_popup)?(?:\.php)?
            )?                          # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
            (?:\?|\#!?)                 # the params delimiter ? or # or #!
            (?:.*?&)?                   # any other preceding param (like /?s=tuff&v=xxxx)
            v=
        )
    ))|
    youtu\.be/                          # just youtu.be/xxxx
    )
)?                                      # all until now is optional -> you can pass the naked ID
([0-9A-Za-z_-]{11})                     # here is it! the YouTube video ID
(?(1).+)?                               # if we found the ID, everything can follow
$"""
        video_id = re.match(YOUTUBE_URL, str(url), re.VERBOSE)
        return video_id and video_id.group(1)

    def thumbnail(self):
        return self.video_id and "http://i.ytimg.com/vi/%s/0.jpg" % self.video_id

    def video(self):
        return self.video_id and "http://www.youtube.com/watch?v=%s" % self.video_id


class AtomGeneratorBase:

    # Redefine FeedGenerator.atom_str to return utf-8 string
    class _FeedGenerator(FeedGenerator):
        def atom_str(self, pretty=False, extensions=True):
            feed, doc = self._create_atom(extensions=extensions)
            return etree.tostring(feed, pretty_print=pretty, xml_declaration=True, encoding="utf-8")

    def _hash(self, str):
        return hashlib.sha256(str).hexdigest()

    def _src_key(self):
        return self.__module__ + ":source:" + self.src

    def _xml_key(self):
        return self.__module__ + ":xml:" + self.src

    def __init__(self, src=None, cache=None):
        self.src = src
        self.cache = cache
        self._fg = self._FeedGenerator()
        if src:
            self.update()

    def update(self, force=False):
        try:
            if not self.cache:
                self._xml = self._update()
                return self._xml

            page = urllib2.urlopen(self.src).read()
            src_hash = self._hash(page)

            if not force and self.cache.get(self._src_key()) == src_hash:
                self._xml = self.cache.get(self._xml_key())
                if self._xml is not None:
                    return self._xml
            self._xml = self._update(page)

            self.cache.set_many({self._src_key(): src_hash,
                                 self._xml_key(): self._fg.atom_str(pretty=True)})

        except ValueError as e:
            self._xml = error_xml(e)

        return self._xml

    def feed(self):
        return self._xml

app = Flask(__name__)
app.config.from_object("local_settings")

import atom_generator.views
