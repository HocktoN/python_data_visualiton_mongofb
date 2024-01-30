import requests

from bs4 import BeautifulSoup
from unittest import TestCase
from src.tools import GetData

"""
Test file for testing GetData class
"""


class TestGetData(TestCase):
    def setUp(self) -> None:
        self.response = requests.get("https://turkishnetworktimes.com/zeytinburnunda-tramvayin-acilan-kapagi-cami-"
                                     "patlatti/")
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.get_data = GetData("https://turkishnetworktimes.com/ttb-merkez-konseyi-davasinda-karar-aciklandi/",
                                self.soup)

    def test_get_header(self):
        expected_result = "Zeytinburnu’nda tramvayın açılan kapağı camı patlattı"
        self.assertEqual(self.get_data.get_header(), expected_result)

    def test_get_summary(self):
        expected_result = ('Olay, dün saat 16.00 sıralarında Kabataş- Bağcılar seferini yapan tramvayda meydana geldi.'
                           ' Zeytinburnu’nda ilerleyen tramvayın, alt bölümünde bulunan muhafaza kapağı açılarak'
                           ' bariyerlere çarptı. Savrulan kapak camı patlattı. Tramvay, Merkezefendi Durağında..')
        self.assertEqual(self.get_data.get_summary(), expected_result)

    def test_get_text(self):
        expected_data = ('Olay, dün saat 16.00 sıralarında Kabataş- Bağcılar seferini yapan tramvayda meydana geldi.'
                         ' Zeytinburnu’nda ilerleyen tramvayın, alt bölümünde bulunan muhafaza kapağı açılarak '
                         'bariyerlere çarptı. Savrulan kapak camı patlattı. Tramvay, Merkezefendi Durağında durdu ve'
                         ' içinde bulunan yolcular tahliye edildi. Olayda can kaybı veya yaralanma yaşanmazken '
                         'panik yaşandı.')
        self.assertEqual(self.get_data.get_text(), expected_data)

    def test_publish_date(self):
        expected_data = '2023-11-30'
        self.assertEqual(self.get_data.get_publish_date(), expected_data)

    def test_update_date(self):
        expected_data = '2023-11-30'
        self.assertEqual(self.get_data.get_update_date(), expected_data)

    def test_get_img_url_list(self):
        expected_data = ['https://turkishnetworktimes.com/wp-content/uploads/2023/11/zeytinburnunda-'
                         'tramvayin-acilan-kapagi-cami-patlatti-49081.jpg']
        self.assertEqual(self.get_data.get_img_url_list(), expected_data)
