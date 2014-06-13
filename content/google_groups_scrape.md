Title: How to scrape Google Groups
Date: 2014-06-13
Category: Tech
Tags: scraping, python
Slug: google_groups_scrape
Author: Martin Putniorz
Summary: When there's no API

Recently I wanted to get some data out of our [django-cs](https://groups.google.com/forum/#!forum/django-cs) group's front page (specificaly last month threads). But you know Google - if they have an API to something, it's often barely usable. It turned out Groups API exist. But only if you are using Google Groups in paid Google Apps, which is not my case. Time to bring out the power tools.

## First try

Classic, kind of conservative approach, is to use library like BeautifulSoup or lxml, load the HTML, serialize values and get out. 

```python
    >>> from lxml.html import parse
    >>> GOOGLE_GROUP_BASE = 'https://groups.google.com/forum/'
    >>> GOOGLE_GROUP_URL = GOOGLE_GROUP_BASE + '#!forum/{}'
    >>> group_url = GOOGLE_GROUP_URL.format('django-cs')
    >>> frontpage = parse(group_url).getroot()
    >>> frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
    >>> html_threads = frontpage.xpath('//div[@class="GIEUOX-DEQ"]')
    >>> threads = (thread_to_dict(thread) for thread in html_threads)
```

As you can see, nothing out of ordinary. I'm using lmxl just because I like it more than BeautifulSoup[^1]. Also notice the very spot-on class name of for thread ```div```. Serialization function ```thread_to_dict``` will be explained in a moment. Now what do you think ```threads``` generator is going to yield? The answer is nothing. Why? Because of JS rendering. 

## Second try

If page is JS rendered, the best way is obviously to let it render in browser. Here comes project [selenium](http://docs.seleniumhq.org/), which is mostly used for automated frontend testing and comes with couple of what they call webdrivers. You can choose between Chrome, Firefox or PhantomJS. I've chosen PhantomJS, because it's designed to run headless and quite speedy. Only problem is that you have to install it [separately](http://phantomjs.org/download.html). So, let's try again.

```python
    >>> import time
    >>> from lmxl import fromstring
    >>> from selenium import webdriver
    >>> browser = webdriver.PhantomJS()
    >>> browser.set_window_size(1024, 768)
    >>> browser.get(group_url)
    >>> time.sleep(5)
    >>> frontpage = fromstring(browser.page_source)
    >>> browser.quit()
    >>> frontpage.make_links_absolute(GOOGLE_GROUP_BASE)
    >>> html_threads = frontpage.xpath('//div[@class="GIEUOX-DEQ"]')
    >>> threads = (thread_to_dict(thread) for thread in html_threads)
```

A little bit more code but nothing dramatic. ```browser``` contains initialized PhantomJS instance with specified window site (this is usable when site is doing redirect to mobile version). We get the URL and then we pause[^2] for 5 seconds (random integer between 4 and 6). After that it's basically same (don't forget to close ```browser```). Generator now yields desired dicts.

## Serialization

```python
def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].text}
    parsed['url'] = thread.xpath('.//a[@class="GIEUOX-DPL"]')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@class="GIEUOX-DOQ"]/span'
        )[0].attrib['title']
    last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//span[@class="GIEUOX-DOQ"]')
    parsed['seen'] = int(info[1].text.split()[0])
    parsed['posts'] = int(info[0].text.split()[0])
    return parsed
```

For getting those crazy classes, browser developer tools are your friends. Date parsing is a bit pain in the ass. Either you can get *day. short_month* format or some full hybrid in ```title``` that with my Czech locale yielded something like ```středa, 11. června 2014 17:57:36 UTC+2``` (this is **not** ```strptime %c``` format!) so I just wrote a simple date parser for it. Info part is later used for thread scoring.

## No animals harmed

As you can see, even without the official API, getting some basic data from Google is pretty straightforward. If you want to see the full source code, head to the [newschimp](https://github.com/sputnikus/newschimp/blob/master/social/gg.py) project. Pull requests are welcome. Also, unofficial Groups API is a great idea.

[^1]: They are both really useful, I just enjoy using lxml more. Ian Bicking [sumed it](http://www.ianbicking.org/blog/2008/12/lxml-an-underappreciated-web-scraping-library.html) nicely.  
[^2]: JS needs some time to render (when scraping Google Groups, the longer you sleep the more threads are going to render)