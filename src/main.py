from lexer import *
from visitor import *


def print_src(src):
    lex = Lexer(src)
    done = False
    line = 0
    while not done:
        tok = lex.getToken()
        if tok.type == TokenType.EOF or tok.type == TokenType.ERR:
            done = True
        if line == tok.line_no:
            print('| ', end='')
        else: 
            print(tok.line_no, end=' ')
            line = tok.line_no

        print("%8s"%(tok.value), "\t'%*s'"%(len(str(tok.value)), tok.type))

def main():
    while True:
        src = input(">>> ")
        if not src: 
            continue
        if src.strip().lower() == 'exit':
            break
        print_src(src)
        lex = Lexer(src)
        parser = PParser(lex)
        parser.expr()
        if parser._had_error:
            continue
        v = NodeVisitor()
        v.visit(parser.show())
        print("%g"%v.result())

if __name__ == '__main__':
    main()