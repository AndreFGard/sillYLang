"""
astminijava.py
Este arquivo deve conter a definição das classes que representam a Árvore de Sintaxe Abstrata (AST)
para o subconjunto da linguagem MiniJava definido na Atividade da disciplina IF688.
"""

import enum
from typing import ClassVar, List, Optional
import textwrap
from typing import Union

#from antlr4.atn import ATNConfig

class ASTNode:
    pass


class Visibility(enum.Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    STATIC = "static"
    FINAL = "final"


class Var(ASTNode):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"{self.name}"

class simpleType:
    INT = Var('int')

class Type(ASTNode):
    def __init__(self, type:Var, dimensions = 0):
        self.type = type
        self.dimensions = dimensions

    def __str__(self):
        return f"{self.type}"

class VarSignature(ASTNode):
    def __init__(self, identifier:Var, type: Var, dimensions:int=0):
        self.identifier = identifier
        self.Type = Type(type, dimensions)
    def __str__(self):
        return f"{self.Type}@{self.identifier}"

#composition instead of inheritance
class VarDecl(ASTNode):
    def __init__(self, identifier, type:Var, static=False,dimensions=0):
        self.VarSignature = VarSignature(identifier, type, dimensions=dimensions)
        self.static = static
        self.visibility = Visibility.PUBLIC #can be altered by derived classes
        self.dimensions = dimensions

    def __repr__(self):
        return f"DECL({self.VarSignature}{'[]'*self.dimensions})"

class Statement(): #type:ignore
    pass

class MethodDecl(ASTNode):
    def __init__(self, name, visibility: Visibility, returnType:Var, params:List[VarSignature]=[], body:list[Statement]=[] ):
        self.VarSignature = VarSignature(name,returnType)
        self.visibility = visibility
        self.params = params
        self.body = body #extra
        self.name = name

    def __repr__(self):
        return (
            f"METHOD({self.VarSignature} = > {','.join(map(str,self.params))})"
            + (" {\n" + textwrap.indent('\n'.join(map(str, self.body)),'\t') +"\n}")
             if self.body else '{}'  
            )


class ClassDecl(ASTNode):
    def __init__(self, name: Var, extends: Var|None=None, members:list[VarDecl|MethodDecl] = []):
        self.name = name
        self.extends = extends or None
        self.methods = list(filter(lambda x: isinstance(x, MethodDecl), members))
        self.attributes = list(filter(lambda x: isinstance(x, VarDecl), members))

    def __repr__(self):
        atributestr = "ATTRIBUTES:\n" + textwrap.indent('\n'.join(map(str, self.attributes)), '\t') 
        methodStr = "METHODS:\n" + textwrap.indent('\n'.join(map(str, self.methods)) if self.methods else '', '\t')
        extendsStr = f"extends {self.extends}" if self.extends else ''
        result = f"Class {self.name} {extendsStr}:\n"
        if atributestr:
            result += textwrap.indent(atributestr, '    ') + '\n'
        if methodStr:
            result += textwrap.indent(methodStr, '    ') + '\n'
        return result


class MainClass(ClassDecl):
    def __init__(self):
        self.body ='public static void main(String[] a) { System.out.println(); }'
        super().__init__(Var('main'), members=[])


class Program(ASTNode):
    def __init__(self, main_class:MainClass, classes: list[ClassDecl]=[]):
        self.main_class = main_class
        self.classes = classes
    
    def __str__(self):

        mcstr = textwrap.indent(str(self.main_class), '\t')
        classtr = ('\n'.join([textwrap.indent(str(c), '\t') for c in self.classes]))
        return (
            f"Program:\n{'-'*32}\n"
            f"Mainclass:\n{mcstr}\n"
            f"{'-'*16}\nClasses:\n"
            f"{classtr}"
        )


#extras
class Statement:
    def __init__(self, value):
        self.value: Expr | VarDecl | MethodDecl = value #type:ignore

    def __str__(self):
            value_type = type(self.value).__name__
            return f"Statement( {str(self.value)})"
    __repr__ = __str__


class FunctionCall(ASTNode):
    def __init__(self, var:Var, argument_names:list ):
        self.var = var
        self.arguments = argument_names
    def __repr__(self):
        return f"Function(run {self.var}({', '.join(map(str, self.arguments))}))"

class Expr(ASTNode): #type:ignore
    pass
#BasicExpr = Union[Var, FunctionCall, Expr]
# Define BasicExpr as a Union type



class DotAccess(ASTNode):
    def __init__(self, subexpr:Union[Var, FunctionCall, Expr], rightside=Var|FunctionCall):
        self.subexpr = subexpr
        self.rightside = rightside
    def __repr__(self):
        return f"Dot({self.subexpr}.{self.rightside})"


#I cant receive Expr as a subexpr 🐔🥚
class Expr(ASTNode):
    def __init__(self, subexpr:Expr|DotAccess|Var|FunctionCall, rightside:list[Var|FunctionCall] = []):
        if isinstance(subexpr, Expr):
            subexpr = subexpr.value

        self.value = self.__dotAccessRecurser(subexpr, rightside)

    def __dotAccessRecurser(self, tail:Var|FunctionCall, l:list[Var|FunctionCall]):
        if l:
            return DotAccess(l[0], self.__dotAccessRecurser(tail, l[1:]))
        else: return tail
    
    def __repr__(self):
        return f"Expr({self.value})"
        


#Type ::=
#Equivalent to the grammars 'Type'
