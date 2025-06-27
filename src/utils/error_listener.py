from antlr4.error.ErrorListener import ConsoleErrorListener

class SyntaxException(Exception):
    def __init__(self, msg):
        self.message = msg
        super().__init__(msg)

class NewErrorListener(ConsoleErrorListener):
    INSTANCE = None

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        text = getattr(offendingSymbol, 'text', str(offendingSymbol))
        raise SyntaxException(f"Error on line {line} col {column}: {text}")

NewErrorListener.INSTANCE = NewErrorListener()
