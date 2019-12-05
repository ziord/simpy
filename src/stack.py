import ast

class Stack:
    def __init__(self):
        self._stack = []

    def push(self, val):
        self._stack.insert(0, val)

    def pop(self):
        if len(self._stack) < 1: return
        val = self._stack[0]
        self._stack.remove(val)
        return val


class ASTTable(Stack):
    def __init__(self):
        Stack.__init__(self)

    def push_node(self, val):
        Stack.push(self, val)

    def pop_node(self):
        return Stack.pop(self)
