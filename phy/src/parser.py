from ast_nodes import Program, AssignmentStatement, PrintStatement, BinaryExpression, IntegerLiteral, Identifier

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self): 
        return self.tokens[self.pos]

    def eat(self, type):
        if self.current().type == type:
            token = self.current()
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {type}, got {self.current().type} at token {self.pos} ('{self.current().value}')")

    def parse(self):
        statements = []
        if self.current().type == 'GIVENS':
            self.eat('GIVENS')
            self.eat('LBRACE')
            while self.current().type != 'RBRACE':
                statements.append(self.parse_assignment())
            self.eat('RBRACE')
        while self.current().type != 'EOF':
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        if self.current().type == 'PRINT':
            self.eat('PRINT')
            expr = self.parse_expr()
            self.eat('SEMICOLON')
            return PrintStatement(expr)
        return self.parse_assignment()

    def parse_assignment(self):
        # 1. Look for 'given' or 'let'
        mode = None
        if self.current().type in ('GIVEN', 'LET'):
            mode = self.eat(self.current().type).value
        
        # 2. Look for 'mass', 'accel', 'force', etc.
        type_kw = None
        if self.current().type == 'TYPE_KW':
            type_kw = self.eat('TYPE_KW').value
            
        # 3. Now get the actual variable name (e.g., 'f' or 'm')
        name_token = self.eat('IDENTIFIER')
        
        # 4. Now expect the '='
        self.eat('EQUALS')
        
        # 5. Parse the rest
        expr = self.parse_expr()
        self.eat('SEMICOLON')
        
        return AssignmentStatement(Identifier(name_token.value), expr, mode, type_kw)

    def parse_expr(self):
        node = self.parse_term()
        while self.current().type in ('PLUS', 'MINUS'):
            op = self.eat(self.current().type).value
            node = BinaryExpression(node, op, self.parse_term())
        return node

    def parse_term(self):
        # This calls parse_factor. If parse_factor is missing, it crashes.
        node = self.parse_factor()
        while self.current().type in ('STAR', 'SLASH'):
            op = self.eat(self.current().type).value
            node = BinaryExpression(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        token = self.current()
        
        # Handle Time (e.g., 00:05:00)
        if token.type == 'TIME_LITERAL':
            return IntegerLiteral(self.eat('TIME_LITERAL').value)
        
        # Handle Numbers with optional Units
        if token.type in ('INT_LITERAL', 'FLOAT_LITERAL'):
            val = self.eat(token.type).value
            unit = None
            # If the very next thing is a UNIT, eat it now!
            if self.current().type == 'UNIT':
                unit = self.eat('UNIT').value
            # If it's an IDENTIFIER that SHOULD have been a unit, eat it too!
            elif self.current().type == 'IDENTIFIER' and self.current().value in ['kg', 'g', 'meter', 'secs', 'N', 'J', 'W']:
                unit = self.eat('IDENTIFIER').value
                
            return IntegerLiteral(val, unit)
            
        if token.type == 'IDENTIFIER':
            return Identifier(self.eat('IDENTIFIER').value)
        
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expr()
            self.eat('RPAREN')
            return node
            
        raise SyntaxError(f"Unexpected token {token.type} ('{token.value}') at token {self.pos}")