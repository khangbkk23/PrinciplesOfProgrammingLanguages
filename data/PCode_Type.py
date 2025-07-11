# Neu de ko cho thi ta phai tu di gia su
C1:
class StaticCheck(Visitor):

    def visitBinOp(self,ctx:BinOp,o):
        e1t = self.visit(ctx.e1, o)
        e2t = self.visit(ctx.e2, o)
        if ctx.op in ["+", "-", "*"]:
            if e1t == 'bool' or e2t == 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'float' if e1t == 'float' or e2t == 'float' else 'int'
        
        if ctx.op in ["/"]:
            if e1t == 'bool' or e2t == 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'float'
            
        if ctx.op in ["&&", "||"]:
            if e1t != 'bool' or e2t != 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'bool'
        
        if ctx.op in ["==", "!=", ">", "<"]:
            if e1t != e2t :
                raise TypeMismatchInExpression(ctx)
            return 'bool'

    def visitUnOp(self, ctx: UnOp, o):
        e1t = self.visit(ctx.e, o)
        if ctx.op == "!":
            if e1t != 'bool':
                raise TypeMismatchInExpression(ctx)
            return 'bool'
        
        if ctx.op == "-":
            if e1t == 'bool':
                raise TypeMismatchInExpression(ctx)
            return e1t

    def visitIntLit(self,ctx:IntLit,o):
        return 'int'

    def visitFloatLit(self,ctx,o):
        return 'float'

    def visitBoolLit(self,ctx,o):
        return 'bool'

C2:
