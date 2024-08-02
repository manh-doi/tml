# Grammar

```ebnf

<file> ::= <statements> EOF

<statements> ::= {<statement>}

<statement> ::= <expression>

<expression> ::= <sum>

<sum> ::= <term>{(PLUS|MINUS)<term>}

<term> ::= <factor>{(MUL|DIV)<factor>}

<factor> ::= <atom>

<atom> ::= (<int>|<float>|<int>)

<int> ::= INT

<float> ::= FLOAT

```