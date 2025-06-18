grammar HLang;

@lexer::header {
from .lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

program  : decl+ EOF ;

decl: funcdecl | vardecl  ;

vardecl: 'var' ID 'int' ('=' exp)? ';' ;

funcdecl: 'func' ID '(' ')' block ';' ;

block : '{' stmt+  '}' ;

stmt: funcall | vardecl;

funcall: ID '(' exp ')' ';' ;

exp:  ID | INTLIT | FLOATLIT;

ID: [a-zA-Z]+;

INTLIT: [0-9]+;

FLOATLIT: [0-9]+ '.' [0-9]+;

NL: '\n' -> skip; //skip newlines

WS : [ \t\r]+ -> skip ; // skip spaces, tabs 

ERROR_CHAR: .;
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;