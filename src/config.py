class BaseConfig:
    """
    Base configuration
    """
    APP_NAME = "Turkish Network Times Scraper"
    APP_VERSION = "0.0.1"

    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    PYMONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
    DB_NAME = "haktan_ozer"
    NEWS_COLLECTION = "news"
    STATS_COLLECTION = "stats"
    WORD_FREQUENCY_COLLECTION = "word_frequency"
