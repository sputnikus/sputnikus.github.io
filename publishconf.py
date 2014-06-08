#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://sputnikus.github.io'
RELATIVE_URLS = False

FEED_ATOM = 'feeds/main.atom.xml'
FEED_RSS = 'feeds/main.xml'
CATEGORY_FEED_ATOM = None
FEED_DOMAIN = SITEURL

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "bysputnikus"
GOOGLE_UNIVERSAL_ANALYTICS = "UA-17206429-4"
