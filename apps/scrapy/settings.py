BOT_NAME = "everydaybrazil"
SPIDER_MODULES = ["apps.scrapy.spiders"]
ITEM_PIPELINES = {
    "apps.scrapy.pipelines.EverydayBrazilPipeline": 100,
}
DOWNLOAD_DELAY = 1
ROBOTSTXT_OBEY = True
