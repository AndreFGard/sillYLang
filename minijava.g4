grammar minijava;

program: classDecl*;


public: 'public'; static: 'static'; private: 'private'; extends: 'extends';

classDecl: CLASS VAR (extends VAR)? LBRACE memberDecl* RBRACE;
memberDecl: (public | private)? static?  (methodDecl |( varDecl SEMICOLON));

methodDecl: VAR VAR LPAREN argSignature RPAREN LBRACE statement* RBRACE;
functionCall: VAR LPAREN arglist RPAREN;

statement: (expr | varDecl) SEMICOLON;

dimensions: ('[' ']');
varDecl: VAR dimensions* VAR dimensions* ;

arglist:( expr (COMMA expr )*)? ;
argSignature: (varDecl (COMMA varDecl )*)? ;

subexpr: LPAREN expr RPAREN; //for disambiguation
basicExpr: functionCall | subexpr | VAR ;
exprPostfix: DOT (VAR | functionCall);

expr: basicExpr exprPostfix*;



// Regras do Lexer
CLASS: 'class';


LPAREN: '(' ;
RPAREN: ')' ;
WS: [ \t\r\n]+ -> skip ;
LBRACE: '{' ;
RBRACE: '}' ;
COMMA: ',' ;
SEMICOLON: ';';
LBRACK: '[';
RBRACK: ']';
DOT: '.';

VAR: [a-zA-Z0-9?+=*]+ ; //bellow the keywords!!!