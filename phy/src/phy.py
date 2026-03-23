
import sys
from ast_nodes import Program, AssignmentStatement, PrintStatement, BinaryExpression, IntegerLiteral, Identifier
from lexer import Lexer
from parser import Parser
# 2. THE UTILITY FUNCTION LIVES HERE
def print_ast(node, indent=0):
    if node is None: return
    p = "  " * indent
    if isinstance(node, Program):
        print("Program")
        for s in node.statements: print_ast(s, indent + 1)
    elif isinstance(node, AssignmentStatement):
        m = f" ({node.mode or ''} {node.type_kw or ''})".strip()
        print(f"{p}AssignmentStatement {m}")
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

# 3. THE ACTUAL EXECUTION
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python phy.py test.phy")
        sys.exit(1)
    
    target = sys.argv[-1] 
    try:
        with open(target, 'r') as f:
            content = f.read()
        
        # Call the Lexer from lexer.py
        tokens = Lexer(content).tokenize()
        
        # Call the Parser from parse.py
        parser = Parser(tokens)
        ast_tree = parser.parse()
        
        # Call the print function defined above
        print_ast(ast_tree)
        
    except Exception as e:
        print(f"Error: {e}")
