from ast_nodes import Program, AssignmentStatement, PrintStatement, BinaryExpression, IntegerLiteral, Identifier, ForLoopStatement

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

    def parse_for(self):
        self.eat('FOR')
        self.eat('LPAREN')
        var_name = self.eat('IDENTIFIER').value
        self.eat('IN')
        self.eat('RANGE')
        self.eat('LPAREN')
        # We'll assume range(end) for simplicity
        end_val = self.parse_expr() 
        self.eat('RPAREN')
        self.eat('RPAREN')
        
        self.eat('LBRACE')
        body = []
        while self.current().type != 'RBRACE':
            body.append(self.parse_statement())
        self.eat('RBRACE')
        
        # Default start at 0 for now
        return ForLoopStatement(Identifier(var_name), IntegerLiteral("0"), end_val, body)

    def parse_statement(self):
        t = self.current().type
        if t == 'PRINT':
            self.eat('PRINT')
            e = self.parse_expr()
            self.eat('SEMICOLON')
            return PrintStatement(e)
        if t == 'FOR':               # <--- ADD THIS
            return self.parse_for()
        return self.parse_assignment()

    def parse_for(self):
        self.eat('FOR')
        self.eat('LPAREN')
        var_name = self.eat('IDENTIFIER').value
        self.eat('IN')
        self.eat('RANGE')
        self.eat('LPAREN')
        end_val = self.parse_expr()
        self.eat('RPAREN')
        self.eat('RPAREN')
        self.eat('LBRACE')
        body = []
        while self.current().type != 'RBRACE':
            body.append(self.parse_statement())
        self.eat('RBRACE')
        return ForLoopStatement(Identifier(var_name), IntegerLiteral("0"), end_val, body)

    def parse_assignment(self):
        m = self.eat(self.current().type).value if self.current().type in ('GIVEN', 'LET') else None
        tk = self.eat('TYPE_KW').value if self.current().type == 'TYPE_KW' else None
        
        # FIX: Allow 'g' or 'm' to be variable names even if they are units
        if self.current().type in ('IDENTIFIER', 'UNIT'):
            name = self.eat(self.current().type).value
        else:
            self.eat('IDENTIFIER') # This will trigger the standard error
            
        self.eat('EQUALS')
        e = self.parse_expr()
        self.eat('SEMICOLON')
        return AssignmentStatement(Identifier(name), e, m, tk)
        
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
            elif self.current().type == 'IDENTIFIER' and self.current().value in ['kg', 'g', 'meter', 'secs', 'N', 'J', 'W', 'k']:
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
