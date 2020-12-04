from utilities import file_name_gen
from fake_useragent import UserAgent
from scrapy.crawler import CrawlerProcess

from spiders import IndeedSpider
from utilities.config_loader import Config

config = Config()
file_path = file_name_gen(config.FILE_NAME, config.FILE_TYPE)

process = CrawlerProcess(
    settings={
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 2.5,
        "USER_AGENT": UserAgent().random,
        "LOG_LEVEL": config.LOG_LEVEL,
        "CLOSESPIDER_ITEMCOUNT": config.ITEM_LIMIT,
        "CONCURRENT_ITEMS": 5,
        "ITEM_PIPELINES": {
            "spiders.indeed.indeed_pipeline.IndeedPipeLine": 300,
        },
        "FEEDS": {
            file_path: {
                "format": config.FILE_TYPE,
                "encoding": "utf8",
                "fields": config.HEADERS,
            }
        },
    }
)

process.crawl(IndeedSpider, config)
process.start()
