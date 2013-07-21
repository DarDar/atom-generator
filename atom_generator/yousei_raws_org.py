from atom_generator import AtomGeneratorBase
from lxml import html, etree


class AtomGenerator(AtomGeneratorBase):

    def update(self):
        if not self.src:
            raise ValueError('Source is not set')

        self._fg.id(self.src)
        self._fg.link(href=self.src)
        self._fg.language("en")

        page = html.parse(self.src).getroot()

        page.make_links_absolute()

        title = page.findtext("body//div[@id='center']/h2[@class='title']")
        if title:
            self._fg.title(title)
        else:
            self._fg.title(self.src)

        author = page.cssselect("html > body div.field-field-encoder > "
                                "div.field-items > div.field-item > div")
        if author:
            author = author[0].tail.strip()

        for torrent in page.cssselect(
                "html body div.content > div.field-field-torrent-file > "
                "div.field-items > div.field-item"):
            fe = self._fg.add_entry()

            anchor = torrent.find("div[@class='torrent-link']/a")
            if anchor is not None:
                fe.id(anchor.get("href"))
                fe.title(torrent.findtext("div/div/div/span") or
                         anchor.textcontent())
                fe.link(href=fe.id())

            if author:
                fe.author(name=author)

            content = torrent.find("div")
            if content:
                fe.content(etree.tostring(content[0], encoding=unicode))

        return self._fg.atom_str(pretty=True)
