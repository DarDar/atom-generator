from feedgen.feed import FeedGenerator
from lxml import etree


def error_xml(e):
    error = etree.Element("error")
    error.text = str(e)
    return etree.tostring(error, pretty_print=True, xml_declaration=True, encoding="utf-8")


class AtomGeneratorBase:

    # Redefine FeedGenerator.atom_str to return utf-8 string
    class _FeedGenerator(FeedGenerator):
        def atom_str(self, pretty=False, extensions=True):
            feed, doc = self._create_atom(extensions=extensions)
            return etree.tostring(feed, pretty_print=pretty, xml_declaration=True, encoding="utf-8")

    def __init__(self, src=None):
        self.src = src
        self._fg = self._FeedGenerator()
        if src:
            self.update()

    def feed(self):
        try:
            return self._fg.atom_str(pretty=True)
        except ValueError as e:
            return error_xml(e)
