import logging
import pymongo
import os

from bs4 import BeautifulSoup
from src.config import BaseConfig as Config
from typing import List


class BaseLogger:
    """
    Base class for logger
    stream_handler: logging.StreamHandler
    file_handler: logging.FileHandler
    """
    current_directory = os.getcwd()
    log_file_path = os.path.join(current_directory, 'logs.log')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


class GetData:
    """
    This class gets data from soup object
    """
    def __init__(self, url: str, soup: BeautifulSoup):
        self.url = url
        self.soup = soup

    def get_header(self) -> str or None:
        try:
            header = self.soup.select_one("h1.single_title").get_text(strip=True)
            return header
        except AttributeError:
            BaseLogger.logger.error(f"Header not found in {self.url}")
            return None

    def get_summary(self) -> str or None:
        try:
            summary = self.soup.select_one("h2.single_excerpt p").get_text(strip=True)
            return summary
        except AttributeError:
            BaseLogger.logger.error(f"Summary not found in {self.url}")
            return None

    def get_text(self) -> str or None:
        try:
            text = self.soup.select_one("div.yazi_icerik").get_text(strip=True)
            return text
        except AttributeError:
            BaseLogger.logger.error(f"Text not found in {self.url}")
            return None

    def get_img_url_list(self) -> List[str] or None:
        try:
            img_url_list = []
            for img in self.soup.select("div.post_line img"):
                img_url_list.append(img.get("data-src"))
            return img_url_list
        except AttributeError:
            BaseLogger.logger.error(f"Image not found in {self.url}")
            return None

    def get_publish_date(self) -> str or None:
        try:
            publish_date_tag = self.soup.select("span.tarih time")[0]
            publish_date_raw = publish_date_tag.get("datetime")
            publish_date = date_control(publish_date_raw)
            return publish_date
        except AttributeError:
            BaseLogger.logger.error(f"Publish date not found in {self.url}")
            return None

    def get_update_date(self) -> str or None:
        try:
            update_date_tag = self.soup.select("span.tarih time")[1]
            update_date_raw = update_date_tag.get("datetime")
            update_date = date_control(update_date_raw)
            return update_date
        except AttributeError:
            BaseLogger.logger.error(f"Update date not found in {self.url}")
            return None


def date_control(date: str) -> str:
    """
    this function checks if the date is in the correct format
    example: 2021-1-1 to -> 2021-01-01

    :param date: date in string format
    :return: date in string format
    """
    split_t = date.split("T")[0]
    split_date = split_t.split("-")
    for index, number in enumerate(split_date):
        if len(number) < 2:
            split_date[index] = f"0{number}"
    return "-".join(split_date)


def connect_to_mongo() -> pymongo.MongoClient:
    """
    this function connects to mongo database for testing
    :return: client object from pymongo
    """
    try:
        client = pymongo.MongoClient(Config.PYMONGO_URI)
        BaseLogger.logger.info("Connected to database")
        return client
    except Exception as e:
        BaseLogger.logger.error(f"{e} error while connecting to database")
