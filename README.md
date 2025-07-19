# sillYLang
Just so I dont lose this: a stupid and simple language, featuring no operands but some support to classes.
Lost? This makes an AST out of a program accepted by the grammar described in minijava.g4. 

Requires antlr python beforehand: ``antlr4 -Dlanguage=Python3 -visitor minijava.g4`

- can be run in a repl-like way: python parser.py
- or by passing a file: python parser.py file.sillylang

This should demonstrate most of what the grammar/ast builder is capable of:
```cpp
class eae { 
    int pato;
    int fib(int n) {
        return(x);
        int eae[][];
        eae.print(smth);
        ?(yes);
    }
}
``
