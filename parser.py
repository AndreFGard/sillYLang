from enum import member
from typing import Dict
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
from minijavaLexer import minijavaLexer
from minijavaParser import minijavaParser
from AST import *
class MinijavaVisitor:
    """😛😛😛\n
    A superset of the professor's provided grammar,
    a subset of minijava,
    the cure for the clojure-sick"""
    def __init__(self):
        ...
    
    def visit(self, ctx):
        if isinstance(ctx, minijavaParser.MethodDeclContext):
            return self.visitMethodDecl(ctx)
        elif isinstance(ctx, minijavaParser.VarDeclContext):
            return self.visitVarDecl(ctx)
        elif isinstance(ctx, minijavaParser.ProgramContext):
            return self.visitProgram(ctx)
        else:
             print(f"Unexpected generic visit attempt of type {ctx}")


    def visitProgram(self, ctx: minijavaParser.ProgramContext):
        classes = [self.visitClassDecl(c) for c in ctx.classDecl() if c]
        return Program(None, classes=classes) #type:ignore

    def __visitArglist(self, ctx: minijavaParser.ArglistContext):
        return [self.visitExpr(x) for x in ctx.expr()]

    def __visitArglistSignature(self, ctx: minijavaParser.ArgSignatureContext):
        return [self.visitVarSignature(c) for c in ctx.children]

    def visitDimensions(self,ctx):
        if ctx.dimensions(): return 1 + self.visitDimensions(ctx.dimensions())
        return 0

    def visitVarDecl(self, ctx:minijavaParser.VarDeclContext):
        return VarDecl(ctx.VAR(1), ctx.VAR(0), dimensions=len(ctx.dimensions()))

    def visitVarSignature(self, ctx):
        return VarSignature(ctx.VAR(1), ctx.VAR(0), dimensions=0)

    def visitFunctionCall(self, ctx: minijavaParser.FunctionCallContext):
        return FunctionCall(ctx.VAR(), self.__visitArglist(ctx.arglist()) )

    def visitBasicExpr(self, ctx: minijavaParser.BasicExprContext):
        if ctx.VAR():
            return Var(ctx.VAR().getText())
        elif ctx.functionCall():
            return self.visitFunctionCall(ctx.functionCall())
        elif ctx.subexpr():
            return self.visitExpr(self.visitExpr(ctx.subexpr().expr()))
        else: raise Exception(f"Unexpected basic expression: {ctx.getText()}")

    def visitExpr(self, ctx: minijavaParser.ExprContext):
        
        def f(x):
            if x.functionCall():
                return self.visitFunctionCall(x.functionCall())
            else:
                return Var(x.VAR().getText())


        l = list(map(f, ctx.exprPostfix()))
        x = self.visitBasicExpr(ctx.basicExpr())
        return Expr(x,l) 

    def visitStatement(self, ctx:minijavaParser.StatementContext):
        if ctx.varDecl():
            x= self.visitVarDecl(ctx.varDecl())
        elif ctx.expr(): x= self.visitExpr(ctx.expr())
        else: raise
        return Statement(x)

    def visitMethodDecl(self, ctx: minijavaParser.MethodDeclContext, visibility=Visibility.PUBLIC):
        return MethodDecl(
            name=Var(ctx.VAR(0).getText()),
            visibility=visibility,
            returnType=Var(ctx.VAR(1).getText()),#type:ignore
            params=self.__visitArglistSignature(ctx.argSignature()),
            body = [self.visitStatement(c) for c in ctx.statement()]
        )


    def visitMemberDecl(self,ctx:minijavaParser.MemberDeclContext):
        if ctx.private(): vis = Visibility.PRIVATE
        else: vis = Visibility.PUBLIC

        memb: VarDecl|MethodDecl = self.visit(ctx.methodDecl() or ctx.varDecl())#type: ignore
        memb.visibility = vis 
        return memb
        

    def visitClassDecl(self, ctx:minijavaParser.ClassDeclContext):
        id = Var(ctx.VAR(0).getText())
        vars,methods = [],[]
        for memb in ctx.memberDecl():
            memb = self.visitMemberDecl(memb)
            if isinstance(memb, minijavaParser.MethodDeclContext):
                methods.append(memb)
            else:
                vars.append(memb)
        return ClassDecl(
            id,
            extends=Var(ctx.VAR(1).getText()) if len(ctx.VAR()) > 1 else None,
            members=vars + methods
        )


from sys import argv

def main():
    visitor = MinijavaVisitor()

    cont = True
    while(cont):
        if len(argv) > 1:
            expression = open(argv[1], 'r').read()
            cont = False
        else:
            expression = input('manda: ')

        lexer = minijavaLexer(InputStream(expression))
        stream = CommonTokenStream(lexer)
        parser = minijavaParser(stream)
        tree = parser.program()
        result = visitor.visit(tree)
        print(result)


if __name__ == '__main__':
    main()
