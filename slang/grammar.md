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



# xxx

<list> ::= LSQBRACE <list_elements> RSQBRACE

<list_elements> ::= [<list_element>]{COMMA <list_element>}[COMMA]

<list_element> ::= <expression>

```