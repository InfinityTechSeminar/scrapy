# Infinity Tech Seminar
[![N|Solid](https://scontent.fhan3-2.fna.fbcdn.net/v/t31.0-8/26233814_142102836486971_6888443210394746478_o.jpg?oh=a9526ff05a8cfbe1ae66194ec27180b1&oe=5ADDF5B1)](https://www.facebook.com/InfinityTechSeminar)
## Scrapy demo - crawl Stackoverflow

> This repository contain scrapy demo for website: quotes and stackoverflow.

## Install python module
```sh
pip install scrapy
pip install SQLAlchemy
pip install pymysql
pip install MySQLdb
```

## Run spider crawl data
```sh
# Run crawl stackoverflow data with LOG_LEVEl=INFO
scrapy crawl stack
# Run crawl stackoverflow data with LOG_LEVEl=DEBUG
scrapy crawl stack -L DEBUG
# Run crawl stackoverflow data with debug information
scrapy crawl stack -a debug=1

# Run crawl quotes with LOG_LEVEL=INFO
scrapy crawl quotes
# Run crawl quotes with LOG_LEVEL=DEBUG
scrapy crawl quotes -L DEBUG
# Run crawl quotes with debug information
scrapy crawl quotes -a debug=1
```
## Save data
> Lưu dữ liệu ra file json:
```sh
# Format
{
    '_file': '{file path here}',
    '_mode': '{write mode here}',
}

# Example
{
    '_file': 'storage/quotes.json',
    '_mode': 'w',
}
```

> Lưu dữ liệu vào database, thêm các trường sau vào item
```sh
{
    '_id': '{item id here}',
    '_table': '{table name}',
}
{
    '_id': '1',
    '_table': 'quotes',
}
```

> Cập nhật lại cấu hình kết nối database trong file settings.py
```sh
DATABASE = {
    'drivername': 'mysql+pymysql',
    'host': 'localhost',
    'port': '3306',
    'username': 'root',
    'password': 'root',
    'database': 'stackoverflow',
    'query': {
        'charset': 'utf8mb4',
        'use_unicode': 1
    }
}
```

> Bật item pipeline trong spider
```sh
custom_settings = {
    'ITEM_PIPELINES': {
        'crawler.extensions.orm.DatabasePipeline': 2,
    }
}
```

## Reference
- [Scrapy document](https://doc.scrapy.org/en/latest/)
- [Scrapy tutorial](https://doc.scrapy.org/en/latest/intro/tutorial.html)
- [Search more example](https://goo.gl/iWQ6vw)
- [Web scraping and crawling with Scrapy and SqlAlchemy](https://manhhomienbienthuy.bitbucket.io/2015/Dec/11/web-scraping-and-crawling-with-scrapy-and-sqlalchemy.html)
- [Advanced web scraping and crawling with Scrapy and SqlAlchemy](https://manhhomienbienthuy.bitbucket.io/2016/Jan/11/advanced-web-scraping-and-crawling-with-scrapy-and-sqlalchemy.html)

## Contact
> Email: ngoctd@ai-t.vn
> Facebook: https://www.facebook.com/InfinityTechSeminar
