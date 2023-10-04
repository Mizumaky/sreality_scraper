from pathlib import Path
import json
import scrapy

from sscraper.items import SscraperItem


class SrealitySpider(scrapy.Spider):
    name = "sreality"

    def start_requests(self):
        urls = [
            "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page=1",
            "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page=2",
            "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page=3",
            "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page=4",
            "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&sort=0&per_page=100&page=5",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonResponse = json.loads(response.text)
        for item in jsonResponse["_embedded"]["estates"]:
            # check item has id, name and image
            if not item["hash_id"]:
                print(f"no hash id")
                continue
            elif not item["name"]:
                print(f"no name")
                continue
            elif not item["_links"]:
                print(f"no image")
                continue
            print(f"parsing ad {item['hash_id']}")
            # # dump for debugging
            # filename = f"ads/sreality_{item['hash_id']}.json"
            # json_object = json.dumps(item, indent=4)
            # with open(filename, "w") as outfile:
            #     outfile.write(json_object)
            # create item
            adItem = SscraperItem()
            adItem["title"] = item["name"]
            adItem["image_url"] = item["_links"]["images"][0]["href"]
            yield adItem