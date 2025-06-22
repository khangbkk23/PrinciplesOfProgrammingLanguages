"""
Semantic Analysis Package for HLang

This package provides comprehensive static semantic analysis for HLang programs,
including type checking, scope management, and semantic constraint verification.
"""

from .static_error import *
from .static_checker import StaticChecker

__all__ = [
    # Static Error Classes
    'StaticError',
    'Redeclared', 
    'Undeclared',
    'TypeMismatchInExpression',
    'TypeMismatchInStatement', 
    'TypeCannotBeInferred',
    'NoDefinition',
    'MustInLoop',
    'NoEntryPoint',
    'CannotAssignToConstant',
    'ArrayIndexOutOfBounds',
    'InvalidArraySize',
    'ReturnNotInFunction',
    'MissingReturnStatement',
    'InvalidBreakTarget',
    'InvalidContinueTarget',
    'IncompatibleTypes',
    'InvalidUnaryOperation',
    'InvalidBinaryOperation',
    
    # Helper Classes (if any exist in static_checker)
    # Note: All symbol management is now internal to StaticChecker
    
    # Main Checker
    'StaticChecker'
]
