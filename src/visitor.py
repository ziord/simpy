from pp import *

class NodeVisitor(AST):
    def __init__(self):
        self._val_stack = Stack()

    def visit(self, node):
        meth_name = 'visit_' + node.__class__.__name__ 
        visitor = getattr(self, meth_name, self.generic_err)
        return visitor(node)

    def generic_err(self):
        raise Exception("Unknown Node")

    def visit_UnaryOp(self, node):
        self.visit(node._rnode)
        if node._tok.type == TokenType.PLUS:
            self._val_stack.push(self._val_stack.pop())
        elif node._tok.type == TokenType.MINUS:
            self._val_stack.push(-self._val_stack.pop())

    def visit_Num(self, node):
        self._val_stack.push(node._value)

    def visit_BinaryOp(self, node):
        self.visit(node._lnode)
        self.visit(node._rnode)
        rn = self._val_stack.pop()
        ln = self._val_stack.pop()
        if node._tok.type == TokenType.PLUS:
            self._val_stack.push(ln+rn)
        elif node._tok.type == TokenType.MINUS:
           self._val_stack.push(ln-rn)
        elif node._tok.type == TokenType.DIV:
           self._val_stack.push(ln/rn)
        elif node._tok.type == TokenType.MULT:
           self._val_stack.push(ln*rn)
        elif node._tok.type == TokenType.MOD:
           self._val_stack.push(ln%rn)

    def result(self):
        return self._val_stack.pop()
        