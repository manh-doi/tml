S-lang language
===============

We create a language named S-lang for demo. Please go to github page(https://github.com/manhdoi/tml) to clone source code that contains S-lang

Overview of the S-lang Language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

S-lang is a straightforward programming language designed to provide a solid foundation for understanding fundamental concepts in language design. Defined by an EBNF grammar, S-lang primarily focuses on representing basic arithmetic expressions.

With S-lang, users can perform addition, subtraction, multiplication, and division operations on both integer and floating-point numbers. The language supports the use of parentheses to control the order of operations. However, S-lang is limited in its scope, as it doesn't support variable declaration, control flow statements, or complex data structures.

Key features
~~~~~~~~~~~~

* Arithmetic expressions: Perform addition, subtraction, multiplication, and division.
* Integer and floating-point numbers: Support both integer and real numbers.
* Parentheses: Control the order of operations.


Demo
~~~~

Update the :code:`slang/slang_files/first.sl` as below:

.. code-block::

    1 + 2
    1 + 2 * 3

Then run commands as below:

.. code-block::

    cd slang
    python main.py

The result should be:

.. code-block::

    tokens: [[TOK INT:1], [PLUS], [TOK INT:2], [TOK INT:1], [PLUS], [TOK INT:2], [MUL], [TOK INT:3], [EOF]]
    nodes: [[[SUM: [INT: [TOK INT:1]] [PLUS] [INT: [TOK INT:2]]], [SUM: [INT: [TOK INT:1]] [PLUS] [TERM: [INT: [TOK INT:2]] [MUL] [INT: [TOK INT:3]]]]], [EOF]]

The lexer returns the :code:`tokens` and the parser returns the :code:`nodes`. This result will be used for further steps suck as compilation or interpretation.


Grammar
~~~~~~~

.. code-block::

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


Project structure
~~~~~~~~~~~~~~~~~

.. code-block::

    .
    ├── builders.py
    ├── grammar.md
    ├── main.py
    ├── nodes.py
    └── slang_files
        └── first.sl


* :code:`builders.py`: implement grammar
* :code:`grammar.md`: grammar of s-lang
* :code:`main.py`: entry point for demo
* :code:`nodes.py`: define nodes as :code:`IntNode`, :code:`FloatNode`, :code:`TermNode`, :code:`SumNode`
* :code:`slang_files`: contains :code:`.sl` file(s) for testing


Lexer
~~~~~

To create a lexer, we use the Lexer object and push pairs :code:`(condition, build_function)` as below:

.. code-block:: python

    from tml.lexical.lexer import Lexer, DIGITS, build_number, ASCII_LETTERS_UNDERSCORE, build_ident, build_string

    lexer = Lexer() \
        .m_plus(lambda x: x in DIGITS, build_number) \
        .m_plus(lambda x: x in ASCII_LETTERS_UNDERSCORE, build_ident) \
        .m_plus(lambda x: x == "\"", build_string)


In above code block, the :code:`lambda x: x in DIGITS` is condition of current character of lexer, :code:`x` is alias name of current char and :code:`build_number` is a build function that already implemented in :code:`TML`.
You can add your pairs :code:`(condition, build_function)` to lexer for specific purpose.

To use the lexer to tokenize a string:
.. code-block::

    tokens, error = lexer.tokenize(input_str, file_name)

If success, :code:`tokens` should be a list of tokens and :code:`error` should be :code:`None`.


Parser
~~~~~~

Parser parses tokens to nodes follow grammar. We need builders that implement the grammar and nodes to present the parsing result.

Nodes
-----

We need define a class that extends from :code:`Node` class and implement :code:`__init__`, :code:`__repr__` functions. Example:

.. code-block:: python

    class IntNode(Node):
        def __init__(self, token):
            self.token = token

        def __repr__(self):
            return f"[INT: {self.token}]"


    class TermNode(Node):
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

        def __repr__(self):
            return f"[TERM: {self.left} {self.operator} {self.right}]"


Builders
--------

Builders implement the grammar of language. Grammar includes rules under ebnf. We need to translate rules to builders.
Example, with rule: :code:`<term> ::= <factor>{(MUL|DIV)<factor>}` we create the :code:`Term` builder as below:

.. code-block:: python

    class Term(Builder):
        def init_builder(self):
            return seq(Factor, repeat(seq(select(terminate(MUL), terminate(DIV)), Factor)))

        def make_node(self, res):
            left, tails = res
            return reduce(lambda r, x: TermNode(r, *x), tails, left)


The builder should be extended from :code:`Builder` class and implement :code:`init_builder` and :code:`make_node` if necessary. The default of :code:`make_node` returns the :code:`res`.
In :code:`init_builder` function we use functions as :code:`seq`, :code:`repeat`, :code:`select`, they are combinator functions that support translate grammar rules to python code.

Another example:

.. code-block:: python

    class Factor(Builder):
        def init_builder(self):
            return Atom


    class Atom(Builder):
        def init_builder(self):
            return select(Int, Float)


    class Int(Builder):
        def init_builder(self):
            return terminate(INT)

        def make_node(self, res):
            return IntNode(res)

We use :code:`terminate` function for terminal symbols, as above example :code:`Int` builder is terminal symbol :code:`INT` token.


Parsing
-------

After implement grammar by builders, we can run parsing as below:

.. code-block:: python

    from tml.parsing.parser import parse

    res = parse(tokens, File)


The :code:`tokens` are the result of lexical analysis. The :code:`File` class is a builder that serves as the starting point for the grammar. The :code:`res` variable holds the parsing result, an instance of :code:`ParseResult`. The parsed nodes can be accessed through :code:`res.res` and utilized in subsequent stages such as compilation or interpretation.

.. code-block:: python

    if res.is_success():
        print(f"nodes: {res.res}")
    else:
        print(res.errors[0])


Done! We have just created the S-lang language with less 200 lines of code by using the **TML** library. Let's create your own language, good luck!