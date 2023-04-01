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

start = "program"

prods = \
"""
program     : statement+

statement   : stat_dec | stat_exp | stat_assign | stat_if | stat_loop
                                            | stat_jump | stat_block | stat_func

stat_dec    : declaration SEMICOL

stat_exp    : expression  SEMICOL

stat_assign : exp_prefix assign_op expression SEMICOL

stat_if     : IF L_PAREN expression R_PAREN stat_block [ELSE stat_block]

stat_loop   : WHILE L_PAREN expression R_PAREN stat_block
            | FOR L_PAREN stat_assign stat_exp exp_prefix assign_op expression
                                                              R_PAREN stat_block

stat_jump   : (BREAK | CONTINUE | RETURN [expression]) SEMICOL

stat_block  : L_BRACE statement+ R_BRACE

stat_func   : declaration stat_block

declaration : type STAR* dec_base [EQUALS expression]

dec_base    : VARIABLE (L_BRACK [expression] R_BRACK)+
            | VARIABLE L_PAREN [declaration (COMMA declaration)*] R_PAREN
            | VARIABLE

expression  : exp_log_and (LOG_OR              exp_log_and)*

exp_log_and : exp_log_not (LOG_AND             exp_log_not)*

exp_log_not : [LOG_NOT]   exp_comp

exp_comp    : exp_bit_or  (comp_op             exp_bit_or)*

exp_bit_or  : exp_bit_xor (BIT_OR              exp_bit_xor)*

exp_bit_xor : exp_bit_and (BIT_XOR             exp_bit_and)*

exp_bit_and : exp_shift   (AMPER               exp_shift)*

exp_shift   : exp_sum     ((L_SHIFT | R_SHIFT) exp_sum)*

exp_sum     : exp_prod    ((PLUS | DASH)       exp_prod)*

exp_prod    : exp_prefix  ((STAR | DIV | MOD)  exp_prefix)*

exp_prefix  : prefix_op* exp_inv_ind

exp_inv_ind : exp_base L_PAREN [expression (COMMA expression)*] R_PAREN
            | exp_base (L_BRACK expression R_BRACK)+
            | exp_base

exp_base    : NATURAL | STRING | VARIABLE | L_PAREN expression R_PAREN

assign_op   : EQUALS | ADD_EQ | SUB_EQ | MULT_EQ | DIV_EQ | MOD_EQ
                             | L_SH_EQ | R_SH_EQ | B_AND_EQ | B_OR_EQ | B_XOR_EQ

comp_op     : LS_THAN | LS_TH_EQ | GR_THAN | GR_TH_EQ | EQEQ | NOT_EQ

prefix_op   : PLUS | DASH | BIT_COMP | STAR | AMPER | SIZEOF
                                                          | L_PAREN type R_PAREN

type        : INT | CHAR | VOID
"""
prods = [e.split(":") for e in prods.split("\n\n")]
prods = dict([(e[0].strip(), e[1].strip()) for e in prods])
