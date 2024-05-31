import pandas as pd
import scrapy
from latest_user_agents import get_random_user_agent
from scrapy.spidermiddlewares.httperror import HttpError


class BooktopiaSpider(scrapy.Spider):
    name = "booktopia"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'output.csv',
    }
    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
        'referer': 'https://www.booktopia.com.au/',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': get_random_user_agent(),
        'x-nextjs-data': '1'
    }

    def start_requests(self):
        # Read the input CSV file with ISBNs using pandas
        df = pd.read_csv('input_list.csv')    # add your input file path
        for isbn in df['ISBN13']:
            url = f'https://www.booktopia.com.au/_next/data/BiLaGwnyd3BPwc2WwI_bZ/search.json?keywords={isbn}'
            yield scrapy.Request(url, headers=self.headers, callback=self.parse_initial, meta={'isbn': isbn}, errback=self.handle_error)


    def handle_error(self, failure):
        isbn = failure.request.meta['isbn']
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 404:
                yield from self.parse_not_found_details(isbn)
        else:
            yield from self.parse_not_found_details(isbn)

    def parse_initial(self, response):
        isbn = response.meta['isbn']
        data = response.json()
        if "pageProps" in data and "__N_REDIRECT" in data['pageProps']:
            redirect_url = data['pageProps']["__N_REDIRECT"]
            full_redirect_url = f'https://www.booktopia.com.au/_next/data/BiLaGwnyd3BPwc2WwI_bZ{redirect_url}.json'
            yield scrapy.Request(full_redirect_url, headers=self.headers, callback=self.parse_details, meta={'isbn': isbn})
        else:
            yield from self.parse_not_found_details(isbn)

    def parse_details(self, response):
        isbn = response.meta['isbn']
        data = response.json()
        book_details = data['pageProps']

        if "__N_REDIRECT" in book_details:
            redirect_url = data['pageProps']["__N_REDIRECT"]
            full_redirect_url = f'https://www.booktopia.com.au/_next/data/BiLaGwnyd3BPwc2WwI_bZ{redirect_url}.json'
            yield scrapy.Request(full_redirect_url, headers=self.headers, callback=self.parse_details,
                                 meta={'isbn': isbn})

        else:
            book_details = data['pageProps']['product']
            try:
                if book_details:
                    yield {
                        'Title': book_details.get('displayName', ''),
                        'ISBN': isbn,
                        'Author':', '.join(contributor['name'] for contributor in book_details.get('contributors', [])),
                        'Book type': book_details.get('type', ''),
                        'Original Price': book_details.get('retailPrice', ''),
                        'Discounted Price': book_details.get('salePrice', ''),
                        'ISBN-10': book_details.get('isbn10', ''),
                        'Published Date': book_details.get('publicationDate', ''),
                        'Publisher': book_details.get('publisher', ''),
                        'No. of Pages': book_details.get('numberOfPages', '')
                    }
            except Exception as e:
                print('No record found!..', e)
                yield from self.parse_not_found_details(isbn)

    def parse_not_found_details(self, isbn):
        # Book not found
        yield {
            'Title': 'book not found',
            'ISBN': isbn,
            'Author': '',
            'Book type': '',
            'Original Price': '',
            'Discounted Price': '',
            'ISBN-10': '',
            'Published Date': '',
            'Publisher': '',
            'No. of Pages': ''
        }


# Run this spider using the command:
# scrapy crawl booktopia


