# interpreter / parser
# arithmetic expressions

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # type PLUS, MINUS, EOF, etc.
        self.type = type
        # value 2,'+','-',None, etc.
        self.value = value

    def __str__(self):
        """return Token object
        ex.
            Token(INTEGER, 2)
            Token(MUL, '*')
            Token(LPAREN, '(')
        """
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()



class Lexer(object):
    def __init__(self, text):
        # user input
        self.text = text
        # position within the text string
        self.pos = 0
        # character at the position within the text string
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        """walk through the text one character at a time"""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # End of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """ignore any whitespaces in the input"""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        
    def integer(self):
        """combine any number of digit characters and convert them to an int"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result = result + self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """workhorse of the interpreter
        
        creates Token objects
        ex.
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(LPAREN, '(')
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)




class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        """if the token type and the type of the current type match
        move to the next token
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        """term : (factor(MUL | DIV)factor)*"""
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()

        return result

    def expr(self):
        """expr : term((PLUS | MINUS)term)*"""
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result



def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)



if __name__=='__main__':
    main()