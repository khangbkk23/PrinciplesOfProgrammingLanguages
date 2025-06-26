grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    
    return result

}


options{
	language=Python3;
}

program:    decllist EOF;

decllist:   decl decllist | decl;

decl:       vardecl | funcdecl;

vardecl: typ idlist SM;

funcdecl: typ ID paramdecl body;

body: '{' stmtlist '}';

stmtlist: stmt stmtlist |;

stmt: assign | call | return | vardecl;

assign: ID EQ expr SM;

call:   ID '(' exprlist ')' SM;

exprlist:   exprprime | ;

exprprime:  expr CM exprprime | expr;

return: 'return' expr SM;

paramdecl: '(' paramlist ')';

paramlist:  paramprime | ;

paramprime: param SM paramprime | param;

idlist: ID CM idlist | ID;

param:  typ idlist;

CM: ',';

SM: ';';

EQ: '=';

typ: 'int' | 'float';

ID: [a-zA-Z]+;

expr: expr '+' expr
    | expr '*' expr
    | expr '/' expr
    | expr '-' expr
    | INT_LIT
    | call;

INT_LIT:    [0-9]+;

FLOAT_LIT:  INT_LIT '.' INT_LIT;

WS: [ \t\r\n] -> skip ;

ERROR_CHAR: . {raise ErrorToken(self.text)};
