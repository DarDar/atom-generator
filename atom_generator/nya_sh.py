from lxml import html, etree
from lxml.builder import E
from dateutil import parser, tz
import re
from atom_generator import AtomGeneratorBase
from atom_generator.video import YouTube


class AtomGenerator(AtomGeneratorBase):

    def _update(self, page=None):
        if not self.src:
            raise ValueError("Source is not set")

        self._fg.id(self.src)
        self._fg.link(href=self.src)
        self._fg.language("ru-ru")

        if page is None:
            page = html.parse(self.src).getroot()
        else:
            page = html.fromstring(page)

        page.make_links_absolute(base_url=self.src)

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
                author = re.match(ur"(.*) \u2014 (.*)", author)
                if author:
                    fe.author(name=author.group(1))
                    fe.updated(
                        parser.parse(author.group(2))
                        .replace(tzinfo=tz.gettz("Europe/Moscow"))
                    )
                    fe.published(fe.updated())

            content = quote.find("div[@class='content']")
            if content is not None:
                etree.strip_tags(content, "noindex")
                # Replace thumbnail with its original image
                # <a href="full-size"><img src="thumbnail"/></a> -> <img src="full-size"/>
                for image in content.xpath(".//a/img[last()=1]"):
                    anchor = image.getparent()
                    image.set("src", anchor.get("href"))
                    anchor.getparent().replace(anchor, image)
                fe.content(etree.tostring(content, encoding=unicode))
            else:
                youtube = YouTube()
                videos = []
                for video in quote.iterfind("div/object/embed"):
                    video_src = video.get("src")
                    if youtube(video_src):
                        link = E.a(E.img(src=youtube.thumbnail(), href=youtube.video()))
                    else:
                        link = E.a(video_src, href=video_src)
                    videos.append(E.div(link))
                if videos:
                    if len(videos) == 1:
                        content = videos[0]
                    else:
                        content = etree.Element("div")
                        content.extend(videos)
                    fe.content(etree.tostring(content, encoding=unicode))

        return self._fg.atom_str(pretty=True)
