import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    #to prevent our spider to crawl into hyperlinks and scrape entire internet
    start_urls = ["https://books.toscrape.com"]

    #any custom settings in spider file overrides that is settings.py file
    custom_settings = {

        'FEEDS' : {
        'booksdata_spiderdefault.json' : {'format':'json', 'overwrite':True},
        }
    }

    def parse(self, response):
        #we get the name of this css by going to website and inspecting element
        books = response.css('article.product_pod')
        
        for book in books:
            #we need to get to the link of every book to get all its details
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)
            
            '''
            #PrevCode : The following code was to get just name,price and url from each book.
            yield{
                #here text refers to the exact text mentioned on page
                #for href we have to do attrib
                'name' : book.css('h3 a::text').get(),
                'price' : book.css('.product_price .price_color::text').get(), 
                #this space between price and dot is imp!!
                'url' : book.css('h3 a').attrib['href'],
            }
            '''

        #the above attrib['href'] returns HTML link. The below attr(href) returns jQuery object which
        #may be the entire link or a part of it.

        next_page = response.css('li.next a ::attr(href)').get()


        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback= self.parse)

    def parse_book_page(self, response):
        #fill with CSS selectors and xpath selectors. Use shell for trial and error.
        table_rows = response.css("table tr")
        
        # yield {
        #     'url' : response.url,
        #     'title' : response.css('.product_main h1::text').get(),
        #     'product_type': table_rows[1].css("td ::text").get(),
        #     'price_excl_tax': table_rows[2].css("td ::text").get(),
        #     'price_incl_tax': table_rows[3].css("td ::text").get(),
        #     'tax': table_rows[4].css("td ::text").get(),
        #     'availability': table_rows[5].css("td ::text").get(),
        #     'num_reviews': table_rows[6].css("td ::text").get(),
        #     'stars' : response.css("p.star-rating").attrib['class'],
        #     'category' : response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        #     'description' : response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        #     'price': response.css('p.price_color ::text').get(),
        # }

        #we will create an object of bookitem class and use that
        book_item = BookItem()

    
        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type' ] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews']=  table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),
    
        yield book_item


