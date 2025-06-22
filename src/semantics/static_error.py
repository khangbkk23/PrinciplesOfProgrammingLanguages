"""
Static Error Classes for HLang Semantic Analysis
This module defines all the exception classes that can be raised during static semantic checking.
"""

class StaticError(Exception):
    """Base class for all static semantic errors"""
    pass


class Redeclared(StaticError):
    """
    Raised when an identifier is declared more than once in the same scope.
    
    Args:
        kind (str): The kind of redeclared entity ('Variable', 'Constant', 'Function', 'Parameter')
        name (str): The name of the redeclared identifier
    """
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        super().__init__(f"Redeclared {kind}: {name}")


class Undeclared(StaticError):
    """
    Raised when an identifier or function is used but not declared.
    
    Args:
        kind (object): Either Identifier() or Function() to indicate the type
        name (str): The name of the undeclared identifier/function
    """
    def __init__(self, kind, name):
        self.kind = kind
        self.name = name
        kind_str = "Identifier" if isinstance(kind, Identifier) else "Function"
        super().__init__(f"Undeclared {kind_str}: {name}")


class TypeMismatchInExpression(StaticError):
    """
    Raised when there's a type mismatch in an expression context.
    
    Args:
        expr: The expression node where the type mismatch occurred
    """
    def __init__(self, expr):
        self.expr = expr
        super().__init__(f"Type Mismatch In Expression: {expr}")


class TypeMismatchInStatement(StaticError):
    """
    Raised when there's a type mismatch in a statement context.
    
    Args:
        stmt: The statement node where the type mismatch occurred
    """
    def __init__(self, stmt):
        self.stmt = stmt
        super().__init__(f"Type Mismatch In Statement: {stmt}")


class TypeCannotBeInferred(StaticError):
    """
    Raised when a type cannot be inferred from the context.
    
    Args:
        stmt: The statement node where type inference failed
    """
    def __init__(self, stmt):
        self.stmt = stmt
        super().__init__(f"Type Cannot Be Inferred: {stmt}")


class MustInLoop(StaticError):
    """
    Raised when break/continue statements appear outside of loop constructs.
    
    Args:
        stmt: The break/continue statement node
    """
    def __init__(self, stmt):
        self.stmt = stmt
        super().__init__(f"Must In Loop: {stmt}")


class NoEntryPoint(StaticError):
    """
    Raised when there's no valid main function in the program.
    A valid main function must:
    - Be named 'main'
    - Take no parameters
    - Return void
    """
    def __init__(self):
        super().__init__("No Entry Point")


# Helper classes for Undeclared error
class Identifier:
    """Marker class to indicate undeclared identifier (variable/constant)"""
    def __str__(self):
        return "Identifier"


class Function:
    """Marker class to indicate undeclared function"""
    def __str__(self):
        return "Function"
