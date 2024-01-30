import requests

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from src.tools import BaseLogger, GetData
from src.db_ops import DB
from src.config import BaseConfig as Config


class WebScraper:
    """
    This class scrapes data from turkishnetworktimes.com and saves to MongoDB database
    """

    def __init__(self):
        self.db = DB(Config.DB_NAME, Config.NEWS_COLLECTION)
        self.session = requests.Session()
        self.fail_count = 0
        self.success_count = 0
        self.already_exists_count = 0

    @staticmethod
    def all_new_pages():
        """
        This method generates all new pages
        :return: Yields new page url
        """
        for page_number in range(1, 50):
            url = f"https://turkishnetworktimes.com/kategori/gundem/page/{page_number}/"
            yield url

    def all_new_urls_from_page(self, new_page):
        """
        This method generates all new urls from new page
        :param new_page:
        :return: Yields new url
        """
        response = self.session.get(new_page)
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.select("div.haber-post a"):
            yield link.get("href")

    def get_data_from_new_page(self, new_page):
        """
        This method gets data from new page
        :param new_page:
        :return: Dict of data
        """
        try:
            response = self.session.get(new_page)
            BaseLogger.logger.info(f"Getting data from {new_page}")
            self.success_count += 1
        except Exception as e:
            BaseLogger.logger.error(f"{e} error in {new_page}")
            self.fail_count += 1
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        get_data = GetData(new_page, soup)

        result = {"url": new_page,
                  "header": get_data.get_header(),
                  "summary": get_data.get_summary(),
                  "text": get_data.get_text(),
                  "img_url_list": get_data.get_img_url_list(),
                  "publish_date": get_data.get_publish_date(),
                  "update_date": get_data.get_update_date()}
        return result

    def save_data(self, data):
        """
        This method saves data to database
        :param data:
        :return:
        """
        self.db.insert(data)
        BaseLogger.logger.info(f"Data saved successfully to collection->: {Config.NEWS_COLLECTION}")

    def run(self):
        """
        This method runs all methods in this class,
        Check data is exists in database,
        if not exists, get data from new page and save to database,
        using ThreadPoolExecutor because of performance.
        """

        with ThreadPoolExecutor(max_workers=10) as executor:
            for new_page in self.all_new_pages():
                for new_url in self.all_new_urls_from_page(new_page):

                    if self.db.find({"url": new_url}) is not None:
                        BaseLogger.logger.info(f"Data already exists in database->: {new_url}")
                        self.already_exists_count += 1
                        continue

                    future = executor.submit(self.get_data_from_new_page, new_url)
                    result = future.result()
                    self.save_data(result)
