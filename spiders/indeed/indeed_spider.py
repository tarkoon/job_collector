from scrapy import Spider
from spiders.indeed.indeed_items import IndeedItems
from itertools import product
from urllib.parse import urlencode
from urllib.request import Request
from spiders.indeed.indeed_loader import IndeedLoader


def url_validator(func):
    """Extra protection to make sure I only scrap Indeed"""

    def wrapper(*args, **kwargs):
        base_url = args[0].base_url
        if Request(args[1].url).host in base_url:
            return func(*args, **kwargs)

    return wrapper


class IndeedSpider(Spider):
    name = "indeed-spider"

    def __init__(self, config):
        """
        Args:
            config: Main Config File for Spider
        """

        self.config = config

        self.base_url = "https://www.indeed.com"
        self.sub_keywords = self.config.SUB_KEYWORDS

        self.allowed_domains = ["indeed.com"]
        self.start_urls = self.__build_start_urls(
            base_query=(self.base_url + "/jobs?"),
            locations=self.config.LOCATIONS,
            keywords=self.config.SEARCH_KEYWORDS,
            radius=self.config.RADIUS,
        )

        self.item_total = 0

        super().__init__()

    @url_validator
    def parse(self, response, **kwargs):

        jobs = response.xpath(
            "//div[contains(@class, 'jobsearch-SerpJobCard unified')]"
        )
        for job in jobs:
            loader = IndeedLoader(item=IndeedItems(), selector=job)

            loader.add_xpath("company", ".//span[@class='company']")
            url = job.xpath(".//h2/a/@href").get()

            yield response.follow(
                url,
                callback=self.parse_job_page,
                meta={"company": None, "item": loader.load_item()},
            )

        next_page = response.xpath("//li/a[contains(@aria-label, 'Next')]/@href").get()
        if next_page:
            yield response.follow(next_page)

    @url_validator
    def parse_job_page(self, response, **kwargs):

        loader = IndeedLoader(item=response.meta.get("item"), response=response)

        loader.add_xpath("title", "//h1/text()")
        loader.add_xpath(
            "location",
            "//div[contains(@class, 'jobsearch-InlineCompanyRating')]/div[last()]/text()",
        )
        loader.add_xpath(
            "salary",
            "//div[@id='jobDetailsSection']//div[text()='Salary']/following-sibling::span/text()",
        )

        loader.add_xpath("text", "//div[@id='jobDescriptionText']//text()")
        loader.add_value("url", response.url)

        yield loader.load_item()

    @staticmethod
    def __build_start_urls(base_query, locations, keywords, radius) -> list:
        """Builds start urls

        Builds a list of start urls based on the parameters passed in.
        If keywords is None, then exclude it from the search query.

        Returns:
            A list of unique urls, properly encoded for the purpose of
            scraping.
        """

        if not keywords:
            return [
                base_query + urlencode({"l": location, "radius": radius}, safe=",")
                for location in locations
            ]

        # Each product iteration returns a (keyword, location) tuple
        return [
            base_query
            + urlencode({"q": keyword, "l": location, "radius": radius}, safe=",")
            for keyword, location in product(keywords, locations)
        ]
