import time

from datetime import datetime
from src.db_ops import DB
from src.config import BaseConfig as Config
from src.scraper import WebScraper

"""

Main file for running the scraper

"""

if __name__ == "__main__":

    start_time = time.time()

    scraper = WebScraper()
    scraper.run()

    elapsed_time = time.time() - start_time

    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    fail_count = scraper.fail_count
    success_count = scraper.success_count

    db = DB(Config.DB_NAME, Config.STATS_COLLECTION)
    db.insert({"date": date,
               "elapsed_time": elapsed_time,
               "count": fail_count + success_count,
               "fail_count": fail_count,
               "success_count": success_count})
