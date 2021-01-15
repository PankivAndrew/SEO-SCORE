import spacy
from spacy.matcher import Matcher

from src.scorer.decorators import decorate_all_methods, ErrorDefender


@decorate_all_methods(ErrorDefender)
class Appraiser:

    def __init__(self, config, primary_keywords, secondary_keywords):
        self.config = config
        self.final_score = 0.0
        self.nlp = None
        self.matcher = None
        self.primary_keywords = primary_keywords
        self.secondary_keywords = secondary_keywords
        self.__configure()

    def score(self, seo_text, h1, h2):
        self.__add_words_to_matcher(self.primary_keywords)
        self.final_score += self.calculate_first_rule(h1, h2)
        self.final_score += self.calculate_second_rule(seo_text)
        return self.final_score

    def calculate_first_rule(self, h1, h2):
        h1_doc = self.nlp(h1)

        h1_matches = self.matcher(h1_doc)
        if len(h1_matches) > 0:
            return self.config.FIRST_RULE_WEIGHT

        h2_doc = self.nlp(h2)

        h2_matches = self.matcher(h2_doc)
        if len(h2_matches) > 0:
            return self.config.FIRST_RULE_WEIGHT

        return 0.0

    def calculate_second_rule(self, text):
        first_two_sentences = ''.join(sentence for sentence in text.split('.')[:2])

        first_two_sentences_doc = self.nlp(first_two_sentences)

        first_two_sentences_matches = self.matcher(first_two_sentences_doc)
        if len(first_two_sentences_matches) > 0:
            return self.config.SECOND_RULE_WEIGHT
        return 0.0

    def calculate_third_rule(self, text):
        pass

    def __configure(self):
        self.nlp = spacy.load(f'{self.config.LANGUAGE}_core_web_sm')
        self.matcher = Matcher(self.nlp.vocab)

    def __add_words_to_matcher(self, keywords_list):
        for keywords in keywords_list:
            pattern = []
            keywords = keywords.split(' ')
            for i, word in enumerate(keywords):
                pattern.append({'LEMMA': word})
                if i != len(keywords) - 1:
                    pattern.append({'IS_ALPHA': True, 'OP': '*'})
            self.matcher.add('+'.join(word for word in keywords), None, pattern)
