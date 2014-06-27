Title: Better Google Group scraper
Date: 2014-06-27
Category: Tech
Tags: scraping, python
Slug: google_groups_scrape_again
Author: Martin Putniorz
Summary: When you can't depend on class anymore

In [previous article]({filename}/google_groups_scrape.md) about Google Group scraping I've demonstrated very minimal script to get basic informations about group threads. It turns out class based approach doesn't work so well, because JavaScript frontend of Groups is not consistent in class naming. I fixed my scripts and now I'm going to show you, what I've changed.

## Third try

Since we can't use classes for XPath, we need to search for another leads. Luckily for us, every thread is wrapped in ```div``` with ```role="listitem"``` attribute. So after this little change, our thread extractor looks like this.

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
    >>> html_threads = frontpage.xpath('//div[@role="listitem"]')
    >>> threads = (thread_to_dict(thread) for thread in html_threads)
```

## Serialization (almost classless)

Even serialization script relied heavily on classes. Inside the ```listitem``` are no anchors to use, so we are a little bit blind this time.

```python
def thread_to_dict(thread):
    parsed = {'name': thread.xpath('.//a')[0].text}
    parsed['url'] = thread.xpath('.//a')[0].attrib['href']
    raw_last_change = thread.xpath('.//span[@title]'
        )[0].attrib['title']
    last_change = date_parse(raw_last_change)
    parsed['month'] = last_change.month
    info = thread.xpath('.//div[contains(@style,"right")]')[0]
    parsed['seen'] = int(info.xpath('.//span[@class]')[3].text.split()[0])
    parsed['posts'] = int(info.xpath('.//span[@class]')[4].text.split()[0])
    return parsed
```

First link in the thread contains name and of course address. Then we search for ```span``` with ```title``` attribute. That's a time of the last change. Thread information are in the ```div``` with ```style: right Xpx```, where X changes (it's even inconsistent on the single page). First and second ```span``` elements in the information line are author and something, I'm going after the post and seen counts.

## Beyond scraping

Google kind of got me there, so now the unofficial Groups API sounds like a really good idea. Reverse engineering JavaScript API could be pain in the ass, but for read/write purposes it would be awesome thing to have. 