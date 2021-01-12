import requests
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

    @staticmethod
    def get_text(content):
        soup = BeautifulSoup(content, 'html.parser')

        description_div = soup.find("div", {"id": "description"})
        if description_div is None:
            raise Exception("Can`t find description div")

        content_div = description_div.find("div", {"class": "localized-desc__content"})
        if content_div is None:
            raise Exception("Can`t find description localized content")

        text_div = content_div.find("div", {"class": "localized-desc__description-text"})
        if text_div is None:
            raise Exception("Can`t find text")
        return text_div.text

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
        load_more_div = browser.find_elements_by_class_name('localized-desc__original_desc_read_more')
        if len(load_more_div) != 0:
            load_more_div = load_more_div[0]
            load_more_a = load_more_div.find_element_by_css_selector('a')
            load_more_a.click()
        html = browser.page_source
        browser.quit()
        return html

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
