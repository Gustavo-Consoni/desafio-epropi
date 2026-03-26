import scrapy


class EverydayBrazilSpider(scrapy.Spider):
    name = "everydaybrazil"

    def __init__(self, suffix="arroz-feijao-e-graos", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://www.everydaybrazil.com/en/collections/{suffix}"]

    def parse(self, response):
        for product in response.css("li.productgrid--item"):
            try:
                yield {
                    "image": f"https:{product.css('img.productitem--image-primary::attr(src)').get()}",
                    "description": product.css("h2.productitem--title a::text").get().strip(),
                    "brand": product.css("span.productitem--vendor a::text").get().strip(),
                    "price": float(product.css("div[data-price-container] span.money::text").get().replace("$", "").replace(",", "").strip()),
                }
            except Exception as error:
                print(str(error))
                continue
