import lexer

class AST:
    ...

class Num(AST):
    def __init__(self, tok, value):
        self._tok = tok
        self._value = value

class UnaryOp(AST):
    def __init__(self, tok, op, rnode):
        self._tok = tok
        self._op = op
        self._rnode = rnode

class BinaryOp(AST):
    def __init__(self, tok, lnode, op, rnode):
        self._tok = tok
        self._lnode = lnode
        self._op = op 
        self._rnode = rnode



    
