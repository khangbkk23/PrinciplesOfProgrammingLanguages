"""
Visitor interface for AST traversal in HLang programming language.
This module defines the abstract visitor pattern interface for traversing
and processing AST nodes.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nodes import *


class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""
    
    # Program and declarations
    @abstractmethod
    def visit_program(self, node: 'Program'): pass
    
    @abstractmethod
    def visit_const_decl(self, node: 'ConstDecl'): pass
    
    @abstractmethod
    def visit_func_decl(self, node: 'FuncDecl'): pass
    
    @abstractmethod
    def visit_param(self, node: 'Param'): pass
    
    # Type system
    @abstractmethod
    def visit_int_type(self, node: 'IntType'): pass
    
    @abstractmethod
    def visit_float_type(self, node: 'FloatType'): pass
    
    @abstractmethod
    def visit_bool_type(self, node: 'BoolType'): pass
    
    @abstractmethod
    def visit_string_type(self, node: 'StringType'): pass
    
    @abstractmethod
    def visit_void_type(self, node: 'VoidType'): pass
    
    @abstractmethod
    def visit_array_type(self, node: 'ArrayType'): pass
    
    # Statements
    @abstractmethod
    def visit_var_decl(self, node: 'VarDecl'): pass
    
    @abstractmethod
    def visit_assignment(self, node: 'Assignment'): pass
    
    @abstractmethod
    def visit_if_stmt(self, node: 'IfStmt'): pass
    
    @abstractmethod
    def visit_while_stmt(self, node: 'WhileStmt'): pass
    
    @abstractmethod
    def visit_for_stmt(self, node: 'ForStmt'): pass
    
    @abstractmethod
    def visit_return_stmt(self, node: 'ReturnStmt'): pass
    
    @abstractmethod
    def visit_break_stmt(self, node: 'BreakStmt'): pass
    
    @abstractmethod
    def visit_continue_stmt(self, node: 'ContinueStmt'): pass
    
    @abstractmethod
    def visit_expr_stmt(self, node: 'ExprStmt'): pass
    
    @abstractmethod
    def visit_block_stmt(self, node: 'BlockStmt'): pass
    
    # Left-values
    @abstractmethod
    def visit_id_lvalue(self, node: 'IdLValue'): pass
    
    @abstractmethod
    def visit_array_access_lvalue(self, node: 'ArrayAccessLValue'): pass
    
    # Expressions
    @abstractmethod
    def visit_binary_op(self, node: 'BinaryOp'): pass
    
    @abstractmethod
    def visit_unary_op(self, node: 'UnaryOp'): pass
    
    @abstractmethod
    def visit_function_call(self, node: 'FunctionCall'): pass
    
    @abstractmethod
    def visit_array_access(self, node: 'ArrayAccess'): pass
    
    @abstractmethod
    def visit_array_literal(self, node: 'ArrayLiteral'): pass
    
    @abstractmethod
    def visit_identifier(self, node: 'Identifier'): pass
    
    # Literals
    @abstractmethod
    def visit_integer_literal(self, node: 'IntegerLiteral'): pass
    
    @abstractmethod
    def visit_float_literal(self, node: 'FloatLiteral'): pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: 'BooleanLiteral'): pass
    
    @abstractmethod
    def visit_string_literal(self, node: 'StringLiteral'): pass
