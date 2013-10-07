from atom_generator import AtomGeneratorBase
from lxml import html
import urllib2
import json
import re


class AtomGenerator(AtomGeneratorBase):

    def update(self):
        if not self.src:
            raise ValueError("Source is not set")

        self._fg.id(self.src)
        self._fg.link(href=self.src)
        self._fg.language("en")

        page = urllib2.urlopen(self.src).read()
        re.S = True
        info = re.search(r"<script>\s*var posts = \[(.*)\];\s*</script>", page)
        info = json.loads(info.group(1))

        self._fg.title(info.get("title", self.src))

        author = info.get("user")
        if author:
            author = author.get(
                "fullname",
                author.get("username"))

        self._fg.pubDate(info.get("createdAt"))
        self._fg.updated(info.get("updatedAt"))

        div = html.fromstring(info.get("body"))
        for torrent in div.xpath("//strong[text()='Download']/"
                                 "following::a[not(text()='magnet')]"):
            fe = self._fg.add_entry()

            fe.id(torrent.get("href"))
            fe.title(torrent.text_content())
            fe.link(href=fe.id())

            if author:
                fe.author(name=author)

            fe.updated(self._fg.updated())

            fe.content(fe.title())

        return self._fg.atom_str(pretty=True)
