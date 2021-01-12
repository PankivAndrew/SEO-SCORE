from os import getenv
from dotenv import load_dotenv

load_dotenv()


class ParserConfigs:
    TRANSLATE_URL = getenv('TRANSLATE_URL')


class ProcessorConfigs:
    LANGUAGE = 'en'
    FIRST_RULE_WEIGHT = float(getenv('FIRST_RULE_WEIGHT', 0.3))
    SECOND_RULE_WEIGHT = float(getenv('SECOND_RULE_WEIGHT', 0.3))
    THIRD_RULE_WEIGHT = float(getenv('THIRD_RULE_WEIGHT', 0.4))
