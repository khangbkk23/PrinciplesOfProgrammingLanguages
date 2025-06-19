import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'build'))

from antlr4 import *
from build.HLangLexer import HLangLexer
from build.HLangParser import HLangParser


class Tokenizer:
    def __init__(self, input_string):
        self.input_stream = InputStream(input_string)
        self.lexer = HLangLexer(self.input_stream)

    def get_tokens(self):
        tokens = []
        token = self.lexer.nextToken()
        while token.type != Token.EOF:
            tokens.append(token.text)
            try:
                token = self.lexer.nextToken()
            except Exception as e:
                tokens.append(str(e))
                return tokens
        return tokens + ["EOF"]

    def get_tokens_as_string(self):
        tokens = []
        token = self.lexer.nextToken()
        while token.type != Token.EOF:
            tokens.append(token.text)
            try:
                token = self.lexer.nextToken()
            except Exception as e:
                tokens.append(str(e))
                return ",".join(tokens)
        return ",".join(tokens + ["EOF"])


class Parser:
    def __init__(self, input_string):
        self.input_stream = InputStream(input_string)
        self.lexer = HLangLexer(self.input_stream)
        self.token_stream = CommonTokenStream(self.lexer)
        self.parser = HLangParser(self.token_stream)

    def parse(self):
        try:
            self.parser.program()  # Assuming 'program' is the entry point of your grammar
            return "success"
        except Exception as e:
            return str(e)
