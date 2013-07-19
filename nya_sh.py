#!/usr/bin/env python
import re
from lxml import html, etree
from feedgen.feed import FeedGenerator
from dateutil import parser, tz


# Redefine FeedGenerator.atom_str to return utf-8 string
def atom_str(self, pretty=False, extensions=True):
    feed, doc = self._create_atom(extensions=extensions)
    return etree.tostring(
        feed,
        pretty_print=pretty,
        xml_declaration=True,
        encoding="utf-8"
    )

FeedGenerator.atom_str = atom_str


def error_xml(e):
    error = etree.Element("error")
    error.text = str(e)
    return etree.tostring(error, xml_declaration=True, encoding="utf-8")


def nya_sh(sub=""):
    url = "http://nya.sh/%s" % sub

    fg = FeedGenerator()
    fg.id(url)
    fg.link(href=url)
    fg.language("ru-ru")

    try:
        page = html.parse(url).getroot()
    except IOError as e:
        return error_xml(e)

    page.make_links_absolute()

    title = page.xpath("//title")
    if title:
        fg.title(title[0].text_content())
    else:
        fg.title(url)

    description = page.xpath("//meta[@name='description']")
    if description:
        fg.description(description[0].get("content"))

    for quote in page.xpath("//div[@class='q']"):
        fe = fg.add_entry()

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

    try:
        return fg.atom_str(pretty=True)
    except ValueError as e:
        return error_xml(e)


if __name__ == "__main__":
    pass
