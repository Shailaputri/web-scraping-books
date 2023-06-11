# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def serialize_price(value):
    #to process any data
    return f'$ {str(value)}'


class BookItem(scrapy.Item):
    #has the same items we parsed in bookspider.py
    #we will this by importing in bookspider.

    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    # price_excl_tax = scrapy.Field(serializer = serialize_price)
    #we can do some processing here or directly in pipelines
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()


    
   
