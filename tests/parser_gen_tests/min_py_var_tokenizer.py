# Copyright 2020 Christian Seberino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

WS = r"\s+"

regexes = {"ADD_EQ"    : r"\+=",
           "B_AND_EQ"  : r"&=",
           "B_OR_EQ"   : r"\|=",
           "B_XOR_EQ"  : r"\^=",
           "BIT_AND"   : r"&",
           "BIT_NOT"   : r"~",
           "BIT_OR"    : r"\|",
           "BIT_XOR"   : r"\^",
           "BREAK"     : r"break",
           "COLON"     : r":",
           "COMMA"     : r",",
           "CONTINUE"  : r"continue",
           "DASH"      : r"-",
           "DEF"       : r"def",
           "DIV"       : r"/",
           "DIV_EQ"    : r"/=",
           "ELIF"      : r"elif",
           "ELSE"      : r"else",
           "EQEQ"      : r"==",
           "EQUALS"    : r"=",
           "EXP_EQ"    : r"\*\*=",
           "FALSE"     : r"False",
           "FOR"       : r"for",
           "GR_TH_EQ"  : r">=",
           "GR_THAN"   : r">",
           "IF"        : r"if",
           "IN"        : r"in",
           "IS"        : r"is",
           "L_BRACE"   : r"\{",
           "L_BRACK"   : r"\[",
           "LOG_AND"   : r"and",
           "LOG_NOT"   : r"not",
           "LOG_OR"    : r"or",
           "L_PAREN"   : r"\(",
           "L_SH_EQ"   : r"<<=",
           "L_SHIFT"   : r"<<",
           "LS_TH_EQ"  : r"<=",
           "LS_THAN"   : r"<",
           "MOD"       : r"%",
           "MOD_EQ"    : r"%=",
           "MULT_EQ"   : r"\*=",
           "NATURAL"   : r"\d+",
           "NEWLINE"   : r"\n",
           "NONE"      : r"None",
           "NOT_EQ"    : r"!=",
           "PLUS"      : r"\+",
           "R_BRACE"   : r"\}",
           "R_BRACK"   : r"\]",
           "R_PAREN"   : r"\)",
           "R_SH_EQ"   : r">>=",
           "R_SHIFT"   : r">>",
           "RETURN"    : r"return",
           "SEMICOL"   : r";",
           "STAR"      : r"\*",
           "STARSTAR"  : r"\*\*",
           "STRING"    : r'"(\\"|[^"])*(?<=[^\\])"',
           "SUB_EQ"    : r"-=",
           "TRUE"      : r"True",
           "VARIABLE"  : r"[a-zA-Z_]\w*",
           "WHILE"     : r"while"}
key     = lambda e : -len(e[1]) * (e[0] != "VARIABLE")
regexes = sorted(regexes.items(), key = key)

def tokenizer_(text):
        tokens = []
        index  = 0
        while index < len(text):
                match = re.match(WS, text[index:])
                if match:
                        index += len(match.group(0))
                        continue
                for e in regexes:
                        match = re.match(e[1], text[index:])
                        if match:
                                tokens.append((e[0], match.group(0)))
                                index += len(match.group(0))
                                break
        tokens.append(("NEWLINE", "\n"))

        return tokens

def tokenizer(text):
        tokens = []
        levels = [0]
        for e in text.split("\n"):
                if e:
                        level = re.search(r"\S", e).start()
                        if level > levels[-1]:
                                levels.append(level)
                                tokens.append(("BLOCK_BEG", ""))
                        else:
                                while level < levels[-1]:
                                        levels.pop()
                                        tokens.append(("BLOCK_END", ""))
                        tokens += tokenizer_(e)
        while levels != [0]:
                levels.pop()
                tokens.append(("BLOCK_END", ""))

        return tokens
