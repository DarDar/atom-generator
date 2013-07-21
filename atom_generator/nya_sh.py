from atom_generator import AtomGeneratorBase
from lxml import html, etree
from dateutil import parser, tz
import re


class AtomGenerator(AtomGeneratorBase):

    def update(self):
        if not self.src:
            raise ValueError('Source is not set')

        self._fg.id(self.src)
        self._fg.link(href=self.src)
        self._fg.language("ru-ru")

        page = html.parse(self.src).getroot()

        page.make_links_absolute()

        title = page.xpath("//title")
        if title:
            self._fg.title(title[0].text_content())
        else:
            self._fg.title(self.src)

        description = page.xpath("//meta[@name='description']")
        if description:
            self._fg.description(description[0].get("content"))

        for quote in page.xpath("//div[@class='q']"):
            fe = self._fg.add_entry()

            anchor = quote.xpath("div[@class='sm']/a")
            if anchor:
                fe.id(anchor[0].get("href"))
                fe.title(anchor[0].text_content())
                fe.link(href=fe.id())

            author = quote.xpath("div[@class='sm']/i")
            if author:
                m = re.match(u'(.*) \u2014 (.*)', author[0].text_content())
                if m:
                    fe.author(name=m.group(1))
                    fe.updated(
                        parser.parse(m.group(2))
                        .replace(tzinfo=tz.gettz('Europe/Moscow'))
                    )
                    fe.published(fe.updated())

            content = quote.xpath("div[@class='content']")
            if content:
                fe.content(etree.tostring(content[0], encoding=unicode))

        return self._fg.atom_str(pretty=True)
