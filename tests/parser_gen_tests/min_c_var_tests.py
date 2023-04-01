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
import unittest
import warnings

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)

        def test_min_c_var_tokenizer(self):
                import min_c_var_tokenizer

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
                          output = min_c_var_tokenizer.tokenizer(e[0])
                          self.assertEqual(output, answer)

        def test_min_c_var_grammar(self):
                import min_c_var_tokenizer
                import min_c_var_grammar
                p = parser_gen.parser_gen.parser_gen_(min_c_var_tokenizer,
                                                 min_c_var_grammar)

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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
4;
""")
                answer    = ("program",
                             ("statement",
                              ("stat_exp", EXP_4, SEMICOL)))
                self.assertEqual(output, answer)

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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

                output    = p("""
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
                output    = p("""
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
                output    = p("""
i = i + x + 1;
""")
                self.assertEqual(output, answer)

unittest.main()
