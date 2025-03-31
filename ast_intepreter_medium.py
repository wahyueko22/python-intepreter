"""
Simple Compiler Implementation in Python

This compiler supports:
- Variable assignments
- Arithmetic operations (+, -, *, /)
- Print statements
- If statements
- While loops

Example syntax:
    x = 5;
    y = 10;
    print x + y;
    if x < y then
        print "x is less than y";
    end
    while x < 20 do
        x = x + 1;
        print x;
    end
"""

class Token:
    # Token types
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    ID = 'ID'
    ASSIGN = 'ASSIGN'
    SEMICOLON = 'SEMICOLON'
    EOF = 'EOF'
    PRINT = 'PRINT'
    STRING = 'STRING'
    IF = 'IF'
    THEN = 'THEN'
    ELSE = 'ELSE'
    END = 'END'
    WHILE = 'WHILE'
    DO = 'DO'
    GREATER = 'GREATER'
    LESS = 'LESS'
    EQUAL = 'EQUAL'
    
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        return f'Token({self.type}, {self.value})'
        
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        
    def error(self):
        raise Exception('Invalid character')
        
    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
        
    def string(self):
        result = ''
        # Skip the opening quote
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        # Skip the closing quote
        self.advance()
        return result
        
    def _id(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        # Check for keywords
        keywords = {
            'print': Token.PRINT,
            'if': Token.IF,
            'then': Token.THEN,
            'else': Token.ELSE,
            'end': Token.END,
            'while': Token.WHILE,
            'do': Token.DO
        }
        
        token_type = keywords.get(result, Token.ID)
        return Token(token_type, result)
        
    def get_next_token(self):
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
                
            if self.current_char.isdigit():
                return Token(Token.INTEGER, self.integer())
                
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
                
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(Token.EQUAL, '==')
                return Token(Token.ASSIGN, '=')
                
            if self.current_char == ';':
                self.advance()
                return Token(Token.SEMICOLON, ';')
                
            if self.current_char == '+':
                self.advance()
                return Token(Token.PLUS, '+')
                
            if self.current_char == '-':
                self.advance()
                return Token(Token.MINUS, '-')
                
            if self.current_char == '*':
                self.advance()
                return Token(Token.MULTIPLY, '*')
                
            if self.current_char == '/':
                self.advance()
                return Token(Token.DIVIDE, '/')
                
            if self.current_char == '(':
                self.advance()
                return Token(Token.LPAREN, '(')
                
            if self.current_char == ')':
                self.advance()
                return Token(Token.RPAREN, ')')
                
            if self.current_char == '>':
                self.advance()
                return Token(Token.GREATER, '>')
                
            if self.current_char == '<':
                self.advance()
                return Token(Token.LESS, '<')
                
            if self.current_char == '"':
                return Token(Token.STRING, self.string())
                
            self.error()
            
        return Token(Token.EOF, None)

class AST:
    pass

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(AST):
    pass

class Print(AST):
    def __init__(self, expr):
        self.expr = expr

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class If(AST):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Condition(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invalid syntax')
        
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
            
    def program(self):
        """
        program : compound_statement
        """
        node = self.compound_statement()
        return node
        
    def compound_statement(self):
        """
        compound_statement : statement (SEMICOLON statement)* SEMICOLON?
        """
        nodes = []
        
        node = self.statement()
        nodes.append(node)
        
        while self.current_token.type == Token.SEMICOLON:
            self.eat(Token.SEMICOLON)
            if self.current_token.type in (Token.ID, Token.PRINT, Token.IF, Token.WHILE):
                nodes.append(self.statement())
            else:
                break
                
        root = Compound()
        root.children = nodes
        return root
        
    def statement(self):
        """
        statement : assignment_statement 
                  | print_statement 
                  | if_statement
                  | while_statement
                  | empty
        """
        if self.current_token.type == Token.ID:
            node = self.assignment_statement()
        elif self.current_token.type == Token.PRINT:
            node = self.print_statement()
        elif self.current_token.type == Token.IF:
            node = self.if_statement()
        elif self.current_token.type == Token.WHILE:
            node = self.while_statement()
        else:
            node = self.empty()
        return node
        
    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(Token.ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
        
    def print_statement(self):
        """
        print_statement : PRINT expr
        """
        self.eat(Token.PRINT)
        node = Print(self.expr())
        return node
        
    def if_statement(self):
        """
        if_statement : IF condition THEN compound_statement END
                     | IF condition THEN compound_statement ELSE compound_statement END
        """
        self.eat(Token.IF)
        condition = self.condition()
        self.eat(Token.THEN)
        body = self.compound_statement()
        
        else_body = None
        if self.current_token.type == Token.ELSE:
            self.eat(Token.ELSE)
            else_body = self.compound_statement()
            
        self.eat(Token.END)
        return If(condition, body, else_body)
        
    def while_statement(self):
        """
        while_statement : WHILE condition DO compound_statement END
        """
        self.eat(Token.WHILE)
        condition = self.condition()
        self.eat(Token.DO)
        body = self.compound_statement()
        self.eat(Token.END)
        return While(condition, body)
        
    def condition(self):
        """
        condition : expr (GREATER | LESS | EQUAL) expr
        """
        left = self.expr()
        
        if self.current_token.type in (Token.GREATER, Token.LESS, Token.EQUAL):
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.expr()
            return Condition(left, op, right)
        else:
            self.error()
        
    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(Token.ID)
        return node
        
    def empty(self):
        """
        empty :
        """
        return NoOp()
        
    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()
        
        while self.current_token.type in (Token.PLUS, Token.MINUS):
            token = self.current_token
            if token.type == Token.PLUS:
                self.eat(Token.PLUS)
            else:
                self.eat(Token.MINUS)
                
            node = BinOp(left=node, op=token, right=self.term())
            
        return node
        
    def term(self):
        """
        term : factor ((MULTIPLY | DIVIDE) factor)*
        """
        node = self.factor()
        
        while self.current_token.type in (Token.MULTIPLY, Token.DIVIDE):
            token = self.current_token
            if token.type == Token.MULTIPLY:
                self.eat(Token.MULTIPLY)
            else:
                self.eat(Token.DIVIDE)
                
            node = BinOp(left=node, op=token, right=self.factor())
            
        return node
        
    def factor(self):
        """
        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable
               | STRING
        """
        token = self.current_token
        if token.type == Token.PLUS:
            self.eat(Token.PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Token.MINUS:
            self.eat(Token.MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == Token.INTEGER:
            self.eat(Token.INTEGER)
            return Num(token)
        elif token.type == Token.LPAREN:
            self.eat(Token.LPAREN)
            node = self.expr()
            self.eat(Token.RPAREN)
            return node
        elif token.type == Token.ID:
            return self.variable()
        elif token.type == Token.STRING:
            self.eat(Token.STRING)
            return String(token)
        else:
            self.error()
            
    def parse(self):
        node = self.program()
        if self.current_token.type != Token.EOF:
            self.error()
        return node

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.global_scope = {}
        
    def visit_BinOp(self, node):
        if node.op.type == Token.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == Token.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == Token.MULTIPLY:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == Token.DIVIDE:
            return self.visit(node.left) / self.visit(node.right)
            
    def visit_Num(self, node):
        return node.value
        
    def visit_String(self, node):
        return node.value
        
    def visit_UnaryOp(self, node):
        if node.op.type == Token.PLUS:
            return +self.visit(node.expr)
        elif node.op.type == Token.MINUS:
            return -self.visit(node.expr)
            
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
            
    def visit_Assign(self, node):
        var_name = node.left.value
        self.global_scope[var_name] = self.visit(node.right)
        
    def visit_Var(self, node):
        var_name = node.value
        value = self.global_scope.get(var_name)
        if value is None:
            raise NameError(f"Variable '{var_name}' is not defined")
        return value
        
    def visit_NoOp(self, node):
        pass
        
    def visit_Print(self, node):
        print(self.visit(node.expr))
        
    def visit_If(self, node):
        if self.visit(node.condition):
            self.visit(node.body)
        elif node.else_body:
            self.visit(node.else_body)
            
    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.body)
            
    def visit_Condition(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op.type == Token.GREATER:
            return left > right
        elif node.op.type == Token.LESS:
            return left < right
        elif node.op.type == Token.EQUAL:
            return left == right
        
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
        
    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
        
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('> ')
        except EOFError:
            break
            
        if not text:
            continue
            
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        
        try:
            interpreter.interpret()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()