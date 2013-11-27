from flask import Flask
from feedgen.feed import FeedGenerator
from lxml import etree
import urllib2
import hashlib


def error_xml(e):
    error = etree.Element("error")
    error.text = str(e)
    return etree.tostring(error, pretty_print=True, xml_declaration=True, encoding="utf-8")


class AtomGeneratorBase(object):

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
