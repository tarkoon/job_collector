from itemloaders.processors import TakeFirst, Identity, MapCompose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class IndeedLoader(ItemLoader):
    default_output_processor = TakeFirst()

    company_in = MapCompose(remove_tags, str.strip)
    text_out = Identity()
