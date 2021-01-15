import requests
import string
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from bs4 import BeautifulSoup

from src.scorer.decorators import decorate_all_methods, ErrorDefender


@decorate_all_methods(ErrorDefender)
class HTMLScrapper:

    def __init__(self, config):
        self.config = config

    def scrap(self, url):
        html = self.get_html(url)
        if isinstance(html, dict):
            return

        text = self.get_text(html)
        if isinstance(text, dict):
            return
        return text

    def translate_text(self, text, target_lang, source_lang='en'):
        resp = requests.post(self.config.TRANSLATE_URL,
                             json={
                                 'description': text,
                                 'title': 'seo-score',
                                 'source_locale': source_lang,
                                 'target_locale': target_lang
                             })
        if resp.status_code != 200:
            raise Exception('Can`t translate text')
        return resp.json().get('description')

    def get_text(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        seo_text_description = soup.find("div", {"id": "seo-text-description"})
        if seo_text_description is None:
            raise Exception("Can`t find seo description div")

        heading_divs = seo_text_description.findAll('h2')
        if len(heading_divs) >= 2:
            return self.clean_text(seo_text_description.text.lower()),\
                   self.clean_text(heading_divs[0].text.lower()),\
                   self.clean_text(heading_divs[1].text.lower())
        raise Exception("Can`t find heading divs")

    @staticmethod
    def get_html(url):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.get(url)
        accept_cookies_div = browser.find_elements_by_class_name('js-cookies-not-accepted')
        if len(accept_cookies_div) != 0:
            accept_cookies_div = accept_cookies_div[0]
            accept_cookies_button = accept_cookies_div.find_element_by_class_name('cookie-consent-confirm-box')
            accept_cookies_button.click()
        html = browser.page_source
        browser.quit()
        return html

    @staticmethod
    def clean_text(text):
        return ''.join(char for char in text if char not in string.punctuation)
