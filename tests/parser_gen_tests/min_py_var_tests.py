#!/usr/bin/env python3
#
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

import sys
sys.path.append("../..")

import parser_gen.parser_gen
import parser_gen.add_prods
import unittest
import warnings
import string

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)
                warnings.simplefilter("ignore", DeprecationWarning)

        def test_min_py_var_tokenizer(self):
                import min_py_var_tokenizer

                for e in [("+=",       "ADD_EQ"),
                          ("&=",       "B_AND_EQ"),
                          ("|=",       "B_OR_EQ"),
                          ("^=",       "B_XOR_EQ"),
                          ("&",        "BIT_AND"),
                          ("~",        "BIT_NOT"),
                          ("|",        "BIT_OR"),
                          ("^",        "BIT_XOR"),
                          ("break",    "BREAK"),
                          (":",        "COLON"),
                          (",",        "COMMA"),
                          ("continue", "CONTINUE"),
                          ("-",        "DASH"),
                          ("def",      "DEF"),
                          ("/",        "DIV"),
                          ("/=",       "DIV_EQ"),
                          ("elif",     "ELIF"),
                          ("else",     "ELSE"),
                          ("==",       "EQEQ"),
                          ("=",        "EQUALS"),
                          ("**=",      "EXP_EQ"),
                          ("False",    "FALSE"),
                          ("for",      "FOR"),
                          (">=",       "GR_TH_EQ"),
                          (">",        "GR_THAN"),
                          ("if",       "IF"),
                          ("in",       "IN"),
                          ("is",       "IS"),
                          ("{",        "L_BRACE"),
                          ("[",        "L_BRACK"),
                          ("and",      "LOG_AND"),
                          ("not",      "LOG_NOT"),
                          ("or",       "LOG_OR"),
                          ("(",        "L_PAREN"),
                          ("<<=",      "L_SH_EQ"),
                          ("<<",       "L_SHIFT"),
                          ("<=",       "LS_TH_EQ"),
                          ("<",        "LS_THAN"),
                          ("%",        "MOD"),
                          ("%=",       "MOD_EQ"),
                          ("*=",       "MULT_EQ"),
                          ("562",      "NATURAL"),
                          ("None",     "NONE"),
                          ("!=",       "NOT_EQ"),
                          ("+",        "PLUS"),
                          ("}",        "R_BRACE"),
                          ("]",        "R_BRACK"),
                          (")",        "R_PAREN"),
                          (">>=",      "R_SH_EQ"),
                          (">>",       "R_SHIFT"),
                          ("return",   "RETURN"),
                          (";",        "SEMICOL"),
                          ("*",        "STAR"),
                          ("**",       "STARSTAR"),
                          ('"hello"',  "STRING"),
                          ("-=",       "SUB_EQ"),
                          ("True",     "TRUE"),
                          ("temp",     "VARIABLE"),
                          ("while",    "WHILE")]:
                          answer = [(e[1], e[0]), ("NEWLINE", "\n")]
                          output = min_py_var_tokenizer.tokenizer(e[0])
                          self.assertEqual(output, answer)
                output = min_py_var_tokenizer.tokenizer("""
if 3:
     8
""")
                answer = [("IF",        "if"),
                          ("NATURAL",   "3"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("NATURAL",   "8"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

                output = min_py_var_tokenizer.tokenizer("""
def f(z):
    return z + 2

a = 3 + 4 ; f(x)

while x:
    for i in range(3):
         break
""")
                answer = [("DEF",       "def"),
                          ("VARIABLE",  "f"),
                          ("L_PAREN",   "("),
                          ("VARIABLE",  "z"),
                          ("R_PAREN",   ")"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("RETURN",    "return"),
                          ("VARIABLE",  "z"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "2"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", ""),
                          ("VARIABLE",  "a"),
                          ("EQUALS",    "="),
                          ("NATURAL",   "3"),
                          ("PLUS",      "+"),
                          ("NATURAL",   "4"),
                          ("SEMICOL",   ";"),
                          ("VARIABLE",  "f"),
                          ("L_PAREN",   "("),
                          ("VARIABLE",  "x"),
                          ("R_PAREN",   ")"),
                          ("NEWLINE",   "\n"),
                          ("WHILE",     "while"),
                          ("VARIABLE",  "x"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("FOR",       "for"),
                          ("VARIABLE",  "i"),
                          ("IN",        "in"),
                          ("VARIABLE",  "range"),
                          ("L_PAREN",   "("),
                          ("NATURAL",   "3"),
                          ("R_PAREN",   ")"),
                          ("COLON",     ":"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_BEG", ""),
                          ("BREAK",     "break"),
                          ("NEWLINE",   "\n"),
                          ("BLOCK_END", ""),
                          ("BLOCK_END", "")]
                self.assertEqual(output, answer)

        def test_min_py_var_grammar(self):
                import min_py_var_tokenizer
                import min_py_var_grammar
                p         = parser_gen.parser_gen.parser_gen_(min_py_var_tokenizer,
                                                         min_py_var_grammar)

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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base", ("VARIABLE", "range")),
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base",
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_F),
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_Z),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7),
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_Z),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7),
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_X),
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_Y),
                                         ("R_BRACK", "]"),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_Z),
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_Z),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7, COLON, EXP_Y),
                                         ("R_BRACK", "]"))))))))))))))
                EXP_ZSLB  = ("expression",
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_Z),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7, COLON, EXP_Y,
                                                                  COLON, EXP_Z),
                                         ("R_BRACK", "]"))))))))))))))
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
                                        ("exp_inv_elems",
                                         ("exp_base", ("NATURAL", "7")))))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_X))))))))))))))
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
                                        ("exp_inv_elems",
                                         ("exp_base", ("NATURAL", "7")))))),
                                     ("PLUS", "+"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_X))))),
                                     ("DASH", "-"),
                                     ("exp_prod",
                                      ("exp_pdbn",
                                       ("exp_pow",
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_Y))))))))))))))
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_F),
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
                                        ("exp_inv_elems",
                                         ("exp_base", VAR_F),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7),
                                         ("R_BRACK", "]"),
                                         ("L_PAREN", "("),
                                         EXP_X,
                                         COMMA,
                                         EXP_Y,
                                         COMMA,
                                         EXP_Z,
                                         ("R_PAREN", ")"),
                                         ("L_BRACK", "["),
                                         ("elements", EXP_7),
                                         ("R_BRACK", "]"))))))))))))))
                ST_7      = ("statement",
                             ("stat_semicol",
                              ("semicol_base", EXP_7),
                              ("NEWLINE", "\n")))
                ST_BREAK  = ("statement",
                             ("stat_semicol",
                              ("semicol_base", ("BREAK", "break")),
                              ("NEWLINE", "\n")))

                output    = p("""
continue
break
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("CONTINUE", "continue")),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("BREAK", "break")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
break ; continue
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", ("BREAK",    "break")),
                               SEMICOL,
                               ("semicol_base", ("CONTINUE", "continue")),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
while x:
        7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("WHILE", "while"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
if x:
        7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_if",
                               ("IF", "if"),
                               EXP_X,
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
if x:
        7
else:
        break
""")
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

                output    = p("""
if   x:
        7
elif y:
        7
elif z:
        break
else:
        break
""")
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

                output    = p("""
range(7)
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_R7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
def f():
        7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_func",
                               ("DEF", "def"),
                               VAR_F,
                               ("L_PAREN", "("),
                               ("R_PAREN", ")"),
                               COLON,
                               ("NEWLINE", "\n"),
                               ("block", B_BEG, ST_7, B_END))))
                self.assertEqual(output, answer)

                output    = p("""
def f(x, y, z):
        7
        break
""")
                answer    = ("program",
                             ("statement",
                              ("stat_func",
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

                output    = p("""
for x in range(7):
        7
        break
""")
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

                output    = p("""
None
True
False
"hello"
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_NONE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_TRUE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_FALSE),
                               ("NEWLINE", "\n"))),
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_HELLO),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
(7)
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_T7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
[7]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_L7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
[7, x, y]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_L7XY),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
x = 7
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base",
                                EXP_X, ("assign_op", EQUALS), EXP_7),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
return x
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base",
                                ("RETURN", "return"), EXP_X),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
f(x, y, z)
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_FINV),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
z[7]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_ZIND),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
z[7][x][y][z]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_ZIND4),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
z[7:y]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_ZSLS),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
z[7:y:z]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_ZSLB),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
7 + x
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_7PX),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
7 + x - y
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_7PXMY),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
for i in range(7):
        g += x
        y /= f(x, y, z)
        while z[7:y:z]:
                if z[7]:
                        g = 7 + x - y
                        y = 7 + x - y
""")
                answer    = ("program",
                             ("statement",
                              ("stat_loop",
                               ("FOR", "for"), VAR_I, ("IN", "in"), EXP_R7,
                                                       COLON, ("NEWLINE", "\n"),
                               ("block",
                                B_BEG,
                                ("statement",
                                 ("stat_semicol",
                                  ("semicol_base",
                                   EXP_G,
                                   ("assign_op", ("ADD_EQ", "+=")),
                                   EXP_X),
                                  ("NEWLINE", "\n"))),
                                ("statement",
                                 ("stat_semicol",
                                  ("semicol_base",
                                   EXP_Y,
                                   ("assign_op", ("DIV_EQ", "/=")),
                                   EXP_FINV),
                                  ("NEWLINE", "\n"))),
                                ("statement",
                                 ("stat_loop",
                                  ("WHILE", "while"),
                                  EXP_ZSLB,
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
                                        ("semicol_base",
                                         EXP_G,
                                         ("assign_op", EQUALS),
                                         EXP_7PXMY),
                                        ("NEWLINE", "\n"))),
                                      ("statement",
                                       ("stat_semicol",
                                        ("semicol_base",
                                         EXP_Y,
                                         ("assign_op", EQUALS),
                                         EXP_7PXMY),
                                        ("NEWLINE", "\n"))),
                                      B_END))),
                                   B_END))),
                                B_END))))
                self.assertEqual(output, answer)

                output    = p("""
f(x, y, z)(x, y, z)
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_F2INV),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

                output    = p("""
f(x, y, z)[7](x, y, z)[7]
""")
                answer    = ("program",
                             ("statement",
                              ("stat_semicol",
                               ("semicol_base", EXP_FLOTS),
                               ("NEWLINE", "\n"))))
                self.assertEqual(output, answer)

unittest.main()
