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


Contains the tokenizer.

Tokenizers convert programs into tokens.  Tokens are the smallest meaningful
units of programs.  Examples include if, for, while, {, ], ; and ;.
"""

import re

TOKEN_DEFS = {"ADD_EQ"   : r"\+=",
              "BIT_AND"  : r"&",
              "BIT_NOT"  : r"~",
              "BIT_OR"   : r"\|",
              "BIT_XOR"  : r"\^",
              "BREAK"    : r"break",
              "B_AND_EQ" : r"&=",
              "B_OR_EQ"  : r"\|=",
              "B_XOR_EQ" : r"\^=",
              "COLON"    : r":",
              "COMMA"    : r",",
              "CONTINUE" : r"continue",
              "DASH"     : r"-",
              "DEF"      : r"def",
              "DIV"      : r"/",
              "DIV_EQ"   : r"/=",
              "ELIF"     : r"elif",
              "ELSE"     : r"else",
              "EQEQ"     : r"==",
              "EQUALS"   : r"=",
              "EXP_EQ"   : r"\*\*=",
              "FALSE"    : r"False",
              "FOR"      : r"for",
              "GR_THAN"  : r">",
              "GR_TH_EQ" : r">=",
              "IF"       : r"if",
              "IN"       : r"in",
              "IS"       : r"is",
              "LOG_AND"  : r"and",
              "LOG_NOT"  : r"not",
              "LOG_OR"   : r"or",
              "LS_THAN"  : r"<",
              "LS_TH_EQ" : r"<=",
              "L_BRACE"  : r"\{",
              "L_BRACK"  : r"\[",
              "L_PAREN"  : r"\(",
              "L_SHIFT"  : r"<<",
              "L_SH_EQ"  : r"<<=",
              "MOD"      : r"%",
              "MOD_EQ"   : r"%=",
              "MULT_EQ"  : r"\*=",
              "NATURAL"  : r"\d+",
              "NONE"     : r"None",
              "NOT_EQ"   : r"!=",
              "PLUS"     : r"\+",
              "RETURN"   : r"return",
              "R_BRACE"  : r"\}",
              "R_BRACK"  : r"\]",
              "R_PAREN"  : r"\)",
              "R_SHIFT"  : r">>",
              "R_SH_EQ"  : r">>=",
              "SEMICOL"  : r";",
              "STAR"     : r"\*",
              "STARSTAR" : r"\*\*",
              "STRING"   : r'"[^"]*"',
              "SUB_EQ"   : r"-=",
              "TRUE"     : r"True",
              "VARIABLE" : r"[a-zA-Z_]\w*",
              "WHILE"    : r"while"}
TOKEN_DEFS = dict(sorted(TOKEN_DEFS.items(),
                         key = lambda e : -len(e[1]) * (e[0] != "VARIABLE")))
NEWLINE    = ("NEWLINE",   "\n")
BLOCK_BEG  = ("BLOCK_BEG", "")
BLOCK_END  = ("BLOCK_END", "")
WS_RE      = r"\s*"

def tokenizer_(line):
        """
        tokenizer helper function

        Converts program lines into tokens.  Token definitions are checked in
        descending order based on size except for the VARIABLE token definition
        which is always checked last.
        """

        def token(text):
                for e in TOKEN_DEFS:
                        match = re.match(TOKEN_DEFS[e], text)
                        if match:
                                token = (e, match.group(0))
                                break

                return token

        tokens = []
        index  = 0
        while index < len(line):
                index += len(re.match(WS_RE, line[index:]).group(0))
                tokens.append(token(line[index:]))
                index += len(tokens[-1][1])
        tokens.append(NEWLINE)

        return tokens

def tokenizer(program):
        """
        Converts programs into tokens.

        Changes in indentation are replaced with BLOCK_BEG and BLOCK_END
        tokens.  Spaces are added before colons unless they are in strings.
        """

        tokens   = []
        indents  = [0]
        program_ = re.sub(f'{TOKEN_DEFS["STRING"]}|:',
                          lambda e: e.group(0) if e.group(0) != ":" else " :",
                          program)
        for e in program_.split("\n"):
                if e:
                        indent  = len(re.match(WS_RE, e).group(0))
                        if indent > indents[-1]:
                                indents.append(indent)
                                tokens.append(BLOCK_BEG)
                        else:
                                while indent < indents[-1]:
                                        indents.pop()
                                        tokens.append(BLOCK_END)
                        tokens += tokenizer_(e)
        while indents != [0]:
                indents.pop()
                tokens.append(BLOCK_END)

        return tokens
