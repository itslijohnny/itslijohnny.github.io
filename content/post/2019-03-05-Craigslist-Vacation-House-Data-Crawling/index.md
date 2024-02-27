---
title: Craigslist Vacation House Data Crawling
date: 2019-02-12T01:13:34-08:00 
description: The is a tutorial of using Scrayp to get collect data from Craigslist.com. 
categories: 
    - Python
    - Tutorial

tags:
    - Python
    - Crawling
    - Scrapy
    - Tutorial
    - HTML

image: 5cd7d789264a1.jpg
---

In this [tutorial](https://github.com/itslijohnny/web-crawler-tutorial/tree/master/scrapy_craigslist) I use [Scrapy](https://scrapy.org/) to collect data from Craigslist.com. Specifically, the data under craigslist.org/Seattle/housing/vacation rentals. You can find the page under the link: [https://seattle.craigslist.org/d/vacation‐rentals/search/vac](https://seattle.craigslist.org/d/vacation‐rentals/search/vac)
<!--more-->
In the example, I collected following information:
1. Title
2. Posted Date
3. Rental Price
4. Number of bedrooms
5. Neighborhood
6. Description

> For more information or the code, please go to my [github page](https://github.com/itslijohnny/web-crawler-tutorial/tree/master/scrapy_craigslist).

## PREPARATION
### INSTALLATION

You can install scrapy through ```pip install``` command:
```bash
$ pip install scrapy
```
or use ```conda install``` command:
```bash
$ conda install scrapy
```
### CREAT PROJECT
Before we start coding, we can use ```scrapy startproject``` command to quickly create a project.
In terminal or CMD, navigate to your desired folder and execute following command:
```bash
$ scrapy startproject scrapy_craigslist
```
Here *scrapy_craigslist* is the name of the project.

After that, we can use ```genspider``` command to create a Scrapy Spider. Here, we name it vacation_rentals and designated a URL. We user craiglist.org Seattle vacation house list page as an example.

```bash
$ scrapy genspider vacation_rentals seattle.craigslist.org/d/vacation‐rentals/search/vac
```

This will create a directory with the following structure:

```
─── scrapy_craigslist
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-36.pyc
    │   └── settings.cpython-36.pyc
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-36.pyc
        │   └── vacation_rentals.cpython-36.pyc
        └── vacation_rentals.py
```

## EDITING

Navigate to the spiders folder and open the spider py file in your favorite editor.
There are some pre written code, but you need to make sure that ```allowed_domains``` and ```start_urls``` are in the right form.

```python
import scrapy

class CarSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://seattle.craigslist.org/d/vacation‐rentals/search/vac/']

    def parse(self, response):
        pass

```
Let's write our own code under ```def parse(self, response):```. You can check the code [here](https://github.com/itslijohnny/web-crawler-tutorial/blob/master/scrapy_craigslist/scrapy_craigslist/spiders/vacation_rentals.py).

```python
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re


class VacationRentalsSpider(scrapy.Spider):
    name = 'vacation_rentals'
    allowed_domains = ['craigslist.org']
    start_urls = ['http://seattle.craigslist.org/d/vacation‐rentals/search/vac/']

    def parse(self, response):
        # Extract all wrapper for each list item between <p class="result-info"></p>
        vacs = response.xpath('//p[@class="result-info"]')
        # Get next page button URL <a href="/search/vac?s=120" class="button next" title="next page">next &gt; </a>
        next_rel_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        # Get full address.
        next_url = response.urljoin(next_rel_url)
        # Go through all the pages.
        yield Request(next_url, callback=self.parse)

        # Loop each item to extract title, posted date, rental price, number of bedrooms, and neighborhood
        for vac in vacs:
            # Get title from <a></a> tag.
            title = vac.xpath('a/text()').extract_first()
            # Get posted date from <time class="result-date" datetime="2019-03-06 18:34" title="Wed 06 Mar 06:34:28 PM">Mar  6</time> block. Use @datetime for attribute datetime.
            pdate = vac.xpath('time/@datetime').extract_first().split()[0]
            # Get rental price form <span class="result-price">$84</span>
            rprice = vac.xpath('span/span[@class="result-price"]/text()').extract_first()
            # Get Number of bedrooms from <span class="housing">2br - 760ft<sup>2</sup> - </span> and clean up the extra
            nbedroom = str(vac.xpath('span/span[@class="housing"]/text()').extract_first()).split('-')[0].strip()
            # Get Neighborhood from <span class="result-hood"> (*** - *****)</span>
            hood = re.sub('[()]', '', str(vac.xpath('span/span[@class="result-hood"]/text()').extract_first())).strip()
            # Get the address of description page of each vacation house.
            vacaddress = vac.xpath('a/@href').extract_first()
            # We needed open the URL of each house and scrape the house description, while passing the meta to parse_page function.
            yield Request(vacaddress, callback=self.parse_page, meta={'URL': vacaddress, 'Title': title, 'Posted Date':pdate,"Rental Price":rprice,"Number of bedrooms":nbedroom, "Neighborhood":hood})

    # Extract description page of the vacation house.
    def parse_page(self, response):
        # Pass the variables
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        pdate = response.meta.get('Posted Date')
        rprice = response.meta.get('Rental Price')
        nbedroom = response.meta.get('Number of bedrooms')
        hood = response.meta.get('Neighborhood')
        # Get the description.
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        yield{'Title': title, 'Posted Date':pdate,"Rental Price":rprice,"Number of bedrooms":nbedroom, "Neighborhood":hood,'Description':description}

```

### RUN SPIDER
To put our spider to work, run ```crawl``` command in terminal or CMD:
```bash
$ scrapy crawl vacation_rentals -o result-titles.csv
```
```-o``` means out put data into file. ```result-titles.csv``` is the files' name.