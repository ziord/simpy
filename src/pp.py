from lexer import *
from ast import *
from stack import *

class Precedence(Enum):
    PREC_NONE       = -1
    PREC_EXPR       = 0
    PREC_TERM       = 1
    PREC_SUP_TERM   = 2
    PREC_FACTOR     = 3
    PREC_PRIMARY    = 4

class ParseRule:
    def __init__(self, pref=None, inf=None, prec=Precedence.PREC_NONE):
        self._prefix = pref
        self._infix = inf
        self._prec = prec

class PParser:
    def __init__(self, lexer):
        self._lexer = lexer
        self.curr_tok = self._lexer.getToken()
        self.prev_tok = self.curr_tok
        self._had_error = False
        self._ast_tab = ASTTable()

    def unary(self):
        ttype = self.prev_tok.type
        tok = self.prev_tok
        self.parsePrec(Precedence.PREC_FACTOR)
        if ttype == TokenType.PLUS:
            node = UnaryOp(tok, TokenType.PLUS, self._ast_tab.pop_node())
            self._ast_tab.push_node(node)
        elif ttype == TokenType.MINUS:
            node = UnaryOp(tok, TokenType.MINUS, self._ast_tab.pop_node())
            self._ast_tab.push(node)

    def number(self):
        tok = self.prev_tok
        node = Num(tok, tok.value)
        self._ast_tab.push(node)

    def binary(self):
        ttype = self.prev_tok.type
        tok = self.prev_tok
        self.parsePrec(self.get_rule(ttype)._prec.value+1)
        node_b = self._ast_tab.pop_node()
        node_a = self._ast_tab.pop_node()
        if ttype == TokenType.PLUS:
            node = BinaryOp(tok, node_a, TokenType.PLUS, node_b)
            self._ast_tab.push_node(node)
        elif ttype == TokenType.MINUS:
            node = BinaryOp(tok, node_a, TokenType.MINUS, node_b)
            self._ast_tab.push_node(node)
        elif ttype == TokenType.DIV:
            node = BinaryOp(tok, node_a, TokenType.DIV, node_b)
            self._ast_tab.push_node(node)
        elif ttype == TokenType.MULT:
            node = BinaryOp(tok, node_a, TokenType.MULT, node_b)
            self._ast_tab.push_node(node)
        elif ttype == TokenType.MOD:
            node = BinaryOp(tok, node_a, TokenType.MOD, node_b)
            self._ast_tab.push_node(node)

    def get_rule(self, prec):
        return rules[list(TokenType).index(TokenType[prec.name])]

    def error(self, msg, tok):
        print(msg, '[line %d]'%tok.line_no, '->', tok.value)
        self._had_error = True
        

    def adv(self):
        self.prev_tok = self.curr_tok
        while True:
            tok = self._lexer.getToken()
            self.curr_tok = tok
            return

    def synch(self):
        self.curr_tok = makeToken(TokenType.EOF, self.curr_tok.line_no, None)

    def parsePrec(self, prec):
        self.adv()
        parse_rule = self.get_rule(self.prev_tok.type)
        if parse_rule and not parse_rule._prefix:
            self.error("Invalid Token", self.prev_tok)
            self.synch()
            return
        parse_rule._prefix(self)
        if self._had_error: return
        try:
            while prec <= self.get_rule(self.curr_tok.type)._prec.value:
                self.adv()
                parse_rule = self.get_rule(self.prev_tok.type)
                parse_rule._infix(self)
        except:
            while prec.value <= self.get_rule(self.curr_tok.type)._prec.value:
                self.adv()
                parse_rule = self.get_rule(self.prev_tok.type)
                parse_rule._infix(self)

    def grouping(self):
        self.expr()
        self.consume(')', "Expected ')' at end of expression")

    def consume(self, chars, msg):
        if self.curr_tok.value == chars:
            self.adv()
        else:
            self.error(msg, self.curr_tok)

    def expr(self):
        self.parsePrec(Precedence.PREC_EXPR)

    def show(self):
        return ( self._ast_tab.pop_node())


rules = [
    ParseRule(pref=PParser.unary, inf=PParser.binary, prec=Precedence.PREC_EXPR),   #PLUS
    ParseRule(pref=PParser.unary, inf=PParser.binary, prec=Precedence.PREC_EXPR),   #MINUS
    ParseRule(pref=None, inf=PParser.binary, prec=Precedence.PREC_TERM),   #DIV
    ParseRule(pref=None, inf=PParser.binary, prec=Precedence.PREC_TERM),   #MULT
    ParseRule(pref=None, inf=PParser.binary, prec=Precedence.PREC_SUP_TERM),   #MOD
    ParseRule(pref=PParser.grouping, inf=None, prec=Precedence.PREC_NONE),   #LPAREN
    ParseRule(pref=None, inf=PParser.binary, prec=Precedence.PREC_NONE),   #RPAREN
    ParseRule(pref=PParser.number, inf=None, prec=Precedence.PREC_NONE),   #NUMBER
    ParseRule(pref=None, inf=None, prec=Precedence.PREC_NONE),   #EOF
    ParseRule(pref=None, inf=None, prec=Precedence.PREC_NONE)    #ERR
]