from scrapy.item import Item, Field


class IndeedItems(Item):

    title = Field()
    company = Field()

    location = Field()
    city = Field()
    state = Field()
    country = Field()
    zip_code = Field()

    salary = Field()
    min_pay = Field()
    max_pay = Field()
    pay_type = Field()

    text = Field()
    match = Field()
    keywords = Field()
    url = Field()

    def __repr__(self):

        spacing = "\n" * 2

        return (
            spacing
            + repr(
                {
                    "title": self.get("title"),
                    "company": self.get("company"),
                    "location": self.get("location"),
                    "salary": self.get("salary"),
                    "match": self.get("match"),
                    "keywords": self.get("keywords"),
                    "url": self.get("url"),
                }
            )
            + spacing
        )
