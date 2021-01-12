import spacy
from spacy.matcher import Matcher

from src.scorer.decorators import decorate_all_methods, ErrorDefender


@decorate_all_methods(ErrorDefender)
class Appraiser:

    def __init__(self, config):
        self.config = config
        self.nlp = None
        self.matcher = None
        self.__configure()

    def score(self, text):
        doc = self.nlp(text)

    def calculate_first_rule(self, text):
        pass

    def calculate_second_rule(self, text):
        pass

    def calculate_third_rule(self, text):
        pass

    def __configure(self):
        self.nlp = spacy.load(f'{self.config.LANGUAGE}_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)
