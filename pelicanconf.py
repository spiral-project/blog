#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'The spiral project'
SITENAME = u'Daybed'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social widget
SOCIAL = (('Github', 'https://github.com/spiral-project'),)

DEFAULT_PAGINATION = False

THEME = "pure"

TAGLINE = u"Validation and storage as a service"
COVER_IMG_URL = '/theme/sidebar.jpg'

SOCIAL = (
    ('envelope', 'http://librelist.com/browser/daybed.dev/'),
    ('rss', '/feeds/all.atom.xml'),
    ('github', 'https://github.com/spiral-project'),
)
MENUITEMS = (
('Archives', '/archives.html'),
)
STATIC_PATHS = ['images', 'documents', 'extra/CNAME', 'presentations']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'}}
