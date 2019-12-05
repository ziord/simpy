from enum import Enum
from collections import namedtuple

class TokenType(Enum):
    PLUS = '+'
    MINUS = '-'
    DIV = '/'
    MULT = '*'
    MOD = '%'
    LPAREN = '('
    RPAREN = ')'
    NUMBER = 'NUMBER'
    EOF = None
    ERR = 'ERR'

Token = namedtuple("Token", ["type", "line_no", "value"])

def makeToken(type, line, value):
    return Token(type, line, value)

class Lexer:
    def __init__(self, src):
        self._line_no = 1
        self._pos = 0
        self._src = src
        self._current_char = src[self._pos]

    def advance(self):
        if self._current_char == '\n':
            self._line_no += 1
        self._pos += 1
        if self._pos > (len(self._src)-1):
            self._current_char = None
            return makeToken(TokenType.EOF, self._line_no, TokenType.EOF.value)
        else:
            self._current_char = self._src[self._pos]

            

    def skip_whitespace(self):
        while self._current_char and self._current_char.isspace():
            self.advance()

    def peek(self):
        ind = self._pos + 1
        if  ind > len(self._src) - 1:
            return ''
        return self._src[ind]

    def num(self):
        num_ = self._current_char
        self.advance()
        while self._current_char is not None and self._current_char.isdigit() :
            num_ += self._current_char
            self.advance()
        pk = self.peek()
        if self._current_char == '.' and (pk.isdigit() or pk.isspace() or pk == ''):
            num_ += self._current_char
            self.advance()
            while self._current_char is not None and self._current_char.isdigit() :
                num_ += self._current_char
                self.advance()
        return float(num_)

    def getToken(self):
        self.skip_whitespace()
        tok = self._current_char
        #if not tok:
        if tok and tok.isdigit():
            return makeToken(TokenType.NUMBER, self._line_no, self.num())
        try:
            type = TokenType(tok)
            self.advance()
            return makeToken(type, self._line_no, type.value)
        except Exception:
            return makeToken(TokenType.ERR, self._line_no, tok)
        


