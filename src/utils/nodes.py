"""
AST Node classes for HLang programming language.
This module defines all the AST node types used to represent
the abstract syntax tree for HLang programs.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import ASTVisitor


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    def __init__(self):
        self.line = None
        self.column = None
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor', o: Any = None):
        """Accept a visitor for the Visitor pattern."""
        pass
    
    def __str__(self):
        """Default string representation."""
        return f"{self.__class__.__name__}()"


# ============================================================================
# Program and Top-level Declarations
# ============================================================================

class Program(ASTNode):
    """Root node representing the entire program."""
    
    def __init__(self, const_decls: List['ConstDecl'], func_decls: List['FuncDecl']):
        super().__init__()
        self.const_decls = const_decls
        self.func_decls = func_decls
    
    def accept(self, visitor, o=None):
        return visitor.visit_program(self, o)
    
    def __str__(self):
        const_str = ', '.join(str(c) for c in self.const_decls) if self.const_decls else ""
        func_str = ', '.join(str(f) for f in self.func_decls) if self.func_decls else ""
        parts = []
        if const_str:
            parts.append(f"consts=[{const_str}]")
        if func_str:
            parts.append(f"funcs=[{func_str}]")
        return f"Program({', '.join(parts)})" if parts else "Program()"


class ConstDecl(ASTNode):
    """Constant declaration node."""
    
    def __init__(self, name: str, type_annotation: Optional['Type'], value: 'Expr'):
        super().__init__()
        self.name = name
        self.type_annotation = type_annotation
        self.value = value
    
    def accept(self, visitor, o=None):
        return visitor.visit_const_decl(self, o)
    
    def __str__(self):
        type_str = f", {self.type_annotation}" if self.type_annotation else ""
        return f"ConstDecl({self.name}{type_str}, {self.value})"


class FuncDecl(ASTNode):
    """Function declaration node."""
    
    def __init__(self, name: str, params: List['Param'], return_type: 'Type', body: List['Stmt']):
        super().__init__()
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
    
    def accept(self, visitor, o=None):
        return visitor.visit_func_decl(self, o)
    
    def __str__(self):
        params_str = ', '.join(str(p) for p in self.params) if self.params else ""
        params_part = f"[{params_str}]" if params_str else "[]"
        body_str = ', '.join(str(s) for s in self.body) if self.body else ""
        body_part = f"[{body_str}]" if body_str else "[]"
        return f"FuncDecl({self.name}, {params_part}, {self.return_type}, {body_part})"


class Param(ASTNode):
    """Function parameter node."""
    
    def __init__(self, name: str, param_type: 'Type'):
        super().__init__()
        self.name = name
        self.param_type = param_type
    
    def accept(self, visitor, o=None):
        return visitor.visit_param(self, o)
    
    def __str__(self):
        return f"Param({self.name}, {self.param_type})"


# ============================================================================
# Type System
# ============================================================================

class Type(ASTNode):
    """Base class for type annotations."""
    pass


class IntType(Type):
    """Integer type node."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_int_type(self, o)
    
    def __str__(self):
        return "int"


class FloatType(Type):
    """Float type node."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_float_type(self, o)
    
    def __str__(self):
        return "float"


class BoolType(Type):
    """Boolean type node."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_bool_type(self, o)
    
    def __str__(self):
        return "bool"


class StringType(Type):
    """String type node."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_string_type(self, o)
    
    def __str__(self):
        return "string"


class VoidType(Type):
    """Void type node."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_void_type(self, o)
    
    def __str__(self):
        return "void"


class ArrayType(Type):
    """Array type node."""
    
    def __init__(self, element_type: Type, size: int):
        super().__init__()
        self.element_type = element_type
        self.size = size
    
    def accept(self, visitor, o=None):
        return visitor.visit_array_type(self, o)
    
    def __str__(self):
        return f"[{self.element_type}; {self.size}]"


# ============================================================================
# Statements
# ============================================================================

class Stmt(ASTNode):
    """Base class for all statement nodes."""
    pass


class VarDecl(Stmt):
    """Variable declaration statement."""
    
    def __init__(self, name: str, type_annotation: Optional[Type], value: 'Expr'):
        super().__init__()
        self.name = name
        self.type_annotation = type_annotation
        self.value = value
    
    def accept(self, visitor, o=None):
        return visitor.visit_var_decl(self, o)
    
    def __str__(self):
        type_str = f", {self.type_annotation}" if self.type_annotation else ""
        return f"VarDecl({self.name}{type_str}, {self.value})"


class Assignment(Stmt):
    """Assignment statement."""
    
    def __init__(self, lvalue: 'LValue', value: 'Expr'):
        super().__init__()
        self.lvalue = lvalue
        self.value = value
    
    def accept(self, visitor, o=None):
        return visitor.visit_assignment(self, o)
    
    def __str__(self):
        return f"Assignment({self.lvalue}, {self.value})"


class IfStmt(Stmt):
    """If statement with optional else-if and else branches."""
    
    def __init__(self, condition: 'Expr', then_stmt: 'BlockStmt', 
                 elif_branches: List[tuple], else_stmt: Optional['BlockStmt']):
        super().__init__()
        self.condition = condition
        self.then_stmt = then_stmt
        self.elif_branches = elif_branches  # List of (condition, block) tuples
        self.else_stmt = else_stmt
    
    def accept(self, visitor, o=None):
        return visitor.visit_if_stmt(self, o)
    
    def __str__(self):
        elif_str = ""
        if self.elif_branches:
            elif_parts = [f"({cond}, {block})" for cond, block in self.elif_branches]
            elif_str = f", elif_branches=[{', '.join(elif_parts)}]"
        else_str = f", else_stmt={self.else_stmt}" if self.else_stmt else ""
        return f"IfStmt(condition={self.condition}, then_stmt={self.then_stmt}{elif_str}{else_str})"


class WhileStmt(Stmt):
    """While loop statement."""
    
    def __init__(self, condition: 'Expr', body: 'BlockStmt'):
        super().__init__()
        self.condition = condition
        self.body = body
    
    def accept(self, visitor, o=None):
        return visitor.visit_while_stmt(self, o)
    
    def __str__(self):
        return f"WhileStmt({self.condition}, {self.body})"


class ForStmt(Stmt):
    """For-in loop statement."""
    
    def __init__(self, variable: str, iterable: 'Expr', body: 'BlockStmt'):
        super().__init__()
        self.variable = variable
        self.iterable = iterable
        self.body = body
    
    def accept(self, visitor, o=None):
        return visitor.visit_for_stmt(self, o)
    
    def __str__(self):
        return f"ForStmt({self.variable}, {self.iterable}, {self.body})"


class ReturnStmt(Stmt):
    """Return statement."""
    
    def __init__(self, value: Optional['Expr'] = None):
        super().__init__()
        self.value = value
    
    def accept(self, visitor, o=None):
        return visitor.visit_return_stmt(self, o)
    
    def __str__(self):
        return f"ReturnStmt({self.value})" if self.value else "ReturnStmt()"


class BreakStmt(Stmt):
    """Break statement."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_break_stmt(self, o)
    
    def __str__(self):
        return "BreakStmt()"


class ContinueStmt(Stmt):
    """Continue statement."""
    
    def __init__(self):
        super().__init__()
    
    def accept(self, visitor, o=None):
        return visitor.visit_continue_stmt(self, o)
    
    def __str__(self):
        return "ContinueStmt()"


class ExprStmt(Stmt):
    """Expression statement."""
    
    def __init__(self, expr: 'Expr'):
        super().__init__()
        self.expr = expr
    
    def accept(self, visitor, o=None):
        return visitor.visit_expr_stmt(self, o)
    
    def __str__(self):
        return f"ExprStmt({self.expr})"


class BlockStmt(Stmt):
    """Block statement (compound statement)."""
    
    def __init__(self, statements: List[Stmt]):
        super().__init__()
        self.statements = statements
    
    def accept(self, visitor, o=None):
        return visitor.visit_block_stmt(self, o)
    
    def __str__(self):
        stmts_str = ', '.join(str(stmt) for stmt in self.statements) if self.statements else ""
        stmts_part = f"[{stmts_str}]" if stmts_str else "[]"
        return f"BlockStmt({stmts_part})"


# ============================================================================
# Left-values (Assignable Expressions)
# ============================================================================

class LValue(ASTNode):
    """Base class for left-value expressions (assignable)."""
    pass


class IdLValue(LValue):
    """Identifier left-value."""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    def accept(self, visitor, o=None):
        return visitor.visit_id_lvalue(self, o)
    
    def __str__(self):
        return f"IdLValue({self.name})"


class ArrayAccessLValue(LValue):
    """Array access left-value."""
    
    def __init__(self, array: 'Expr', index: 'Expr'):
        super().__init__()
        self.array = array
        self.index = index
    
    def accept(self, visitor, o=None):
        return visitor.visit_array_access_lvalue(self, o)
    
    def __str__(self):
        return f"ArrayAccessLValue({self.array}, {self.index})"


# ============================================================================
# Expressions
# ============================================================================

class Expr(ASTNode):
    """Base class for all expression nodes."""
    pass


class BinaryOp(Expr):
    """Binary operation expression."""
    
    def __init__(self, left: Expr, operator: str, right: Expr):
        super().__init__()
        self.left = left
        self.operator = operator  # '+', '-', '*', '/', '%', '==', '!=', '<', '<=', '>', '>=', '&&', '||', '>>'
        self.right = right
    
    def accept(self, visitor, o=None):
        return visitor.visit_binary_op(self, o)
    
    def __str__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


class UnaryOp(Expr):
    """Unary operation expression."""
    
    def __init__(self, operator: str, operand: Expr):
        super().__init__()
        self.operator = operator  # '+', '-', '!'
        self.operand = operand
    
    def accept(self, visitor, o=None):
        return visitor.visit_unary_op(self, o)
    
    def __str__(self):
        return f"UnaryOp({self.operator}, {self.operand})"


class FunctionCall(Expr):
    """Function call expression."""
    
    def __init__(self, function: Expr, args: List[Expr]):
        super().__init__()
        self.function = function
        self.args = args
    
    def accept(self, visitor, o=None):
        return visitor.visit_function_call(self, o)
    
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args) if self.args else ""
        args_part = f"[{args_str}]" if args_str else "[]"
        return f"FunctionCall({self.function}, {args_part})"


class ArrayAccess(Expr):
    """Array access expression."""
    
    def __init__(self, array: Expr, index: Expr):
        super().__init__()
        self.array = array
        self.index = index
    
    def accept(self, visitor, o=None):
        return visitor.visit_array_access(self, o)
    
    def __str__(self):
        return f"ArrayAccess({self.array}, {self.index})"


class ArrayLiteral(Expr):
    """Array literal expression."""
    
    def __init__(self, elements: List[Expr]):
        super().__init__()
        self.elements = elements
    
    def accept(self, visitor, o=None):
        return visitor.visit_array_literal(self, o)
    
    def __str__(self):
        elements_str = ', '.join(str(elem) for elem in self.elements) if self.elements else ""
        elements_part = f"[{elements_str}]" if elements_str else "[]"
        return f"ArrayLiteral({elements_part})"


class Identifier(Expr):
    """Identifier expression."""
    
    def __init__(self, name: str):
        super().__init__()
        self.name = name
    
    def accept(self, visitor, o=None):
        return visitor.visit_identifier(self, o)
    
    def __str__(self):
        return f"Identifier({self.name})"


# ============================================================================
# Literal Expressions
# ============================================================================

class Literal(Expr):
    """Base class for literal expressions."""
    
    def __init__(self, value: Any):
        super().__init__()
        self.value = value


class IntegerLiteral(Literal):
    """Integer literal expression."""
    
    def __init__(self, value: int):
        super().__init__(value)
    
    def accept(self, visitor, o=None):
        return visitor.visit_integer_literal(self, o)
    
    def __str__(self):
        return f"IntegerLiteral({self.value})"


class FloatLiteral(Literal):
    """Float literal expression."""
    
    def __init__(self, value: float):
        super().__init__(value)
    
    def accept(self, visitor, o=None):
        return visitor.visit_float_literal(self, o)
    
    def __str__(self):
        return f"FloatLiteral({self.value})"


class BooleanLiteral(Literal):
    """Boolean literal expression."""
    
    def __init__(self, value: bool):
        super().__init__(value)
    
    def accept(self, visitor, o=None):
        return visitor.visit_boolean_literal(self, o)
    
    def __str__(self):
        return f"BooleanLiteral({self.value})"


class StringLiteral(Literal):
    """String literal expression."""
    
    def __init__(self, value: str):
        super().__init__(value)
    
    def accept(self, visitor, o=None):
        return visitor.visit_string_literal(self, o)
    
    def __str__(self):
        return f'StringLiteral({self.value!r})'
