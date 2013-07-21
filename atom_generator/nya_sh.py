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

        title = page.findtext("head/title")
        if title:
            self._fg.title(title)
        else:
            self._fg.title(self.src)

        description = page.find("head/meta[@name='description']")
        if description is not None:
            self._fg.description(description.get("content"))

        for quote in page.iterfind("body//div[@class='q']"):
            fe = self._fg.add_entry()

            anchor = quote.find("div[@class='sm']/a")
            if anchor is not None:
                fe.id(anchor.get("href"))
                fe.title(anchor.text_content())
                fe.link(href=fe.id())

            author = quote.findtext("div[@class='sm']/i")
            if author:
                author = re.match(u'(.*) \u2014 (.*)', author)
                if author:
                    fe.author(name=author.group(1))
                    fe.updated(
                        parser.parse(author.group(2))
                        .replace(tzinfo=tz.gettz('Europe/Moscow'))
                    )
                    fe.published(fe.updated())

            content = quote.find("div[@class='content']")
            if content is not None:
                fe.content(etree.tostring(content, encoding=unicode))

        return self._fg.atom_str(pretty=True)
