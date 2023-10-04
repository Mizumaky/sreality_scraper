# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class SscraperPipeline:
    def __init__(self):
        print("initializing sreality scraper pipeline")
        self.dbConn = None
        self.dbCursor = None
        self.dbName = "srealitydb"
        self.dbHost = "db"
        self.dbPort = "5432"
        self.dbUser = "mizumaky"
        self.dbPassword = "secret"

    def open_spider(self, spider):
        print("opening spider")
        print("connecting to database")
        self.dbConn = psycopg2.connect(
            dbname=self.dbName,
            host=self.dbHost,
            port=self.dbPort,
            user=self.dbUser,
            password=self.dbPassword,
        )
        self.dbCursor = self.dbConn.cursor()
        print("creating table")
        self.dbCursor.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                my_id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                image_url TEXT
            )
        """)
        print("clearing table")
        self.dbCursor.execute("DELETE FROM ads")

    def close_spider(self, spider):
        print("fetching data from database")
        self.dbCursor.execute("SELECT * FROM ads")
        results = self.dbCursor.fetchall()
        print("closing database connection")
        self.dbCursor.close()
        self.dbConn.close()

        print("creating a web page")
        html = "<html><head><title>Sreality Scraper</title></head><body>"
        html += "<div style='text-align: center;'>"
        html += "<h1>Sreality Scraper</h1>"
        html += "<table style='margin: 0 auto;'>"
        html += "<tr><th>#</th><th>Title</th><th>Image URL</th></tr>"
        for row in results:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td><img src='{row[2]}' width='100'></td></tr>"
        html += "</table>"
        html += "</div>"
        html += "</body></html>"
        with open("../webserver/sreality.html", "w") as outfile:
            outfile.write(html)

    def process_item(self, item, spider):
        insert_query = f"INSERT INTO ads (title, image_url) VALUES (%s, %s)"
        data = (item['title'], item['image_url'])
        # print(f"saving item {data} to database")
        self.dbCursor.execute(insert_query, data)
        self.dbConn.commit()
        return item