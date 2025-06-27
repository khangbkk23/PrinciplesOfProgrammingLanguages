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