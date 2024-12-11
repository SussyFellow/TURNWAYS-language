import re


TOKEN_TYPES = {
    'NUMBER': r'\d+(\.\d+)?',           # Matches integers or decimals
    'STRING': r'"[^"]*"',               # Matches double-quoted strings
    'TRUE': r'\btrue\b',                # Matches 'true' literal
    'FALSE': r'\bfalse\b',              # Matches 'false' literal
    'LET': r'\blet\b',                  # Matches 'let' keyword
    'PRINT': r'\bprint\b',              # Matches 'print' keyword
    'IF': r'\bif\b',                    # Matches 'if' keyword
    'WHILE': r'\bwhile\b',              # Matches 'while' keyword
    'BREAK': r'\bbreak\b',              # Matches 'break' keyword
    'CONTINUE': r'\bcontinue\b',        # Matches 'continue' keyword
    'PAGE': r'\bpage\b',        # Matches 'page' keyword
    'EQUALS': r'==',
    'NOT_EQUALS': r'!=',
    'LESS': r'<',
    'GREATER': r'>',
    'LESS_EQUALS': r'<=',
    'GREATER_EQUALS': r'>=',
    'IDENTIFIER': r'[a-zA-Z_]\w*',      # Matches variable names
    'EQUAL_ASSIGN': r'=',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MUL': r'\*',
    'DIV': r'/',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'LBRACKET': r'\[',
    'RBRACKET': r'\]',
    'SEMICOLON': r';',
    'WHITESPACE': r'\s+',               # Spaces, tabs, etc.
}

printZone = ""

def printZIn(text):
    global printZone 
    printZone += str(text) + '\n'

def printZOut():
    global printZone
    print(turnwaysFlop(printZone))
    printZone = ''
    return True
    
def vertInput():
    inPiece = ''
    inWhole = ''
    while (True):
        inPiece = str(input())
        if (inPiece == ''): 
            break
        elif (inWhole != ''):
            inPiece = '\n' + inPiece
        inWhole += inPiece
    return inWhole

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

def tokenize(text):
    tokens = []
    pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())
    for match in re.finditer(pattern, text):
        kind = match.lastgroup
        value = match.group()
        if kind == 'WHITESPACE':
            continue  # Skip whitespace
        elif kind == 'NUMBER':
            value = float(value)  # Convert to number
        elif kind == 'STRING':
            value = value[1:-1]  # Remove quotes from strings
        tokens.append(Token(kind, value))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current] if self.current < len(self.tokens) else None

    def consume(self):
        token = self.peek()
        self.current += 1
        return token

    def parse(self):
        statements = []
        while self.peek():
            statements.append(self.statement())
        return statements

    def statement(self):
        token = self.peek()
        if token.type == 'LET':
            return self.variable_declaration()
        elif token.type == 'PRINT':
            return self.print_statement()
        elif token.type == 'IF':
            return self.if_statement()
        elif token.type == 'WHILE':
            return self.while_statement()
        elif token.type == 'BREAK':
            return self.break_statement()
        elif token.type == 'CONTINUE':
            return self.continue_statement()
        elif token.type == 'PAGE':
            return self.page_statement()
        else:
            return self.expression()

    def variable_declaration(self):
        self.consume()  # Consume 'let'
        identifier = self.consume()
        if identifier.type != 'IDENTIFIER':
            raise SyntaxError("Expected variable name after 'let'")
        if self.consume().type != 'EQUAL_ASSIGN':
            raise SyntaxError("Expected '=' after variable name")
        value = self.expression()
        if self.consume().type != 'SEMICOLON':
            raise SyntaxError("Expected ';' after variable declaration")
        return ('let', identifier.value, value)
    
    def print_statement(self):
        self.consume()  # Consume 'print'
        if self.consume().type != 'LPAREN':
            raise SyntaxError("Expected '(' after 'print'")
        value = self.expression()
        if self.consume().type != 'RPAREN':
            raise SyntaxError("Expected ')' after print argument")
        if self.consume().type != 'SEMICOLON':
            raise SyntaxError("Expected ';' after print statement")
        return ('print', value)

    def if_statement(self):
        self.consume()  # Consume 'if'
        if self.consume().type != 'LPAREN':
            raise SyntaxError("Expected '(' after 'if'")
        condition = self.expression()
        if self.consume().type != 'RPAREN':
            raise SyntaxError("Expected ')' after condition")
        if self.consume().type != 'LBRACE':
            raise SyntaxError("Expected '{' to start if block")
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            body.append(self.statement())
        if self.consume().type != 'RBRACE':
            raise SyntaxError("Expected '}' to end if block")
        return ('if', condition, body)
    
    def while_statement(self):
        self.consume()  # Consume 'while'
        if self.consume().type != 'LPAREN':
            raise SyntaxError("Expected '(' after 'while'")
        condition = self.expression()
        if self.consume().type != 'RPAREN':
            raise SyntaxError("Expected ')' after condition")
        if self.consume().type != 'LBRACE':
            raise SyntaxError("Expected '{' to start while block")
        body = []
        while self.peek() and self.peek().type != 'RBRACE':
            body.append(self.statement())
        if self.consume().type != 'RBRACE':
            raise SyntaxError("Expected '}' to end while block")
        return ('while', condition, body)
    
    def break_statement(self):
        self.consume()  # Consume 'break'
        if self.consume().type != 'SEMICOLON':
            raise SyntaxError("Expected ';' after 'break'")
        return ('break',)

    def continue_statement(self):
        self.consume()  # Consume 'continue'
        if self.consume().type != 'SEMICOLON':
            raise SyntaxError("Expected ';' after 'continue'")
        return ('continue',)

    def page_statement(self):
        self.consume()  # Consume 'page'
        if self.consume().type != 'SEMICOLON':
            raise SyntaxError("Expected ';' after 'page'")
        return ('page',)

    def expression(self):
        node = self.comparison()
        return self.array_access(node)
    
    def array_access(self, node):
        while self.peek() and self.peek().type == 'LBRACKET':
            self.consume()  # Consume '['
            index = self.expression()
            if self.consume().type != 'RBRACKET':
                raise SyntaxError("Expected ']' after array index")
            node = ('array_access', node, index)
        return node

    def comparison(self):
        # Handles comparisons (==, !=, <, >, <=, >=)
        node = self.term()
        if self.peek() and self.peek().type in ('EQUALS', 'NOT_EQUALS', 'LESS', 'GREATER', 'LESS_EQUALS', 'GREATER_EQUALS'):
            op = self.consume()
            right = self.term()
            return (op.type, node, right)
        return node

    def term(self):
        # Handles addition and subtraction
        node = self.factor()
        while self.peek() and self.peek().type in ('PLUS', 'MINUS'):
            op = self.consume()
            right = self.factor()
            node = (op.type, node, right)
        return node

    def factor(self):
        # Handles numbers, strings, identifiers, array literals, and parentheses
        token = self.consume()
        if token.type == 'NUMBER':
            return float(token.value)
        elif token.type == 'STRING':
            return token.value
        elif token.type == 'TRUE':
            return True
        elif token.type == 'FALSE':
            return False
        elif token.type == 'IDENTIFIER':
            return ('var', token.value)
        elif token.type == 'LBRACKET':  # Array literal
            elements = []
            while self.peek() and self.peek().type != 'RBRACKET':
                elements.append(self.expression())
                if self.peek() and self.peek().type == 'COMMA':
                    self.consume()  # Consume ','
            if self.consume().type != 'RBRACKET':
                raise SyntaxError("Expected ']' to close array literal")
            return ('array', elements)
        elif token.type == 'LPAREN':
            expr = self.expression()
            if self.consume().type != 'RPAREN':
                raise SyntaxError("Expected ')'")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")

def evaluate(node, context):
    if isinstance(node, (float, bool, str)):  # Number, boolean, or string
        return node
    elif isinstance(node, tuple):
        if node[0] == 'let':
            _, name, value = node
            context[name] = evaluate(value, context)
            return None
        elif node[0] == 'print':
            _, value = node
            printZIn(evaluate(value, context))
            return None
        elif node[0] == 'var':
            _, name = node
            if name not in context:
                raise NameError(f"Variable '{name}' not defined")
            return context[name]
        elif node[0] == 'if':
            _, condition, body = node
            if evaluate(condition, context):
                for statement in body:
                    evaluate(statement, context)
            return None
        elif node[0] == 'while':
            _, condition, body = node
            while evaluate(condition, context):
                for statement in body:
                    result = evaluate(statement, context)
                    if result == 'break':
                        return None
                    elif result == 'continue':
                        break
            return None
        elif node[0] == 'break':
            return 'break'
        elif node[0] == 'continue':
            return 'continue'
        elif node[0] == 'page':
            printZOut()
            return None
        elif node[0] == 'array':
            _, elements = node
            return [evaluate(element, context) for element in elements]
        elif node[0] == 'array_access':
            _, array, index = node
            array_val = evaluate(array, context)
            index_val = int(evaluate(index, context))
            if not isinstance(array_val, list):
                raise TypeError("Attempted to access an index on a non-array")
            if index_val < 0 or index_val >= len(array_val):
                raise IndexError("Array index out of range")
            return array_val[index_val]
        elif node[0] == 'EQUAL_ASSIGN':  # For array index assignment
            _, target, value = node
            if target[0] == 'array_access':
                _, array, index = target
                array_val = evaluate(array, context)
                index_val = int(evaluate(index, context))
                if not isinstance(array_val, list):
                    raise TypeError("Attempted to assign to an index on a non-array")
                if index_val < 0 or index_val >= len(array_val):
                    raise IndexError("Array index out of range")
                array_val[index_val] = evaluate(value, context)
                return None
        elif node[0] in ('PLUS', 'MINUS', 'MUL', 'DIV'):
            op, left, right = node
            left_val = evaluate(left, context)
            right_val = evaluate(right, context)
            if op == 'PLUS':
                return left_val + right_val
            elif op == 'MINUS':
                return left_val - right_val
            elif op == 'MUL':
                return left_val * right_val
            elif op == 'DIV':
                return left_val / right_val
        elif node[0] in ('EQUALS', 'NOT_EQUALS', 'LESS', 'GREATER', 'LESS_EQUALS', 'GREATER_EQUALS'):
            op, left, right = node
            left_val = evaluate(left, context)
            right_val = evaluate(right, context)
            if op == 'EQUALS':
                return left_val == right_val
            elif op == 'NOT_EQUALS':
                return left_val != right_val
            elif op == 'LESS':
                return left_val < right_val
            elif op == 'GREATER':
                return left_val > right_val
            elif op == 'LESS_EQUALS':
                return left_val <= right_val
            elif op == 'GREATER_EQUALS':
                return left_val >= right_val
    raise ValueError(f"Unexpected node: {node}")

def turnwaysFlip(text): #takes vertical text and turns it horizontal
    lines = text.splitlines()
    x = 0
    turnText = ''
    if (lines == []):
        return ''
    while (x < len(lines[0])):
        y = 0
        while (y < len(lines)):
            if (x < len(lines[y])):
                turnText += str(lines[y][x])
            y += 1
        x += 1
        if (x < len(lines[0])):
            turnText += '\n'
    return turnText    

def turnwaysFlop(text): #takes horizontal text and turns it veritcal
    lines = text.splitlines()
    longLine = 0
    for line in lines:
        if (len(line) > longLine):
            longLine = len(line)
    turnLines = ['']*longLine
    for line in lines:
        for i in range(0, longLine):
            if(i < len(line)):
                turnLines[i] += str(line[i])
            else: 
                turnLines[i] += ' '
    turnText = '\n'.join(turnLines)
    return turnText

def main():
    print(turnwaysFlop("Enter file path to source code:"))
    input_file = turnwaysFlip(vertInput())
    try:
        with open(input_file, 'r') as f:
            raw_code = turnwaysFlop(f.read()) 
            source_code = turnwaysFlip(raw_code)
            tokens = tokenize(source_code)
            
            parser = Parser(tokens)
            program = parser.parse()
            
            context = {}
            for statement in program:
                evaluate(statement, context)
    except FileNotFoundError:
        printZIn(f"File '{input_file}' not found. Please try again.")
    except Exception as e:
        printZIn(f"An error occurred: {e}")
    printZOut()

main()