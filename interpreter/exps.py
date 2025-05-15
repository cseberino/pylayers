"""
Copyright 2025 Christian Seberino

This file is part of Pylayers.

Pylayers is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Pylayers is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
Pylayers. If not, see <https://www.gnu.org/licenses/>.

________________________________________________________________________________


Contains the exps function which converts programs to expressions.

Unevaluated programs do not include evaluated functions and macros.
"""

import re

IGNORE_RE = r"(\s|#[^\n]*\n)*"
TOKEN_RE  = r'\(|\)|"[^"]*"|[^"\(\)\s]+'
BOOL_RE   = r"True|False"
INT_RE    = r"\-?\d+"

def tokenizer(program):
        """
        Converts programs to tokens.

        Tokens are expressions or parts of expressions.
        """

        tokens = []
        index  = 0
        while index < len(program):
                index += len(re.match(IGNORE_RE, program[index:]).group(0))
                token  = re.match(TOKEN_RE, program[index:])
                if token:
                        tokens.append(token.group(0))
                        index += len(token.group(0))

        return tokens

def parser(tokens):
        """
        Converts tokens to abstract syntax trees.

        Abtract syntax trees are lists of expression representations.  Variable
        representations use tuples.
        """

        def exp(tokens):
                token = tokens.pop(0)
                if token == "(":
                        exp_ = []
                        while tokens and (tokens[0] != ")"):
                                exp_.append(exp(tokens))
                        tokens.pop(0)
                else:
                        if   re.fullmatch(BOOL_RE, token):
                                exp_ = True if token == "True" else False
                        elif re.fullmatch(INT_RE,  token):
                                exp_ = int(token)
                        elif token[0] == token[-1] == '"':
                                exp_ = token[1:-1]
                        else:
                                exp_ = (token,)

                return exp_

        ast = []
        while tokens:
                ast.append(exp(tokens))

        return ast

def exps(program):
        """
        Converts programs into expressions.

        Uses a tokenizer and a parser.
        """

        return parser(tokenizer(program))
