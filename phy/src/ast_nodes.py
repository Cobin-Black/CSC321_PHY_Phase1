class Node:
    """Base class for all nodes."""
    def __str__(self):
        return self.__class__.__name__

class Program(Node):
    def __init__(self, statements):
        self.statements = statements # List of Statement nodes

class AssignmentStatement(Node):
    def __init__(self, identifier, expression, mode=None, type_kw=None):
        self.identifier = identifier  # Identifier node
        self.expression = expression  # BinaryExpression or Literal
        # Optional metadata for PHY
        self.mode = mode              # 'given' or 'let'
        self.type_kw = type_kw        # 'mass', 'accel', etc.

class PrintStatement(Node):
    def __init__(self, expression):
        self.expression = expression

class BinaryExpression(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IntegerLiteral(Node):
    def __init__(self, value, unit=None):
        # We store the value (can be int or time string)
        self.value = value 
        # Unit is stored here to keep PHY functionality 
        self.unit = unit 

class Identifier(Node):
    def __init__(self, name):
        self.name = name