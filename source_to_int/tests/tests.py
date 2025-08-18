#!/usr/bin/env python3

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


Contains the unit tests.

Tests the tokenizer, parser generator, parser and intermediate code generator.
"""

import sys
sys.path.append("..")
import tokenizer
import parser_gen
import parser
import int_code_gen

import triv_tokenizer
import arith_tokenizer
import min_c_tokenizer
import triv_grammar
import arith_grammar
import min_c_grammar
import unittest
import importlib
import subprocess
import os

class Tester(unittest.TestCase):
        def setUp(self):
                importlib.reload(parser_gen)
                importlib.reload(parser)

        def test_basic_1(self):
                text   = \
"""
1 + 2
"""
                output = tokenizer.tokenizer(text)
                answer = [("NATURAL", "1"),
                          ("PLUS",    "+"),
                          ("NATURAL", "2"),
                          ("NEWLINE", "\n")]
                self.assertEqual(output, answer)

        def test_basic_2(self):
                text   = \
"""
"asdf"
"""
                output = tokenizer.tokenizer(text)
                answer = [("STRING",  '"asdf"'),
                          ("NEWLINE", "\n")]
                self.assertEqual(output, answer)

        def test_basic_3(self):
                text   = \
"""
"as:df"
"""
                output = tokenizer.tokenizer(text)
                answer = [("STRING",  '"as:df"'),
                          ("NEWLINE", "\n")]
                self.assertEqual(output, answer)

        def test_all_singles(self):
                token_defs = sorted(tokenizer.TOKEN_DEFS.items(),
                                    key = lambda e : e[0])
                texts      = ["+=", "&", "~", "|", "^", "break", "&=", "|=",
                               "^=", ":", ",", "continue", "-", "def", "/",
                               "/=", "elif", "else", "==", "=", "**=", "False",
                               "for", ">", ">=", "if", "in", "is", "and", "not",
                               "or", "<", "<=", "{", "[", "(", "<<", "<<=", "%",
                               "%=", "*=", "2425", "None", "!=", "+", "return",
                               "}", "]", ")", ">>", ">>=", ";", "*", "**",
                               '"some string"', "-=", "True", "my_var", "while"]
                for i, e in enumerate(texts):
                        output = tokenizer.tokenizer_(e)
                        answer = [(token_defs[i][0], e), tokenizer.NEWLINE]
                        self.assertEqual(output, answer)

        def test_multiple_lines(self):
                text   = \
"""
1 + 2
"asdf"
"""
                output = tokenizer.tokenizer(text)
                answer = [("NATURAL", "1"),
                          ("PLUS",    "+"),
                          ("NATURAL", "2"),
                          ("NEWLINE", "\n"),
                          ("STRING",  '"asdf"'),
                          ("NEWLINE", "\n")]
                self.assertEqual(output, answer)

        def test_blocks(self):
                text   = \
"""
if True:
   1 + 2
   "asdf"
"""
                output = tokenizer.tokenizer(text)
                answer = [("IF",        "if"),
                          ("TRUE",      "True"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("NATURAL",   "1"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "2"),
                          ("NEWLINE",   "\n"),
                          ("STRING",    '"asdf"'),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

                text   = \
"""
if 1 + 2:
   True
   "asdf"
"""
                output = tokenizer.tokenizer(text)
                answer = [("IF",        "if"),
                          ("NATURAL",   "1"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "2"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("TRUE",      "True"),
                          ("NEWLINE",   "\n"),
                          ("STRING",    '"asdf"'),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

        def test_min_c_tokenizer(self):
                for e in [("+=",       "ADD_EQ"),
                          ("&",        "AMPER"),
                          ("~",        "BIT_COMP"),
                          ("|",        "BIT_OR"),
                          ("^",        "BIT_XOR"),
                          ("break",    "BREAK"),
                          ("&=",       "B_AND_EQ"),
                          ("|=",       "B_OR_EQ"),
                          ("^=",       "B_XOR_EQ"),
                          ("char",     "CHAR"),
                          (",",        "COMMA"),
                          ("continue", "CONTINUE"),
                          ("-",        "DASH"),
                          ("/",        "DIV"),
                          ("/=",       "DIV_EQ"),
                          ("else",     "ELSE"),
                          ("=",        "EQUALS"),
                          ("==",       "EQEQ"),
                          ("for",      "FOR"),
                          (">",        "GR_THAN"),
                          (">=",       "GR_TH_EQ"),
                          ("if",       "IF"),
                          ("int",      "INT"),
                          ("&&",       "LOG_AND"),
                          ("||",       "LOG_OR"),
                          ("<",        "LS_THAN"),
                          ("<=",       "LS_TH_EQ"),
                          ("{",        "L_BRACE"),
                          ("[",        "L_BRACK"),
                          ("(",        "L_PAREN"),
                          ("<<",       "L_SHIFT"),
                          ("<<=",      "L_SH_EQ"),
                          ("%",        "MOD"),
                          ("%=",       "MOD_EQ"),
                          ("*=",       "MULT_EQ"),
                          ("!",        "LOG_NOT"),
                          ("!=",       "NOT_EQ"),
                          ("23434",    "NATURAL"),
                          ("+",        "PLUS"),
                          ("return",   "RETURN"),
                          ("}",        "R_BRACE"),
                          ("]",        "R_BRACK"),
                          (")",        "R_PAREN"),
                          (">>",       "R_SHIFT"),
                          (">>=",      "R_SH_EQ"),
                          (";",        "SEMICOL"),
                          ("sizeof",   "SIZEOF"),
                          ("*",        "STAR"),
                          ('"adf23"',  "STRING"),
                          ("-=",       "SUB_EQ"),
                          ("asdf3",    "VARIABLE"),
                          ("void",     "VOID"),
                          ("while",    "WHILE")]:
                          answer = [(e[1], e[0])]
                          output = min_c_tokenizer.tokenizer(e[0])
                          self.assertEqual(output, answer)

        def test_triv_grammar(self):
                parser = parser_gen.parser_gen(triv_grammar.GRAMMAR)

                def p_and_tok(text):
                        return parser(triv_tokenizer.tokenizer(text))

                for let in "abcdefghijklmnopqrstuvwxyz":
                        setattr(sys.modules[__name__], let, (let.upper(), let))

                answer = ("program", ("one_or_more", b))
                output = p_and_tok("b")
                self.assertEqual(output, answer)

                answer = ("program", ("one_or_more", b, b, b, b, b))
                output = p_and_tok("bbbbb")
                self.assertEqual(output, answer)

                answer = ("program", ("zero_or_more", d))
                output = p_and_tok("d")
                self.assertEqual(output, answer)

                answer = ("program", ("zero_or_more", d, a))
                output = p_and_tok("da")
                self.assertEqual(output, answer)

                answer = ("program", ("zero_or_more", d, a, a, a, a, a))
                output = p_and_tok("daaaaa")
                self.assertEqual(output, answer)

                answer = ("program", ("optional", c, e))
                output = p_and_tok("ce")
                self.assertEqual(output, answer)

                answer = ("program", ("optional", e))
                output = p_and_tok("e")
                self.assertEqual(output, answer)

                answer = ("program", ("group", f, g))
                output = p_and_tok("fg")
                self.assertEqual(output, answer)

                answer = ("program", ("group", f, h))
                output = p_and_tok("fh")
                self.assertEqual(output, answer)

                answer = ("program", ("set", i, j, k))
                output = p_and_tok("ijk")
                self.assertEqual(output, answer)

        def test_arith_grammar(self):
                parser = parser_gen.parser_gen(arith_grammar.GRAMMAR)

                def p_and_tok(text):
                        return parser(arith_tokenizer.tokenizer(text))

                plus   = ("PLUS", "+")
                minus  = ("MINUS", "-")
                mult   = ("MULT", "*")
                div    = ("DIV", "/")
                lprns  = ("LPARENS", "(")
                rprns  = ("RPARENS", ")")

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, plus, prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("1+1")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("1234+328")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, minus, prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("1-1")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("1234-328")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "823")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("823")
                self.assertEqual(output, answer)

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(342)")
                self.assertEqual(output, answer)

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(342)*(87924)")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("program", sum_x)
                output = p_and_tok("1234*328")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("program", sum_x)
                output = p_and_tok("1234/328")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, mult, val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("11*22+3*5")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("11/22+3*5")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("11/22-3*5")
                self.assertEqual(output, answer)

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(342)/(87924)")
                self.assertEqual(output, answer)

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(23+25)/(8*723)")
                self.assertEqual(output, answer)

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("(23+25)+(8*723)")
                self.assertEqual(output, answer)

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(23+25)*(8*723)")
                self.assertEqual(output, answer)

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("program", sum_x)
                output = p_and_tok("(23+25)-(8*723)")
                self.assertEqual(output, answer)

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, minus, prodx2)
                exp_x  = ("program", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, div, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("program", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("program", sum_x)
                output = p_and_tok("(23-25)/(8/723)")
                self.assertEqual(output, answer)

                nat_11 = ("NATURAL", "11")
                val_11 = ("value", nat_11)
                nat_22 = ("NATURAL", "22")
                val_22 = ("value", nat_22)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_8  = ("NATURAL", "8")
                val_8  = ("value", nat_8)
                nat_17 = ("NATURAL", "17")
                val_17 = ("value", nat_17)
                nat_4  = ("NATURAL", "4")
                val_4  = ("value", nat_4)

                p11d22 = ("product", val_11, div, val_22)
                p8d17  = ("product", val_8, div, val_17)
                p3     = ("product", val_3)
                p4     = ("product", val_4)

                sumone = ("sum", p11d22, plus, p3)
                sumtwo = ("sum", p8d17, minus, p4)

                expone = ("program", sumone)
                exptwo = ("program", sumtwo)

                valone = ("value", lprns, expone, rprns)
                valtwo = ("value", lprns, exptwo, rprns)

                pone   = ("product", valone, div, valtwo)
                sone   = ("sum", pone)
                answer = ("program", sone)
                output = p_and_tok("(11/22+3)/(8/17-4)")
                self.assertEqual(output, answer)

                nat_1  = ("NATURAL", "11")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "22")
                val_2  = ("value", nat_2)
                nat_3  = ("NATURAL", "3")
                val_3  = ("value", nat_3)
                nat_4  = ("NATURAL", "5")
                val_4  = ("value", nat_4)
                prod_1 = ("product", val_1, div,  val_2)
                prod_2 = ("product", val_3, mult, val_4)
                sum_x  = ("sum", prod_1, plus, prod_2)
                exp_x  = ("program", sum_x)
                val_a  = ("value", lprns, exp_x, rprns)

                nat_5  = ("NATURAL", "8")
                val_5  = ("value", nat_5)
                nat_6  = ("NATURAL", "17")
                val_6  = ("value", nat_6)
                nat_7  = ("NATURAL", "4")
                val_7  = ("value", nat_7)
                nat_8  = ("NATURAL", "6")
                val_8  = ("value", nat_8)
                prod_3 = ("product", val_5, div,  val_6)
                prod_4 = ("product", val_7, mult, val_8)
                sum_y  = ("sum", prod_3, minus, prod_4)
                exp_y  = ("program", sum_y)
                val_b  = ("value", lprns, exp_y, rprns)

                prod_z = ("product", val_a, div, val_b)
                sum_z  = ("sum", prod_z)
                answer = ("program", sum_z)
                output = p_and_tok("(11/22+3*5)/(8/17-4*6)")
                self.assertEqual(output, answer)

                n      = 10 * [[]]
                v      = 10 * [[]]
                p      = 10 * [[]]
                for i in range(1, 10):
                        n[i] = ("NATURAL", str(i))
                        v[i] = ("value",   n[i])
                        p[i] = ("product", v[i])

                s      = ("sum", p[1], plus, p[2], plus, p[3])
                answer = ("program", s)
                output = p_and_tok("1+2+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], plus, p[9], plus, p[3])
                answer = ("program", s)
                output = p_and_tok("7+8+9+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], minus, p[9], plus, p[3])
                answer = ("program", s)
                output = p_and_tok("7+8-9+3")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], mult, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("program", s)
                output = p_and_tok("5*4*2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("program", s)
                output = p_and_tok("5*4/2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("program", s)
                output = p_and_tok("5*4/2*7")
                self.assertEqual(output, answer)

                p5t4   = ("product", v[5], mult, v[4])
                s5t4   = ("sum", p5t4)
                e5t4   = ("program", s5t4)
                v5t4   = ("value", lprns, e5t4, rprns)
                pxd2t7 = ("product", v5t4, div, v[2], mult, v[7])
                p9t1d3 = ("product", v[9], mult, v[1], div, v[3])
                p8t3d5 = ("product", v[8], mult, v[3], div, v[5])
                p6     = ("product", v[6])
                p3     = ("product", v[3])
                sxm6   = ("sum", p8t3d5, minus, p6)
                exm6   = ("program", sxm6)
                vxm6   = ("value", lprns, exm6, rprns)
                pxm6   = ("product", vxm6)
                s      = ("sum", pxd2t7, plus, p3, minus, p9t1d3, plus, pxm6)
                answer = ("program", s)
                output = p_and_tok("(5*4)/2*7+3-9*1/3+(8*3/5-6)")
                self.assertEqual(output, answer)

        def test_min_c_grammar(self):
                parser = parser_gen.parser_gen(min_c_grammar.GRAMMAR)

                def p_and_tok(text):
                        return parser(min_c_tokenizer.tokenizer(text))

                SEMICOL    = ("SEMICOL",     ";")
                COMMA      = ("COMMA",       ",")
                STAR       = ("STAR",        "*")
                EQUALS     = ("EQUALS",      "=")
                TYPE_INT   = ("type",        ("INT",  "int"))
                TYPE_CHAR  = ("type",        ("CHAR", "char"))
                TYPE_VOID  = ("type",        ("VOID", "void"))
                L_PAREN    = ("L_PAREN",     "(")
                R_PAREN    = ("R_PAREN",     ")")
                L_BRACE    = ("L_BRACE",     "{")
                R_BRACE    = ("R_BRACE",     "}")
                VAR_I      = ("VARIABLE",    "i")
                VAR_X      = ("VARIABLE",    "x")
                VAR_Y      = ("VARIABLE",    "y")
                VAR_Z      = ("VARIABLE",    "z")
                VAR_F      = ("VARIABLE",    "f")
                VAR_G      = ("VARIABLE",    "g")
                DEC_INT_X  = ("declaration", TYPE_INT,   ("dec_base", VAR_X))
                DEC_INT_Y  = ("declaration", TYPE_INT,   ("dec_base", VAR_Y))
                DEC_CHAR_Z = ("declaration", TYPE_CHAR,  ("dec_base", VAR_Z))
                ST_INT_X   = ("statement",   ("stat_dec", DEC_INT_X,  SEMICOL))
                ST_INT_Y   = ("statement",   ("stat_dec", DEC_INT_Y,  SEMICOL))
                ST_CHAR_Z  = ("statement",   ("stat_dec", DEC_CHAR_Z, SEMICOL))
                EXP_0      = ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ("exp_bit_or",
                                  ("exp_bit_xor",
                                   ("exp_bit_and",
                                    ("exp_shift",
                                     ("exp_sum",
                                      ("exp_prod",
                                       ("exp_prefix",
                                        ("exp_inv_ind",
                                         ("exp_base",
                                          ("NATURAL", "0"))))))))))))))

                EXP_4      = ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ("exp_bit_or",
                                  ("exp_bit_xor",
                                   ("exp_bit_and",
                                    ("exp_shift",
                                     ("exp_sum",
                                      ("exp_prod",
                                       ("exp_prefix",
                                        ("exp_inv_ind",
                                         ("exp_base",
                                          ("NATURAL", "4"))))))))))))))

                output    = p_and_tok("""
int f() {
        int  x;
        char z;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_INT_X, ST_CHAR_Z, R_BRACE))))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
char z;
int  y;

int f() {
        int  x;
        char z;
}

void g() {
        char z;
        int  x;
        int  ***y = 4;
}
""")
                s         = ("statement",
                             ("stat_dec",
                              ("declaration",
                               TYPE_INT, STAR, STAR, STAR, ("dec_base", VAR_Y),
                                                                 EQUALS, EXP_4),
                              SEMICOL))
                answer    = ("program",
                             ST_CHAR_Z,
                             ST_INT_Y,
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_INT_X, ST_CHAR_Z, R_BRACE))),
                             ("statement",
                              ("stat_func",
                               ("declaration",
                                TYPE_VOID,
                                ("dec_base", VAR_G, L_PAREN, R_PAREN)),
                               ("stat_block",
                                L_BRACE, ST_CHAR_Z, ST_INT_X, s, R_BRACE))))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
int x[4];
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_X, ("L_BRACK", "["), EXP_4,
                                                             ("R_BRACK", "]"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
int x[4][4];
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_X, ("L_BRACK", "["), EXP_4,
                                      ("R_BRACK", "]"), ("L_BRACK", "["), EXP_4,
                                                             ("R_BRACK", "]"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
int f(int x, char z);
""")
                answer    = ("program",
                             ("statement",
                              ("stat_dec",
                               ("declaration",
                                TYPE_INT,
                                ("dec_base", VAR_F, ("L_PAREN", "("), DEC_INT_X,
                                          COMMA, DEC_CHAR_Z, ("R_PAREN", ")"))),
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
break;
continue;
return;
return 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_jump", ("BREAK",    "break"),    SEMICOL)),
                             ("statement",
                              ("stat_jump", ("CONTINUE", "continue"), SEMICOL)),
                             ("statement",
                              ("stat_jump", ("RETURN",   "return"),   SEMICOL)),
                             ("statement",
                              ("stat_jump",
                               ("RETURN", "return"), EXP_4, SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_exp", EXP_4, SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
if (4) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
if (4) {
        break;
} else {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")),
                               ("ELSE", "else"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
while (4) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               ("L_PAREN", "("),
                               EXP_4,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
&x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("prefix_op", ("AMPER", "&")),
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                output    = p_and_tok("""
&-~x = 4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("prefix_op", ("AMPER",    "&")),
                                ("prefix_op", ("DASH",     "-")),
                                ("prefix_op", ("BIT_COMP", "~")),
                                ("exp_inv_ind", ("exp_base", VAR_X))),
                               ("assign_op", EQUALS),
                               EXP_4,
                               SEMICOL)))
                self.assertEqual(output, answer)

                sa        = ("stat_assign",
                             ("exp_prefix",
                              ("exp_inv_ind", ("exp_base", VAR_I))),
                             ("assign_op", EQUALS),
                             EXP_0,
                             SEMICOL)
                ebo_i     = ("exp_bit_or",
                             ("exp_bit_xor",
                              ("exp_bit_and",
                               ("exp_shift",
                                ("exp_sum",
                                 ("exp_prod",
                                  ("exp_prefix",
                                   ("exp_inv_ind",
                                    ("exp_base",
                                     VAR_I)))))))))
                ebo_4     = ("exp_bit_or",
                             ("exp_bit_xor",
                              ("exp_bit_and",
                               ("exp_shift",
                                ("exp_sum",
                                 ("exp_prod",
                                  ("exp_prefix",
                                   ("exp_inv_ind",
                                    ("exp_base",
                                     ("NATURAL", "4"))))))))))
                se        = ("stat_exp",
                             ("expression",
                              ("exp_log_and",
                               ("exp_log_not",
                                ("exp_comp",
                                 ebo_i,
                                 ("comp_op", ("LS_THAN", "<")),
                                 ebo_4)))),
                             SEMICOL)
                eip1      = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_I)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base",
                                         ("NATURAL", "1"))))))))))))))
                output    = p_and_tok("""
for (i = 0; i < 4; i = i + 1) {
        break;
}
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("FOR", "for"),
                               ("L_PAREN", "("),
                               sa,
                               se,
                               ("exp_prefix",
                                ("exp_inv_ind", ("exp_base", VAR_I))),
                               ("assign_op", EQUALS),
                               eip1,
                               ("R_PAREN", ")"),
                               ("stat_block",
                                ("L_BRACE", "{"),
                                ("statement", ("stat_jump", ("BREAK", "break"),
                                                                      SEMICOL)),
                                ("R_BRACE", "}")))))
                self.assertEqual(output, answer)

                e1        = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_I)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base", VAR_X)))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_prefix",
                                       ("exp_inv_ind",
                                        ("exp_base",
                                         ("NATURAL", "1"))))))))))))))
                answer    = ("program",
                             ("statement",
                              ("stat_assign",
                               ("exp_prefix",
                                ("exp_inv_ind",
                                 ("exp_base", VAR_I))),
                               ("assign_op", EQUALS),
                               e1,
                               SEMICOL)))
                output    = p_and_tok("""
i = i + x + 1;
""")
                self.assertEqual(output, answer)

        def test_parser(self):
                COLON     = ("COLON",   ":")
                COMMA     = ("COMMA",   ",")
                SEMICOL   = ("SEMICOL", ";")
                EQUALS    = ("EQUALS",  "=")
                L_PAREN   = ("L_PAREN", "(")
                R_PAREN   = ("R_PAREN", ")")
                L_BRACE   = ("L_BRACE", "{")
                R_BRACE   = ("R_BRACE", "}")
                VAR_I     = ("VARIABLE", "i")
                VAR_X     = ("VARIABLE", "x")
                VAR_Y     = ("VARIABLE", "y")
                VAR_Z     = ("VARIABLE", "z")
                VAR_F     = ("VARIABLE", "f")
                VAR_G     = ("VARIABLE", "g")
                B_BEG     = ("BLOCK_BEG", "")
                B_END     = ("BLOCK_END", "")
                EXP_7     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("NATURAL", "7")))))))))))))))
                EXP_X     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("VARIABLE", "x")))))))))))))))
                EXP_Y     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("VARIABLE", "y")))))))))))))))
                EXP_Z     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("VARIABLE", "z")))))))))))))))
                EXP_G     = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("VARIABLE", "g")))))))))))))))
                EXP_NONE  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("NONE", "None")))))))))))))))
                EXP_TRUE  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("TRUE", "True")))))))))))))))
                EXP_FALSE = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("FALSE", "False")))))))))))))))
                EXP_HELLO = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("STRING", '"hello"')))))))))))))))
                EXP_R7    = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", ("VARIABLE", "range")),
                                         ("L_PAREN", "("),
                                         EXP_7,
                                         ("R_PAREN", ")"))))))))))))))
                EXP_T7    = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("L_PAREN", "("),
                                          EXP_7,
                                          ("R_PAREN", ")")))))))))))))))
                EXP_L7    = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("L_BRACK", "["),
                                          EXP_7,
                                          ("R_BRACK", "]")))))))))))))))
                EXP_L7XY  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_",
                                          ("L_BRACK", "["),
                                          EXP_7,
                                          COMMA,
                                          EXP_X,
                                          COMMA,
                                          EXP_Y,
                                          ("R_BRACK", "]")))))))))))))))
                EXP_FINV  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_F),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"))))))))))))))
                EXP_ZIND  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_Z),
                                         ("L_BRACK", "["),
                                         EXP_7,
                                         ("R_BRACK", "]"))))))))))))))
                EXP_ZIND4 = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_Z),
                                         ("L_BRACK", "["),
                                         EXP_7,
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         EXP_X,
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         EXP_Y,
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         EXP_Z,
                                         ("R_BRACK", "]"))))))))))))))
                EXP_ZSLS  = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_Z),
                                         ("L_BRACK", "["),
                                         EXP_7, COLON, EXP_Y,
                                         ("R_BRACK", "]"))))))))))))))
                EXP_1P2   = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", ("NATURAL", "1")))))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", ("NATURAL", "2")))))))))))))))
                EXP_7PX   = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", ("NATURAL", "7")))))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_X))))))))))))))
                EXP_7PXMY = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", ("NATURAL", "7")))))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_X))))),
                                     ("DASH", "-"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_Y))))))))))))))
                EXP_F2INV = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_F),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"))))))))))))))
                EXP_FLOTS = ("expression",
                             ("exp_log_and",
                              ("exp_log_not",
                               ("exp_comp",
                                ("exp_bit_or",
                                 ("exp_bit_xor",
                                  ("exp_bit_and",
                                   ("exp_shift",
                                    ("exp_sum",
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_iis",
                                         ("exp_", VAR_F),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"),
                                         ("L_BRACK", "["),
                                         EXP_7,
                                         ("R_BRACK", "]"),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"),
                                         ("L_BRACK", "["),
                                         EXP_7,
                                         ("R_BRACK", "]"))))))))))))))
                ST_7      = ("statement",
                             ("stat_semicol",
                              ("stat_semicol_", EXP_7),
                              ("NEWLINE", "\n")))
                ST_BREAK  = ("statement",
                             ("stat_semicol",
                              ("stat_semicol_", ("BREAK", "break")),
                              ("NEWLINE", "\n")))

                text      = \
"""
continue
break
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", ("CONTINUE", "continue")),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", ("BREAK", "break")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
break ; continue
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", ("BREAK",    "break")),
                               SEMICOL,
                               ("stat_semicol_", ("CONTINUE", "continue")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
7
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
while x:
        7
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
if x:
        7
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
if x:
        7
else:
        break
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END),
                               ("ELSE", "else"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
if   x:
        7
elif y:
        7
elif z:
        break
else:
        break
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END),
                               ("ELIF", "elif"),
                               EXP_Y,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END),
                               ("ELIF", "elif"),
                               EXP_Z,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END),
                               ("ELSE", "else"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
range(7)
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_R7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
def f():
        7
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_func_def",
                               ("DEF", "def"),
                               VAR_F,
                               ("L_PAREN", "("),
                               ("R_PAREN", ")"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
def f(x, y, z):
        7
        break
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_func_def",
                               ("DEF", "def"),
                               VAR_F,
                               ("L_PAREN", "("),
                               VAR_X,
                               COMMA,
                               VAR_Y,
                               COMMA,
                               VAR_Z,
                               ("R_PAREN", ")"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
for x in range(7):
        7
        break
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("FOR", "for"),
                                VAR_X,
                                ("IN", "in"),
                                EXP_R7,
                                COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, ST_BREAK, B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
None
True
False
"hello"
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_NONE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_TRUE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_FALSE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_HELLO),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
(7)
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_T7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
[7]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_L7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
[7, x, y]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_L7XY),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
x = 7
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_",
                                EXP_X, ("assign", EQUALS), EXP_7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
return x
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_",
                                ("RETURN", "return"), EXP_X),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
f(x, y, z)
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_FINV),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
z[7]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_ZIND),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
z[7][x][y][z]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_ZIND4),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
z[7:y]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_ZSLS),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
1 + 2
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_1P2),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
7 + x
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_7PX),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
7 + x - y
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_7PXMY),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
for i in range(7):
        g += x
        y /= f(x, y, z)
        while z:
                if z[7]:
                        g = 7 + x - y
                        y = 7 + x - y
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("FOR", "for"), VAR_I, ("IN", "in"), EXP_R7,
                                                       COLON, ("NEWLINE", "\n"),
                               ("block",
                                B_BEG,
                                ("statement",
                                 ("stat_semicol",
                                  ("stat_semicol_",
                                   EXP_G,
                                   ("assign", ("ADD_EQ", "+=")),
                                   EXP_X),
                                  ("NEWLINE", "\n"))),
                                ("statement",
                                 ("stat_semicol",
                                  ("stat_semicol_",
                                   EXP_Y,
                                   ("assign", ("DIV_EQ", "/=")),
                                   EXP_FINV),
                                  ("NEWLINE", "\n"))),
                                ("statement",
                                 ("stat_loop",
                                  ("WHILE", "while"),
                                  EXP_Z,
                                  COLON,
                                  ("NEWLINE", "\n"),
                                  ("block",
                                   B_BEG,
                                   ("statement",
                                    ("stat_if",
                                     ("IF", "if"),
                                     EXP_ZIND,
                                     COLON,
                                     ("NEWLINE", "\n"),
                                     ("block",
                                      B_BEG,
                                      ("statement",
                                       ("stat_semicol",
                                        ("stat_semicol_",
                                         EXP_G,
                                         ("assign", EQUALS),
                                         EXP_7PXMY),
                                        ("NEWLINE", "\n"))),
                                      ("statement",
                                       ("stat_semicol",
                                        ("stat_semicol_",
                                         EXP_Y,
                                         ("assign", EQUALS),
                                         EXP_7PXMY),
                                        ("NEWLINE", "\n"))),
                                      B_END))),
                                   B_END))),
                                B_END))))
                self.assertEqual(output, answer)

                text      = \
"""
f(x, y, z)(x, y, z)
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_F2INV),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                text      = \
"""
f(x, y, z)[7](x, y, z)[7]
"""
                output    = parser.parser(tokenizer.tokenizer(text))
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("stat_semicol_", EXP_FLOTS),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

        def test_int_code_gen(self):
                EXP_1  = ("expression",
                          ("exp_log_and",
                           ("exp_log_not",
                            ("exp_comp",
                             ("exp_bit_or",
                              ("exp_bit_xor",
                               ("exp_bit_and",
                                ("exp_shift",
                                 ("exp_sum",
                                  ("exp_prod",
                                   ("exp_pdbn",
                                    ("exp_pow",
                                     ("exp_iis",
                                      ("exp_",
                                       ("NATURAL", "1")))))))))))))))
                EXP_2  = ("expression",
                          ("exp_log_and",
                           ("exp_log_not",
                            ("exp_comp",
                             ("exp_bit_or",
                              ("exp_bit_xor",
                               ("exp_bit_and",
                                ("exp_shift",
                                 ("exp_sum",
                                  ("exp_prod",
                                   ("exp_pdbn",
                                    ("exp_pow",
                                     ("exp_iis",
                                      ("exp_",
                                       ("NATURAL", "2")))))))))))))))
                EXP_7  = ("expression",
                          ("exp_log_and",
                           ("exp_log_not",
                            ("exp_comp",
                             ("exp_bit_or",
                              ("exp_bit_xor",
                               ("exp_bit_and",
                                ("exp_shift",
                                 ("exp_sum",
                                  ("exp_prod",
                                   ("exp_pdbn",
                                    ("exp_pow",
                                     ("exp_iis",
                                      ("exp_",
                                       ("NATURAL", "7")))))))))))))))
                EXP_X  = ("expression",
                          ("exp_log_and",
                           ("exp_log_not",
                            ("exp_comp",
                             ("exp_bit_or",
                              ("exp_bit_xor",
                               ("exp_bit_and",
                                ("exp_shift",
                                 ("exp_sum",
                                  ("exp_prod",
                                   ("exp_pdbn",
                                    ("exp_pow",
                                     ("exp_iis",
                                      ("exp_",
                                       ("VARIABLE", "x")))))))))))))))
                STAT_7 = ("statement",
                          ("stat_semicol",
                           ("stat_semicol_",
                            EXP_7)))
                STAT_X = ("statement",
                          ("stat_semicol",
                           ("stat_semicol_",
                            EXP_X)))

                ast    = ("comp", ("LS_THAN", "<"))
                output = int_code_gen.comp(ast)
                answer = "<"
                self.assertEqual(output, answer)

                ast    = ("assign", ("EQUALS", "="))
                output = int_code_gen.comp(ast)
                answer = "="
                self.assertEqual(output, answer)

                ast    = ("exp_", ("TRUE", "True"))
                output = int_code_gen.comp(ast)
                answer = "True"
                self.assertEqual(output, answer)

                ast    = ("exp_", ("L_PAREN", "("), EXP_7, ("R_PAREN", ")"))
                output = int_code_gen.exp_(ast)
                answer = "(7)"
                self.assertEqual(output, answer)

                ast    = ("exp_", ("L_BRACK", "["), ("R_BRACK", "]"))
                output = int_code_gen.exp_(ast)
                answer = "()"
                self.assertEqual(output, answer)

                ast    = ("exp_", ("L_BRACK", "["), EXP_7, ("R_BRACK", "]"))
                output = int_code_gen.exp_(ast)
                answer = "(7)"
                self.assertEqual(output, answer)

                ast    = ("exp_",
                          ("L_BRACK", "["),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_(ast)
                answer = "(7 7 7 7 7)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis", ("exp_", ("VARIABLE", "a")))
                output = int_code_gen.exp_iis(ast)
                answer = "a"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_PAREN", "("),
                          ("R_PAREN", ")"))
                output = int_code_gen.exp_iis(ast)
                answer = "(a)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_PAREN", "("),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("R_PAREN", ")"))
                output = int_code_gen.exp_iis(ast)
                answer = "(a 7 7 7)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_1,
                          ("COLON", ":"),
                          EXP_7,
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(slice a 1 7)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          ("COLON", ":"),
                          EXP_7,
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(slice a None 7)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_7,
                          ("COLON", ":"),
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(slice a 7 None)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          ("COLON", ":"),
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(slice a None None)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_2,
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(index a 2)"
                self.assertEqual(output, answer)

                ast    = ("exp_pow", ("exp_iis", ("exp_", ("VARIABLE", "a"))))
                output = int_code_gen.exp_pow(ast)
                answer = "a"
                self.assertEqual(output, answer)

                var_a  = ("exp_iis", ("exp_", ("VARIABLE", "a")))
                ast    = ("exp_pow", var_a, ("STARSTAR", "**"), var_a)
                output = int_code_gen.exp_pow(ast)
                answer = "(** a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_iis", ("exp_", ("VARIABLE", "a")))
                ast    = ("exp_pow",
                          var_a,
                          ("STARSTAR", "**"),
                          var_a,
                          ("STARSTAR", "**"),
                          var_a,
                          ("STARSTAR", "**"),
                          var_a)
                output = int_code_gen.exp_pow(ast)
                answer = "(** (** (** a a) a) a)"
                self.assertEqual(output, answer)

                ast    = ("exp_pdbn",
                          ("PLUS", "+"),
                          ("exp_pow",
                           ("exp_iis",
                            ("exp_",
                             ("VARIABLE", "a")))))
                output = int_code_gen.exp_pdbn(ast)
                answer = "(+ a)"
                self.assertEqual(output, answer)

                ast    = ("exp_pdbn",
                          ("PLUS", "+"),
                          ("DASH", "-"),
                          ("BIT_NOT", "~"),
                          ("exp_pow",
                           ("exp_iis",
                            ("exp_",
                             ("VARIABLE", "a")))))
                output = int_code_gen.exp_pdbn(ast)
                answer = "+-~a"
                answer = "(+ (- (~ a)))"
                self.assertEqual(output, answer)

                var_a  = ("exp_pdbn",
                          ("exp_pow",
                           ("exp_iis",
                            ("exp_",
                             ("VARIABLE", "a")))))
                ast    = ("exp_prod",
                          var_a,
                          ("STAR", "*"),
                          var_a)
                output = int_code_gen.exp_prod(ast)
                answer = "(* a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_pdbn",
                          ("exp_pow",
                           ("exp_iis",
                            ("exp_",
                             ("VARIABLE", "a")))))
                ast    = ("exp_prod",
                          var_a,
                          ("STAR", "*"),
                          var_a,
                          ("DIV", "/"),
                          var_a,
                          ("MOD", "%"),
                          var_a)
                output = int_code_gen.exp_prod(ast)
                answer = "(% (/ (* a a) a) a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_prod",
                          ("exp_pdbn",
                           ("exp_pow",
                            ("exp_iis",
                             ("exp_",
                              ("VARIABLE", "a"))))))
                ast    = ("exp_sum",
                          var_a,
                          ("PLUS", "+"),
                          var_a)
                output = int_code_gen.exp_sum(ast)
                answer = "(+ a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_prod",
                          ("exp_pdbn",
                           ("exp_pow",
                            ("exp_iis",
                             ("exp_",
                              ("VARIABLE", "a"))))))
                ast    = ("exp_sum",
                          var_a,
                          ("PLUS", "+"),
                          var_a,
                          ("DASH", "-"),
                          var_a,
                          ("PLUS", "+"),
                          var_a,
                          ("PLUS", "+"),
                          var_a)
                output = int_code_gen.exp_sum(ast)
                answer = "(+ (+ (- (+ a a) a) a) a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_sum",
                          ("exp_prod",
                           ("exp_pdbn",
                            ("exp_pow",
                             ("exp_iis",
                              ("exp_",
                               ("VARIABLE", "a")))))))
                ast    = ("exp_shift",
                          var_a,
                          ("L_SHIFT", "<<"),
                          var_a)
                output = int_code_gen.exp_shift(ast)
                answer = "(<< a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_sum",
                          ("exp_prod",
                           ("exp_pdbn",
                            ("exp_pow",
                             ("exp_iis",
                              ("exp_",
                               ("VARIABLE", "a")))))))
                ast    = ("exp_shift",
                          var_a,
                          ("L_SHIFT", "<<"),
                          var_a,
                          ("R_SHIFT", ">>"),
                          var_a,
                          ("L_SHIFT", "<<"),
                          var_a)
                output = int_code_gen.exp_shift(ast)
                answer = "(<< (>> (<< a a) a) a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_shift",
                          ("exp_sum",
                           ("exp_prod",
                            ("exp_pdbn",
                             ("exp_pow",
                              ("exp_iis",
                               ("exp_",
                                ("VARIABLE", "a"))))))))
                ast    = ("exp_bit_and",
                          var_a,
                          ("BIT_AND", "&"),
                          var_a)
                output = int_code_gen.exp_bit_and(ast)
                answer = "(& a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_shift",
                          ("exp_sum",
                           ("exp_prod",
                            ("exp_pdbn",
                             ("exp_pow",
                              ("exp_iis",
                               ("exp_",
                                ("VARIABLE", "a"))))))))
                ast    = ("exp_bit_and",
                          var_a,
                          ("BIT_AND", "&"),
                          var_a,
                          ("BIT_AND", "&"),
                          var_a,
                          ("BIT_AND", "&"),
                          var_a)
                output = int_code_gen.exp_bit_and(ast)
                answer = "(& (& (& a a) a) a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_bit_or",
                          ("exp_bit_xor",
                           ("exp_bit_and",
                            ("exp_shift",
                             ("exp_sum",
                              ("exp_prod",
                               ("exp_pdbn",
                                ("exp_pow",
                                 ("exp_iis",
                                  ("exp_",
                                   ("VARIABLE", "a")))))))))))
                ast    = ("exp_comp",
                          var_a,
                          ("comp", ("EQEQ", "==")),
                          var_a)
                output = int_code_gen.exp_comp(ast)
                answer = "(== a a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_bit_or",
                          ("exp_bit_xor",
                           ("exp_bit_and",
                            ("exp_shift",
                             ("exp_sum",
                              ("exp_prod",
                               ("exp_pdbn",
                                ("exp_pow",
                                 ("exp_iis",
                                  ("exp_",
                                   ("VARIABLE", "a")))))))))))
                ast    = ("exp_comp",
                          var_a,
                          ("comp", ("LS_THAN", "<")),
                          var_a,
                          ("comp", ("LS_TH_EQ", "<=")),
                          var_a,
                          ("comp", ("EQEQ", "==")),
                          var_a,
                          ("comp", ("IS", "is")),
                          var_a)
                output = int_code_gen.exp_comp(ast)
                answer = "(is (== (<= (< a a) a) a) a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_comp",
                          ("exp_bit_or",
                           ("exp_bit_xor",
                            ("exp_bit_and",
                             ("exp_shift",
                              ("exp_sum",
                               ("exp_prod",
                                ("exp_pdbn",
                                 ("exp_pow",
                                  ("exp_iis",
                                   ("exp_",
                                    ("VARIABLE", "a"))))))))))))
                ast    = ("exp_log_not",
                          ("LOG_NOT", "not"),
                          var_a)
                output = int_code_gen.exp_log_not(ast)
                answer = "(not a)"
                self.assertEqual(output, answer)

                var_a  = ("exp_comp",
                          ("exp_bit_or",
                           ("exp_bit_xor",
                            ("exp_bit_and",
                             ("exp_shift",
                              ("exp_sum",
                               ("exp_prod",
                                ("exp_pdbn",
                                 ("exp_pow",
                                  ("exp_iis",
                                   ("exp_",
                                    ("VARIABLE", "a"))))))))))))
                ast    = ("exp_log_not",
                          ("LOG_NOT", "not"),
                          ("LOG_NOT", "not"),
                          ("LOG_NOT", "not"),
                          var_a)
                output = int_code_gen.exp_log_not(ast)
                answer = "(not (not (not a)))"
                self.assertEqual(output, answer)

                ast    = EXP_7
                output = int_code_gen.expression(ast)
                answer = "7"
                self.assertEqual(output, answer)

                ast    = ("block",
                          ("BLOCK_BEG", ""),
                          STAT_7,
                          ("BLOCK_END", ""))
                output = int_code_gen.block(ast)
                answer = "(block 7)"
                self.assertEqual(output, answer)

                ast    = ("block",
                          ("BLOCK_BEG", ""),
                          STAT_7,
                          STAT_7,
                          STAT_7,
                          STAT_7,
                          ("BLOCK_END", ""))
                output = int_code_gen.block(ast)
                answer = "(block 7 7 7 7)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_", EXP_7)
                output = int_code_gen.stat_semicol_(ast)
                answer = "7"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_", EXP_X)
                output = int_code_gen.stat_semicol_(ast)
                answer = "x"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_",
                          EXP_X,
                          ("assign", ("EQUALS", "=")),
                          EXP_7)
                output = int_code_gen.stat_semicol_(ast)
                answer = "(= x 7)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_", ("CONTINUE", "continue"))
                output = int_code_gen.stat_semicol_(ast)
                answer = "(continue)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_", ("BREAK", "break"))
                output = int_code_gen.stat_semicol_(ast)
                answer = "(break)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_", ("RETURN", "return"))
                output = int_code_gen.stat_semicol_(ast)
                answer = "(return)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol_",
                          ("RETURN", "return"),
                          EXP_X)
                output = int_code_gen.stat_semicol_(ast)
                answer = "(return x)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol",
                          ("stat_semicol_", EXP_7),
                          tokenizer.NEWLINE)
                output = int_code_gen.stat_semicol(ast)
                answer = "7"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol",
                          ("stat_semicol_", EXP_X),
                          tokenizer.NEWLINE)
                output = int_code_gen.stat_semicol(ast)
                answer = "x"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol",
                          ("stat_semicol_",
                           EXP_X,
                           ("assign", ("EQUALS", "=")),
                           EXP_7),
                          tokenizer.NEWLINE)
                output = int_code_gen.stat_semicol(ast)
                answer = "(= x 7)"
                self.assertEqual(output, answer)

                ast    = ("stat_semicol",
                          ("stat_semicol_", EXP_7),
                          ("SEMICOL", ";"),
                          ("stat_semicol_", EXP_X),
                          ("SEMICOL", ";"),
                          ("stat_semicol_",
                           EXP_X,
                           ("assign", ("EQUALS", "=")),
                           EXP_7),
                          tokenizer.NEWLINE)
                output = int_code_gen.stat_semicol(ast)
                answer = "7\nx\n(= x 7)"
                self.assertEqual(output, answer)

                ast    = ("stat_func_def",
                          ("DEF", "def"),
                          ("VARIABLE", "f"),
                          ("L_PAREN", "("),
                          ("R_PAREN", ")"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_func_def(ast)
                answer = "(set f (func () (block 7)))"
                self.assertEqual(output, answer)

                ast    = ("stat_func_def",
                          ("DEF", "def"),
                          ("VARIABLE", "f"),
                          ("L_PAREN", "("),
                          ("VARIABLE", "x"),
                          ("R_PAREN", ")"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_func_def(ast)
                answer = "(set f (func (x) (block 7)))"
                self.assertEqual(output, answer)

                ast    = ("stat_func_def",
                          ("DEF", "def"),
                          ("VARIABLE", "my_func"),
                          ("L_PAREN", "("),
                          ("VARIABLE", "a"),
                          ("COMMA", ","),
                          ("VARIABLE", "b"),
                          ("COMMA", ","),
                          ("VARIABLE", "c"),
                          ("COMMA", ","),
                          ("VARIABLE", "d"),
                          ("R_PAREN", ")"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_func_def(ast)
                answer = "(set my_func (func (a b c d) (block 7)))"
                self.assertEqual(output, answer)

                ast    = ("stat_func_def",
                          ("DEF", "def"),
                          ("VARIABLE", "my_func"),
                          ("L_PAREN", "("),
                          ("VARIABLE", "a"),
                          ("COMMA", ","),
                          ("VARIABLE", "b"),
                          ("COMMA", ","),
                          ("VARIABLE", "c"),
                          ("COMMA", ","),
                          ("VARIABLE", "d"),
                          ("R_PAREN", ")"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           STAT_7,
                           STAT_7,
                           STAT_7,
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_func_def(ast)
                answer = "(set my_func (func (a b c d) (block 7 7 7 7 7)))"
                self.assertEqual(output, answer)

                ast    = ("stat_loop",
                          ("FOR", "for"),
                          ("VARIABLE", "i"),
                          ("IN", "in"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_loop(ast)
                answer = "(for i x (block 7))"
                self.assertEqual(output, answer)

                ast    = ("stat_loop",
                          ("WHILE", "while"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_loop(ast)
                answer = "(while x (block 7))"
                self.assertEqual(output, answer)

                ast    = ("stat_if",
                          ("IF", "if"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_if(ast)
                answer = "(if x (block 7) None)"
                self.assertEqual(output, answer)

                ast    = ("stat_if",
                          ("IF", "if"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELSE", "else"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_if(ast)
                answer = "(if x (block 7) (block 7))"
                self.assertEqual(output, answer)

                ast    = ("statement",
                          ("stat_if",
                           ("IF", "if"),
                           EXP_X,
                           ("COLON", ":"),
                           tokenizer.NEWLINE,
                           ("block",
                            ("BLOCK_BEG", ""),
                            STAT_7,
                            ("BLOCK_END", "")),
                           ("ELSE", "else"),
                           ("COLON", ":"),
                           tokenizer.NEWLINE,
                           ("block",
                            ("BLOCK_BEG", ""),
                            STAT_7,
                            ("BLOCK_END", ""))))
                output = int_code_gen.statement(ast)
                answer = "(if x (block 7) (block 7))"
                self.assertEqual(output, answer)

                ast    = ("statement",
                          ("stat_loop",
                           ("WHILE", "while"),
                           EXP_X,
                           ("COLON", ":"),
                           tokenizer.NEWLINE,
                           ("block",
                            ("BLOCK_BEG", ""),
                            STAT_7,
                            ("BLOCK_END", ""))))
                output = int_code_gen.statement(ast)
                answer = "(while x (block 7))"
                self.assertEqual(output, answer)

                ast    = ("statement",
                          ("stat_func_def",
                           ("DEF", "def"),
                           ("VARIABLE", "my_func"),
                           ("L_PAREN", "("),
                           ("VARIABLE", "a"),
                           ("COMMA", ","),
                           ("VARIABLE", "b"),
                           ("COMMA", ","),
                           ("VARIABLE", "c"),
                           ("COMMA", ","),
                           ("VARIABLE", "d"),
                           ("R_PAREN", ")"),
                           ("COLON", ":"),
                           tokenizer.NEWLINE,
                           ("block",
                            ("BLOCK_BEG", ""),
                            STAT_7,
                            ("BLOCK_END", ""))))
                output = int_code_gen.statement(ast)
                answer = "(set my_func (func (a b c d) (block 7)))"
                self.assertEqual(output, answer)

                ast    = ("statement",
                          ("stat_semicol",
                           ("stat_semicol_",
                            EXP_X,
                            ("assign", ("EQUALS", "=")),
                            EXP_7),
                           tokenizer.NEWLINE))
                output = int_code_gen.statement(ast)
                answer = "(= x 7)"
                self.assertEqual(output, answer)

                ast    = ("program", STAT_7)
                output = int_code_gen.program(ast)
                answer = "7"
                self.assertEqual(output, answer)

                ast    = ("program", STAT_7, STAT_7, STAT_7)
                output = int_code_gen.program(ast)
                answer = "7\n7\n7"
                self.assertEqual(output, answer)

                ast    = ("program", STAT_7)
                output = int_code_gen.int_code_gen(ast)
                answer = "7"
                self.assertEqual(output, answer)

                ast    = ("program", STAT_7, STAT_7, STAT_7)
                output = int_code_gen.int_code_gen(ast)
                answer = "7\n7\n7"
                self.assertEqual(output, answer)

                ast    = ("stat_if",
                          ("IF", "if"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELIF", "elif"),
                          EXP_1,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELSE", "else"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_if(ast)
                answer = "(if x (block 7) (if 1 (block 7) (block 7)))"
                self.assertEqual(output, answer)

                ast    = ("stat_if",
                          ("IF", "if"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELIF", "elif"),
                          EXP_1,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELIF", "elif"),
                          EXP_2,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELIF", "elif"),
                          EXP_7,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELIF", "elif"),
                          EXP_X,
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")),
                          ("ELSE", "else"),
                          ("COLON", ":"),
                          tokenizer.NEWLINE,
                          ("block",
                           ("BLOCK_BEG", ""),
                           STAT_7,
                           ("BLOCK_END", "")))
                output = int_code_gen.stat_if(ast)
                answer = "(if x (block 7) " + \
                         "(if 1 (block 7) " + \
                         "(if 2 (block 7) " + \
                         "(if 7 (block 7) " + \
                         "(if x (block 7) (block 7)" + 5 * ")"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_2,
                          ("R_BRACK", "]"),
                          ("L_BRACK", "["),
                          EXP_7,
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(index (index a 2) 7)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_2,
                          ("R_BRACK", "]"),
                          ("L_BRACK", "["),
                          EXP_7,
                          ("R_BRACK", "]"),
                          ("L_BRACK", "["),
                          ("COLON", ":"),
                          ("R_BRACK", "]"))
                output = int_code_gen.exp_iis(ast)
                answer = "(slice (index (index a 2) 7) None None)"
                self.assertEqual(output, answer)

                ast    = ("exp_iis",
                          ("exp_", ("VARIABLE", "a")),
                          ("L_BRACK", "["),
                          EXP_2,
                          ("R_BRACK", "]"),
                          ("L_BRACK", "["),
                          EXP_7,
                          ("R_BRACK", "]"),
                          ("L_BRACK", "["),
                          ("COLON", ":"),
                          ("R_BRACK", "]"),
                          ("L_PAREN", "("),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("COMMA", ","),
                          EXP_7,
                          ("R_PAREN", ")"))
                output = int_code_gen.exp_iis(ast)
                answer = "((slice (index (index a 2) 7) None None) 7 7 7)"
                self.assertEqual(output, answer)

        def test_source_to_int_code(self):
                file_   = "../__program_file__"
                cmd     = ["../source_to_int", file_]

                program = \
"""
x = 4 + y
"""
                with open(file_, "w") as f:
                        f.write(program)
                output  = subprocess.check_output(cmd).decode().rstrip()
                os.remove(file_)
                answer  = "(= x (+ 4 y))"
                self.assertEqual(output, answer)

                program = \
"""
x = 4 + y
x = 4 + y
"""
                with open(file_, "w") as f:
                        f.write(program)
                output  = subprocess.check_output(cmd).decode().rstrip()
                os.remove(file_)
                answer  = "(= x (+ 4 y))\n(= x (+ 4 y))"
                self.assertEqual(output, answer)
