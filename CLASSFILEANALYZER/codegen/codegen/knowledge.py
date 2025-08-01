##* C3:
    def visitBinExpr(self, ctx, o):
        op = ctx.op
        e1_code, e1_type = self.visit(ctx.e1, o)
        e2_code, e2_type = self.visit(ctx.e2, o)

        if op in ['+', '-', '*', '/']:
            code = e1_code + e2_code
            if op == '+':
                code += self.emit.emitADDOP('+', IntType(), o.frame)
            elif op == '-':
                code += self.emit.emitADDOP('-', IntType(), o.frame)
            elif op == '*':
                code += self.emit.emitMULOP('*', IntType(), o.frame)
            elif op == '/':
                code += self.emit.emitMULOP('/', IntType(), o.frame)
            return code, IntType()
        
        elif op in ['+.', '-.', '*.', '/.']:
            code = e1_code + e2_code
            if op == '+.':
                code += self.emit.emitADDOP('+', FloatType(), o.frame)
            elif op == '-.':
                code += self.emit.emitADDOP('-', FloatType(), o.frame)
            elif op == '*.':
                code += self.emit.emitMULOP('*', FloatType(), o.frame)
            elif op == '/.':
                code += self.emit.emitMULOP('/', FloatType(), o.frame)
            return code, FloatType()
##* C4:
    def visitBinExpr(self, ctx, o):
        e1c, e1t = self.visit(ctx.e1, o)
        e2c, e2t = self.visit(ctx.e2, o)
        
        if type(e1t) is type(e2t):
            rt = e1t
        elif type(e1t) is IntType and type (e2t) is FloatType:
            e1c += self.emit.emitI2F(o.frame)
            rt = FloatType()
        else:
            e2c += self.emit.emitI2F(o.frame)
            rt = FloatType()
            
        if ctx.op in ['+', '-']:
            opc = self.emit.emitADDOP(ctx.op, rt, o.frame)
            
        elif ctx.op == '*':
            opc = self.emit.emitMULOP(ctx.op, rt, o.frame)
            
        elif ctx.op == '/':
            e1c += self.emit.emit.F2I(o.frame)
            e2c += self.emit.emit.F2I(o.frame)
            rt = FloatType()
            opc = self.emit.emitMULOP(ctx.op, rt, o.frame)
        
        else:
            opc = self.emit.emitRELOP(ctx.op, rt, o.frame)
            rt = BoolType()

        return e1c + e2c + opc, rt

##* C5:
    def visitId(self, ctx, o):
        sym = next(filter(lambda x: x.name == ctx.name, o.sym), False) # Find symbol in o.sym that has name == ctx.name
        if type(sym.value) is Index:
            code = self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, o.frame)
        else:
            code = self.emit.emitGETSTATIC(sym.value.value + "." + sym.name, sym.mtype, o.frame)
            # sym.value.value + "." + sym.name: tim ten lop trong cua static, tạo ra tên đầy đủ của biến toàn cục, vì:

            # sym.value.value là tên lớp chứa biến

            #sym.name là tên của biến


        
        return code, sym.mtype

##* C6:
    def visitId(self, ctx, o):
        sym = next(filter(lambda x: x.name == ctx.name, o.sym), False) # Find symbol in o.sym that has name == ctx.name
        if o.isLeft:
            if type(sym.value) is Index:
                code = self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitPUTSTATIC(sym.value.value + "." + sym.name, sym.mtype, o.frame)
        else:
            if type(sym.value) is Index:
                code = self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitGETSTATIC(sym.value.value + "." + sym.name, sym.mtype, o.frame)
        
        return code, sym.mtype

##** CODE GEN 2=======================================================================================
##* C1:
    def visitVarDecl(self, ctx, o):
        if o.frame is None:
            # lexemes: name of attribute
            code = self.emit.emitATTRIBUTE(ctx.name, ctx.typ, False)
            sym = Symbol(ctx.name, ctx.typ, CName(self.className))
        else:
            # index: chua co => lam viec voi frame
            idx = o.frame.getNewIndex()
            # fromLabel:
            fL = o.frame.getStartLabel()
            # toLabel:
            eL = o.frame.getEndLabel()
            code = self.emit.emitVAR(idx, ctx.name, ctx.typ, fL, eL)
            # Duoi day do co None nen ko la static duoc ma phai la local (dung Index)
            sym = Symbol(ctx.name, ctx.typ, Index(idx))
        
        self.emit.printout(code)
        return sym
##* C2:
    def visitAssign(self, ctx, o):
        # Can nap vao 1 doi tuong rhs hay lhs (chỉ hướng) và một lớp access để truy cập đến Expr
        rc, rt = self.visit(ctx.rhs, Access(o.frame, o.sym, False))
        self.emit.printout(rc)
        lc, lt = self.visit(ctx.lhs, Access(o.frame, o.sym, True))
        self.emit.printout(lc)
        
        return

##* C3:
    def visitIf(self, ctx, o):
        if ctx.estmt is None:
            # Sinh new label
            fL = o.frame.getNewLabel() # sinh new label
            # SInh ma cho expr (cap tu stmt den expr -> can Access)
            ec, et = self.visit(ctx.expr, Access(o.frame, o.sym, False)) # Đọc => isLeft = False
            self.emit.printout(ec)
            
            # Nhay den fL neu False
            code = self.emit.emitIFFALSE(fL, o.frame)
            self.emit.printout(code)
            
            # Sinh ma cho stmt
            self.visit(ctx.tstmt, o)
            
            # Dat label tai day
            code = self.emit.emitLABEL(fL, o.frame)
            self.emit.printout(code)
        else:
            # Sinh label moi eL, fL
            fL = o.frame.getNewLabel()
            eL = o.frame.getNewLabel()
            
            # Sinh expr
            ec, et = self.visit(ctx.expr, Access(o.frame, o.sym, False))
            self.emit.printout(ec)
            
            # Nhay den fL neu False
            self.emit.printout(self.emit.emitIFFALSE(fL, o.frame))
            
            # Sinh ma cho stmt
            self.visit(ctx.tstmt, o)
            
            # Nhay den eL moi TH
            self.emit.printout(self.emit.emitGOTO(eL, o.frame))
            
            # Dat FL tai day
            self.emit.printout(self.emit.emitLABEL(fL, o.frame))
            
            # Sinh ma estmt
            self.visit(ctx.estmt, o)
            
            # Dat EL tai day
            self.emit.printout(self.emit.emitLABEL(eL, o.frame))
            
            return

##* C4: 
    def visitWhile(self, ctx, o):
        
        o.frame.enterLoop()
        # Sinh new label
        contL = o.frame.getContinueLabel()
        breakL = o.frame.getBreakLabel()
        # Dat contL
        self.emit.printout(self.emit.emitLABEL(contL, o.frame))
        
        # Sinh ma cho expr
        ec, et = self.visit(ctx.expr, Access(o.frame, o.sym, False))
        self.emit.printout(ec)
        
        # Nhay den breakL neu False
        self.emit.printout(self.emit.emitIFFALSE(breakL, o.frame))
        
        # Sinh ma cho stmt
        self.visit(ctx.stmt, o)
        
        # Nhay toi contL trong moi TH
        self.emit.printout(self.emit.emitGOTO(contL, o.frame))
        
        # Dat breakL tai day
        self.emit.printout(self.emit.emitLABEL(breakL, o.frame))
        
        o.frame.exitLoop()
        return None

##* C5:
    def visitWhile(self, ctx, o):
        
        o.frame.enterLoop()
        
        # Sinh new label
        contL = o.frame.getContinueLabel()
        breakL = o.frame.getBreakLabel()
        startL = o.frame.getNewLabel()
        
        # Dat startL tai day
        self.emit.printout(self.emit.emitLABEL(startL, o.frame))
        
        # Sinh ma cho stmt
        self.visit(ctx.stmt, o)
        
        # Nhay den contL
        self.emit.printout(self.emit.emitLABEL(contL, o.frame))
        
        # Sinh ma cho expr
        ec, et = self.visit(ctx.expr, Access(o.frame, o.sym, False))
        self.emit.printout(ec)
        
        # Nhay den startL neu True
        self.emit.printout(self.emit.emitIFTRUE(startL, o.frame))
        
        # Dat breakL tai day
        self.emit.printout(self.emit.emitLABEL(breakL, o.frame))
        
        o.frame.exitLoop()

##* C6: For

====================================CODE GEN 3=====
##* C1: While co else
    def visitWhile(self, ctx, o):
        
        o.frame.enterLoop()
        # Sinh new label
        contL = o.frame.getContinueLabel()
        breakL = o.frame.getBreakLabel()
        elseL = o.frame.getNewLabel()
        # Dat contL
        self.emit.printout(self.emit.emitLABEL(contL, o.frame))
        
        # Sinh ma cho expr
        ec, et = self.visit(ctx.expr, Access(o.frame, o.sym, False))
        self.emit.printout(ec)
        
        # Nhay den elseL neu False
        self.emit.printout(self.emit.emitIFFALSE(elseL, o.frame))
        
        # Sinh ma cho stmt
        self.visit(ctx.tstmt, o)
        
        # Nhay toi contL trong moi TH
        self.emit.printout(self.emit.emitGOTO(contL, o.frame))
        
        # Dat elseL tai day
        self.emit.printout(self.emit.emitLABEL(elseL, o.frame))
        
        # Sinh ma cho estmt
        self.visit(ctx.estmt, o)
        
        # Dat breakL tai day
        self.emit.printout(self.emit.emitLABEL(breakL, o.frame))
        
        o.frame.exitLoop()
        return None

##* C2: For
    def visitFor(self, ctx, o):
        o.frame.enterLoop()
        
        # Sinh label moi
        startL = o.frame.getNewLabel()
        contL = o.frame.getContinueLabel()
        breakL = o.frame.getBreakLabel()
        
        # idx = ini, tao doi tuong bang phep gan (tu tao luon)
        ini = Assign(ctx.idx, ctx.ini)
        self.visit(ini, o)
        
        # Dat startL
        self.emit.printout(self.emit.emitLABEL(startL, o.frame))
    
        # tao doi tuong cond cap EXPR
        cond = BinExpr("<=", ctx.idx, ctx.end)
        condc, condt = self.visit(cond, Access(o.frame, o.sym, False))
        self.emit.printout(condc)
        
        # Nhay den breakL neu cond False
        self.emit.printout(self.emit.emitIFFALSE(breakL, o.frame))
        
        # sinh ma cho stmt
        self.visit(ctx.stmt, o)
        
        # Dat contL
        self.emit.printout(self.emit.emitLABEL(contL, o.frame))
    
        # Tao doi tuong upd va gan
        upd = BinExpr("+", ctx.idx, ctx.upd)
        updStmt = Assign(ctx.idx, upd)
        self.visit(updStmt, o)
    
        # Nhay toi startL trong moi TH
        self.emit.printout(self.emit.emitGOTO(startL, o.frame))
    
        # Dat breakL
        self.emit.printout(self.emit.emitLABEL(breakL, o.frame))
    
        o.frame.exitLoop()
        return None

##* For theo flowchart, giong 95% de cuoi ky harmony
