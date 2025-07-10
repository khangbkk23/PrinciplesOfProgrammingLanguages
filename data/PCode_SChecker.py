# C1:
# Let AST of a programming language be defined as follows:

class Program: #decl:List[Decl]

class Decl(ABC): #abstract class

class VarDecl(Decl): #name:str,typ:Type

class ConstDecl(Decl): #name:str,val:Lit

class Type(ABC): #abstract class

class IntType(Type)

class FloatType(Type)

class Lit(ABC): #abstract class

class IntLit(Lit): #val:int

and exception RedeclaredDeclaration:

class RedeclaredDeclaration(Exception): #name:str
# Implementation with list
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        o = []
        for decl in ctx.decl:
            self.visit(decl, o)
        

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredDeclaration(ctx.name)
        o += [ctx.name]

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredDeclaration(ctx.name)
        o += [ctx.name]

    def visitIntType(self,ctx:IntType,o:object):
        pass # Ko viet

    def visitFloatType(self,ctx:FloatType,o:object):
        pass # Ko viet

    def visitIntLit(self,ctx:IntLit,o:object):
        pass # Ko viet
    
# Implementation with Functional Programming
from functools import reduce
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        reduce (lambda acc, cur: self.visit(cur, acc), ctx.decl, [])
        
    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredDeclaration(ctx.name)
        return o + [ctx.name] # Muc dich: de ko lam bien doi danh sach o.

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredDeclaration(ctx.name)
        return o + [ctx.name]

    def visitIntType(self,ctx:IntType,o:object):
        pass # Ko viet

    def visitFloatType(self,ctx:FloatType,o:object):
        pass # Ko viet

    def visitIntLit(self,ctx:IntLit,o:object):
        pass # Ko viet

# C2:
class Program: #decl:List[Decl]

class Decl(ABC): #abstract class

class VarDecl(Decl): #name:str,typ:Type

class ConstDecl(Decl): #name:str,val:Lit

class Type(ABC): #abstract class

class IntType(Type)

class FloatType(Type)

class Lit(ABC): #abstract class

class IntLit(Lit): #val:int

class RedeclaredVariable(Exception): #name:str

class RedeclaredConstant(Exception): #name:str
    
# Implement with functional programming
from functools import reduce
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        reduce (lambda acc, cur: self.visit(cur, acc), ctx.decl, [])
        
    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return o + [ctx.name] # Muc dich: de ko lam bien doi danh sach o.

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return o + [ctx.name]

    def visitIntType(self,ctx:IntType,o:object):
        pass # Ko viet

    def visitFloatType(self,ctx:FloatType,o:object):
        pass # Ko viet

    def visitIntLit(self,ctx:IntLit,o:object):
        pass # Ko viet
    
C3: 
    