import re
import usaddress
from scrapy.exceptions import DropItem
from utilities import encode_currency
from urllib.parse import urlparse, parse_qs


class IndeedPipeLine:
    def open_spider(self, spider):
        self.ITEM_LIMIT = spider.config.ITEM_LIMIT
        self.SUB_KEYWORDS = spider.config.SUB_KEYWORDS

    def process_item(self, item, spider):

        if spider.item_total >= self.ITEM_LIMIT != 0:
            raise DropItem

        url = item.get("url")
        job_id = parse_qs(urlparse(url).query).get("jk")
        item["url"] = f"https://www.indeed.com/viewjob?jk={job_id[0]}"

        # TODO Optimize Code
        match = 0

        text = "".join(item.get("text"))
        found_keywords = []
        for keyword in self.SUB_KEYWORDS:
            pattern = re.compile(rf"\b({keyword})\b", flags=re.IGNORECASE)
            if pattern.search(text):
                found_keywords.append(keyword)
                match += 1
        if self.SUB_KEYWORDS:
            item["match"] = f"{round((match / len(self.SUB_KEYWORDS)) * 100, 2)}%"
            item["keywords"] = " - ".join(found_keywords)

        salary = item.get("salary")
        if salary:
            item = self.__parse_salary(item, salary)

        location = item.get("location")
        if location:
            item = self.__parse_location(item, location)

        spider.item_total += 1
        return item

    @staticmethod
    def __parse_salary(item, salary):
        pattern = re.compile(r"\$\s?\d+(,\d+)?(.\d+)?")

        salary_group = [
            float(match.replace("$", "").replace(",", ""))
            for match in [match.group() for match in pattern.finditer(salary)]
        ]

        if "hour" in salary.lower():
            item["pay_type"] = "Hourly"
        if "week" in salary.lower():
            item["pay_type"] = "Weekly"
        if "year" in salary.lower():
            item["pay_type"] = "Yearly"

        if len(salary_group) == 1:
            item["min_pay"] = encode_currency(salary_group[0])
        if len(salary_group) == 2:
            item["min_pay"] = encode_currency(min(salary_group))
            item["max_pay"] = encode_currency(max(salary_group))

        return item

    @staticmethod
    def __parse_location(item, location):
        if "texas" in location.lower():
            location.replace("Texas", "Tx")
            location.replace("texas", "Tx")
        parsed_location = usaddress.tag(location)[0]

        item["city"] = parsed_location.get("PlaceName")
        item["state"] = parsed_location.get("StateName")
        item["country"] = parsed_location.get("CountryName")
        item["zip_code"] = parsed_location.get("ZipCode")

        return item
