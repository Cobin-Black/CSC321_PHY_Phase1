import sys
from ast_nodes import Program, AssignmentStatement, PrintStatement, BinaryExpression, IntegerLiteral, Identifier, ForLoopStatement
from lexer import Lexer
from parser import Parser

# ==========================================
# 1. THE INTERPRETER (Math + Unit Logic)
# ==========================================
class Interpreter:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        if isinstance(node, IntegerLiteral):
            try:
                val = float(node.value)
            except ValueError:
                val = node.value
            return {'val': val, 'unit': node.unit}

        if isinstance(node, Identifier):
            if node.name in self.variables:
                return self.variables[node.name]
            raise NameError(f"Undefined variable: {node.name}")

        if isinstance(node, BinaryExpression):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.operator == '*':
                res_val = left['val'] * right['val']
                u1 = left['unit'] or ""
                u2 = right['unit'] or ""
                res_unit = f"{u1}*{u2}".strip('*')
                return {'val': res_val, 'unit': res_unit}
            
            # Division
            if node.operator == '/':
                res_val = left['val'] / right['val']
                u1 = left['unit'] or ""
                u2 = right['unit'] or ""
                res_unit = f"{u1}/{u2}".strip('/')
                return {'val': res_val, 'unit': res_unit}

            # Addition/Subtraction (Units must stay the same)
            if node.operator == '+':
                return {'val': left['val'] + right['val'], 'unit': left['unit']}
            if node.operator == '-':
                return {'val': left['val'] - right['val'], 'unit': left['unit']}

    def execute(self, node):
        if isinstance(node, Program):
            for s in node.statements: self.execute(s)
        elif isinstance(node, AssignmentStatement):
            self.variables[node.identifier.name] = self.evaluate(node.expression)
        elif isinstance(node, PrintStatement):
            res = self.evaluate(node.expression)
            print(f"RESULT: {res['val']} {res['unit'] or ''}")
        elif isinstance(node, ForLoopStatement): # <--- ADD THIS
            start = int(self.evaluate(node.start_expr)['val'])
            end = int(self.evaluate(node.end_expr)['val'])
            for i in range(start, end):
                self.variables[node.identifier.name] = {'val': float(i), 'unit': None}
                for stmt in node.body:
                    self.execute(stmt)

# ==========================================
#UTILITY
# ==========================================
def print_ast(node, indent=0):
    if node is None: return
    p = "  " * indent
    if isinstance(node, Program):
        print("Program")
        for s in node.statements: print_ast(s, indent + 1)
    elif isinstance(node, AssignmentStatement):
        info = f"({node.mode or ''} {node.type_kw or ''})".strip()
        print(f"{p}AssignmentStatement {info}")
        print_ast(node.identifier, indent + 2)
        print_ast(node.expression, indent + 2)
    elif isinstance(node, PrintStatement):
        print(f"{p}PrintStatement")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, BinaryExpression):
        print(f"{p}BinaryExpression ({node.operator})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, IntegerLiteral):
        u = f", unit: {node.unit}" if node.unit else ""
        print(f"{p}IntegerLiteral (value: {node.value}{u})")
    elif isinstance(node, Identifier):
        print(f"{p}Identifier ({node.name})")
    elif isinstance(node, ForLoopStatement):
        print(f"{p}ForLoop (var: {node.identifier.name})")
        for s in node.body:
            print_ast(s, indent + 2)

# ==========================================
#MAIN
# ==========================================
if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "test.phy"
    
    try:
        with open(filename, 'r') as f:
            source = f.read()

        #Lexing
        tokens = Lexer(source).tokenize()
        
        #Parsing
        parser = Parser(tokens)
        ast_tree = parser.parse()

        # Showing AS
        print("\n--- ABSTRACT SYNTAX TREE ---")
        print_ast(ast_tree)

        #Showing INTERPRETED RESULTS 
        print("\n--- INTERPRETED RESULTS ---")
        interpreter = Interpreter()
        interpreter.execute(ast_tree)
        print("---------------------------\n")

    except Exception as e:
        print(f"Error: {e}")
