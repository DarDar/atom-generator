import re


class YouTube(object):
    def __init__(self, url=None):
        self._video_id = self._extract_id(url)

    def __call__(self, url=False):
        if url is None or url:
            self._video_id = self._extract_id(url)
        return self._video_id

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
        return self._video_id and "http://i.ytimg.com/vi/%s/0.jpg" % self._video_id

    def video(self):
        return self._video_id and "http://www.youtube.com/watch?v=%s" % self._video_id
