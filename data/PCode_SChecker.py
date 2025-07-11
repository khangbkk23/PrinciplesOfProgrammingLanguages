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
from functools import reduce
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.decl, [])

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        o += [ctx.name]
        return o

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        o += [ctx.name]
        return o

    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        o += [ctx.name]
        local_o = []
        for param in ctx.param:
            if param.name in local_o:
                raise RedeclaredVariable(param.name)
            local_o += [param.name]
        
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.body, local_o)
        return o

    def visitIntType(self,ctx:IntType,o:object):pass

    def visitFloatType(self,ctx:FloatType,o:object):pass

    def visitIntLit(self,ctx:IntLit,o:object):pass
# Immutable ways:
from functools import reduce
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.decl, [])

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return o + [ctx.name]
        
    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return o + [ctx.name]

    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        local_o = []
        for param in ctx.param:
            if param.name in local_o:
                raise RedeclaredVariable(param.name)
            local_o += [param.name]
        
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.body, local_o)
        return o + [ctx.name]
        

    def visitIntType(self,ctx:IntType,o:object):
        pass

    def visitFloatType(self,ctx:FloatType,o:object):
        pass

    def visitIntLit(self,ctx:IntLit,o:object):
        pass
### Cach cua thay 
from functools import reduce
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o:object):
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.decl, [])

    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return o + [ctx.name]

    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return o +[ctx.name]

    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.param + ctx.body, [])
        return o + [ctx.name]

    def visitIntType(self,ctx:IntType,o:object):
        pass

    def visitFloatType(self,ctx:FloatType,o:object):
        pass

    def visitIntLit(self,ctx:IntLit,o:object):
        pass
C4:
from functools import reduce

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o:object):
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.decl, [])
    
    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o:
            raise RedeclaredVariable(ctx.name)
        return o + [ctx.name]
    
    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o:
            raise RedeclaredConstant(ctx.name)
        return o + [ctx.name]
    
    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o:
            raise RedeclaredFunction(ctx.name)
        new_global = o + [ctx.name]
        local_o = []
        
        for param in ctx.param:
            if param.name in local_o:
                raise RedeclaredVariable(param.name)
            local_o += [param.name]
        
        local_scope = local_o[:]
        for decl in ctx.body[0]:
            if isinstance(decl, FuncDecl):
                if decl.name in local_scope:
                    raise RedeclaredFunction(decl.name)
                local_scope += [decl.name]
                self.visit(decl, new_global + local_scope[:-1])
            else:
                local_scope = self.visit(decl, local_scope)
                
        for expr in ctx.body[1]:
            self.visit(expr, (local_scope, new_global))
        return new_global
    
    def visitIntType(self,ctx:IntType,o:object):
        pass
    
    def visitFloatType(self,ctx:FloatType,o:object):
        pass
    
    def visitIntLit(self,ctx:IntLit,o:object):
        pass
    
    def visitId(self,ctx:Id,o:object):
        l, g = o
        if ctx.name not in l and ctx.name not in g:
            raise UndeclaredIdentifier(ctx.name)
        
# Using stack
# Dinh stack: moi truong tham khao cuc bo
# Tu dinh toi day: Moi truong tham khao ko cuc bo
# Day stack: moi truong tham khao toan cuc

# Xu ly: Khai bao: so sanh voi dinh stack (MTTK cuc bo)
# Xu ly: Su dung: kiem tra dinh -> day (co o dau thi dung o do)
from functools import reduce

class StaticCheck(Visitor):
    def visitProgram(self,ctx:Program,o:object):
        reduce(lambda acc, cur: self.visit(cur, acc), ctx.decl, [[]])
    
    def visitVarDecl(self,ctx:VarDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredVariable(ctx.name)
        return [o[0] + [ctx.name]] + o[1:]
    
    def visitConstDecl(self,ctx:ConstDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredConstant(ctx.name)
        return [o[0] + [ctx.name]] + o[1:]
    
    def visitFuncDecl(self,ctx:FuncDecl,o:object):
        if ctx.name in o[0]:
            raise RedeclaredFunction(ctx.name)
        new_env = [o[0] + [ctx.name]] + o[1:]
        env = reduce(lambda acc, cur: self.visit(cur, acc), ctx.param + ctx.body[0], [[]] + new_env)
        list(map(lambda x: self.visit(x, env), ctx.body[1]))
        return new_env
                    
    def visitIntType(self,ctx:IntType,o:object):
        pass
    
    def visitFloatType(self,ctx:FloatType,o:object):
        pass
    
    def visitIntLit(self,ctx:IntLit,o:object):
        pass
    
    def visitId(self,ctx:Id,o:object):
        for env in o:
            if ctx.name in env:
                return
        raise UndeclaredIdentifier(ctx.name)