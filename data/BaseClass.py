class AST(ABC): # Lớp cha (Abstract class)
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    @abstractmethod
    def accept(self, v, param):
        return v.visit(self, param)

class Type(AST):    # Là một lớp abstract
    __metaclass__ = ABCMeta
    pass

class IntType(Type): # Kế thừa từ lớp Type
    def __str__(self):
        return "IntType"

    def accept(self, v, param): 
        return v.visitIntType(self, param)

class FloatType(Type): # Kế thừa từ lớp Type
    def __str__(self):
        return "FloatType"

    def accept(self, v, param):
        return v.visitFloatType(self, param)


class Program(AST): # Tim class program doc truoc co bao nhieu truong du lieu
    #decl:list(Decl) # Mot chương trình bao gồm danh sách các khai báo (declarations)
    def __init__(self, decl):
        self.decl = decl
    
    def __str__(self):
        return "Program([" + ','.join(str(i) for i in self.decl) + "])"
    
    def accept(self, v: Visitor, param):
        return v.visitProgram(self, param)

class Decl(AST): # Lớp abstrack (ko có gì hết, hoặc chỉ có metadata)
    __metaclass__ = ABCMeta
    pass

class VarDecl(Decl): # Lớp này kế thừa từ Decl
    #variable:Id
    #varType: Type
    def __init__(self, variable, varType):
        self.variable = variable
        self.varType = varType

    def __str__(self):
        return "VarDecl(" + str(self.variable) + "," + str(self.varType) + ")"

    def accept(self, v, param):
        return v.visitVarDecl(self, param)


class Id(AST):
    #name:string
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Id(" + self.name + ")"

    def accept(self, v, param):
        return v.visitId(self, param)