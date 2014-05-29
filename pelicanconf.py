#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Martin Putniorz'
SITENAME = u'bysputnikus'
SITEURL = ''

TIMEZONE = 'Europe/Prague'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 10

ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

PAGE_URL = 'pages/{slug}'

CATEGORY_URL = False
CATEGORY_SAVE_AS = False
TAGS_URL = False
TAGS_SAVE_AS = False

THEME = "/home/sputnikus/workspace/pure"
TYPOGRIFY = True

PLUGIN_PATH = '/home/sputnikus/workspace/pelican-plugins'
PLUGINS = ['related_posts', ]

RELATED_POSTS_MAX = 3

TWITTER_USERNAME = 'sputnikus'
FLATTR_USERNAME = 'sputnikus'
USE_OPEN_GRAPH = True

TAGLINE = "Living, hacking, noting"
COVER_IMG_URL = "https://i.imgur.com/yydnt.jpg"

SOCIAL = (
    ('twitter-square', 'https://twitter.com/sputnikus'),
    ('github-square', 'https://github.com/sputnikus'),
    ('linkedin-square', 'https://www.linkedin.com/in/mputniorz'),
)

MENUITEMS = (
    ('About', 'pages/about'),
    ('Contact', 'pages/contact-me'),
)

DEFAULT_METADATA = (
    ('about_author', 'Standing and hacking my way to antifragility. Coffee and beer aficionado.<br>I can be wrong.'),
)
