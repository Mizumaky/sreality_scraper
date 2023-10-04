FROM python:3.11

WORKDIR /usr/src/sreality_scraper/sscraper

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["scrapy", "crawl", "sreality"]