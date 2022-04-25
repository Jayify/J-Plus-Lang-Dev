# J+ Lang Lexer created by Jayden Houghton

# -------------- SET UP ---------------

# IMPORTS
from strings_with_arrows import *
# module supplied by CodePulse

# CONSTANTS
DIGITS = "0123456789"


# -------------- ERRORS ---------------
# create custom error class


class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.line + 1}'
        result += "\n\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self. pos_end)
        return result


# subclass of Error, inherits all attributes
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


# -------------- POSITION ---------------

class Position:
    def __init__(self, index, line, column, fn, ftxt):
        self.index = index
        self.line = line
        self.column = column
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.fn, self.ftxt)


# -------------- TOKENS ---------------
# TT stands for Token Type

TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f"{self.type}: {self.value}"
        return f"{self.type}"


# -------------- LEXER ---------------

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None


    def make_tokens(self):
        # returns token, None if valid char, returns [], error if invalid char
        tokens = []

        while self.current_char != None:
            # char is space or tab
            if self.current_char in ' \t':
                self.advance()

            # check if char in digits
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            # check for operator
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            # return error if character not found
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        # check if current_char is a digit or a dot
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


# -------------- NODES ---------------

class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"


class BinOpNode:
    # binary operation node
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.op_token}, {self.right_node})"


# -------------- PARSER ---------------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tkn_index = -1
        self.advance()

    def advance(self):
        self.tkn_index += 1
        if self.tkn_index < len(self.tokens):
            self.current_tkn = self.tokens[self.tkn_index]
        return self.current_tkn

    def parse(self):
        res = self.expr()
        return res

    # grammar rules
    def factor(self):
        token = self.current_tkn
        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        left = func()

        while self.current_tkn.type in ops:
            op_tkn = self.current_tkn
            self.advance()
            right = func()
            left = BinOpNode(left, op_tkn, right)
        return left


# -------------- RUN ---------------

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    # generate abstract syntax tree (AST)
    parser = Parser(tokens)
    ast = parser.parse()
    # return tokens, error
    return ast, None

