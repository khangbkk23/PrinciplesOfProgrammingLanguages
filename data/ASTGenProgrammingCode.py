class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.vardecls()) + 1  # Khong duoc quen EOFFFFFF!
    
    # vardecls: vardecl vardecltail;
    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())
    
    # vardecltail: vardecl vardecltail |;
    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        if ctx.getChildCount() == 0:
            return 0 # Xu ly trong truong hop co rong
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())
        
    # vardecl: mptype ids SM;
    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        mptype = self.visit(ctx.mptype()) # Dem so terminal node tren cay con mptype
        ids = self.visit(ctx.ids()) # Dem so terminal node tren cay con ids
        return mptype + ids + 1 # 1 la terminal not co san

    # mptype: INTTYPE | FLOATTYPE
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return 1

    # ids: ID CM ids | ID
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.getChildCount() == 1:
            return 1
        return 2 + self.visit(ctx.ids())
    
    C2: 
    class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.vardecls()) + 1
    
    # vardecls: vardecl vardecltail;
    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail()) + 1
    
    # vardecltail: vardecl vardecltail |;
    def visitVardecltail(self,ctx:MPParser.VardecltailContext): 
        if ctx.getChildCount() == 0:
            return 1 # Xu ly trong truong hop co rong
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail()) + 1
        
    # vardecl: mptype ids SM;
    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        mptype = self.visit(ctx.mptype()) # Dem so terminal node tren cay con mptype
        ids = self.visit(ctx.ids()) # Dem so terminal node tren cay con ids
        return mptype + ids + 1 # 1 la terminal not co san SM

    # mptype: INTTYPE | FLOATTYPE
    def visitMptype(self,ctx:MPParser.MptypeContext):
        return 1

    # ids: ID CM ids | ID
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.getChildCount() == 1:
            return 1  # ids → ID
        return 1 + self.visit(ctx.ids()) 
    
    
    C3:
class ASTGeneration(MPVisitor):
    
    # program: vardecls EOF;
    def visitProgram(self,ctx:MPParser.ProgramContext):
        return Program(self.visit(ctx.vardecls()))

    # vardecls: vardecl vardecltail;
    def visitVardecls(self,ctx:MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())
    
    # vardecltail: vardecl vardecltail |; Tra ve 1 list cua cac vardecl
    def visitVardecltail(self,ctx:MPParser.VardecltailContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())

    # vardecl: mptype ids SM;
    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        mptype = self.visit(ctx.mptype()) # Tra ve INTTYPE() : IntType()
        ids = self.visit(ctx.ids()) # List cac phan tu: [Id(a), Id(b),....]
        # res = []
        # for x in ids:
        #     res += VarDecl(x, mptype)
        return [VarDecl(x, mptype) for x in ids] # list comprehension for
        
# Viet truoc: 1
    # mptype: INTTYPE | FLOATTYPE;
    def visitMptype(self,ctx:MPParser.MptypeContext):
        if ctx.INTTYPE():
            return IntType() # Tra ve IntType() cua AST
        return FloatType()
    
    # ids: ID CM ids | ID
    def visitIds(self,ctx:MPParser.IdsContext):
        if ctx.getChildCount() == 1:
            return [Id(ctx.ID().getText())]# getText() de lay text cua AST
        else:
            ids = self.visit(ctx.ids())
            # Lay trong danh sach, noi voi cai san co
            return [Id(ctx.ID().getText())] + ids # ids la mang cac phan tu da vist! truoc do phai ep kieu ve mang []
C4:
class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.exp())
        
    def visitExp(self,ctx:MPParser.ExpContext):
        if ctx.ASSIGN():
            l = self.visit(ctx.term())
            ope = ctx.ASSIGN().getText()
            r = self.visit(ctx.exp())
            return Binary(ope, l, r)
        else:
            return self.visit(ctx.term())

    def visitTerm(self,ctx:MPParser.TermContext): 
        if ctx.COMPARE():
            l = self.visit(ctx.factor(0))
            ope = ctx.COMPARE().getText()
            r = self.visit(ctx.factor(1))
            return Binary(ope, l, r)
        else:
            return self.visit(ctx.factor(0))
            
    def visitFactor(self,ctx:MPParser.FactorContext):
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.factor())
            ope = ctx.ANDOR().getText()
            right = self.visit(ctx.operand())
            return Binary(ope, left, right)
        else:
            return self.visit(ctx.operand())

    def visitOperand(self,ctx:MPParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.BOOLIT():
            return BooleanLiteral(ctx.BOOLIT().getText() == "True")
        else:
            return self.visit(ctx.exp())

class ASTGeneration(MPVisitor):

    def visitProgram(self, ctx: MPParser.ProgramContext):
        return Program(self.visit(ctx.vardecls()))

    def visitVardecls(self, ctx: MPParser.VardeclsContext):
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())

    def visitVardecltail(self, ctx: MPParser.VardecltailContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.vardecl()) + self.visit(ctx.vardecltail())

    def visitVardecl(self, ctx: MPParser.VardeclContext): 
        mptype = self.visit(ctx.mptype())
        ids = self.visit(ctx.ids())
        return [VarDecl(x, mptype) for x in ids]

    def visitMptype(self, ctx: MPParser.MptypeContext):
        if ctx.INTTYPE():
            return IntType()
        return FloatType()

    def visitIds(self, ctx: MPParser.IdsContext):
        if ctx.getChildCount() == 1:
            return [Id(ctx.ID().getText())]
        ids = self.visit(ctx.ids())
        return [Id(ctx.ID().getText())] + ids

C5: 
class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext:
        # acc: ban dau la 1 danh sach rong
        # cur: vardecl dau tien
        # ctx.vardecl(): list criteria
        # Ket qua tra ve la 1 danh sach cac VarDecl cuoi cung
        return Program(reduce(lambda acc, cur: acc + self.visit(cur), ctx.vardecl(), []))

    def visitVardecl(self,ctx:MPParser.VardeclContext): 
        var_type = self.visit(ctx.mptype())
        id_list = self.visit(ctx.ids())
        return [VarDecl(id, var_type) for id in id_list]

    def visitMptype(self,ctx:MPParser.MptypeContext):
        if ctx.INTTYPE():
            return IntType()
        return FloatType()
        
    def visitIds(self,ctx:MPParser.IdsContext):
        id_list = [Id(x.getText()) for x in ctx.ID()]
        return id_list

C6:
class ASTGeneration(MPVisitor):

    def visitProgram(self,ctx:MPParser.ProgramContext):
        return self.visit(ctx.exp())

    def visitExp(self,ctx:MPParser.ExpContext):
        terms = ctx.term()
        assigns = ctx.ASSIGN()
        
        if not assigns:
            return self.visit(terms[-1])

        right = self.visit(terms[-1])
        for i in range(len(assigns) - 1, -1, -1):
            left = self.visit(terms[i])
            op = assigns[i].getText()
            right = Binary(op, left, right)
        return right

    def visitTerm(self,ctx:MPParser.TermContext): 
        if ctx.COMPARE():
            left = self.visit(ctx.factor(0))
            right = self.visit(ctx.factor(1))
            op = ctx.COMPARE().getText()
            return Binary(op, left, right)
        else:
            return self.visit(ctx.factor(0))

    def visitFactor(self,ctx:MPParser.FactorContext):
        operand = ctx.operand()
        andor = ctx.ANDOR()

        result = self.visit(operand[0])
        for i in range(len(andor)):
            op = andor[i].getText()
            right = self.visit(operand[i + 1])
            result = Binary(op, result, right)
        return result

    def visitOperand(self,ctx:MPParser.OperandContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.BOOLIT():
            return BooleanLiteral(ctx.BOOLIT().getText() == "True")
        else:
            return self.visit(ctx.exp())
