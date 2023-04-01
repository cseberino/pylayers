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
sys.path += ["../.."]

import parser_gen.parser_gen
import python_tokenizer
import python_grammar
import int_code_gen
import unittest
import warnings
import subprocess

PARSER     = parser_gen.parser_gen.parser_gen_(python_tokenizer, python_grammar)
PROG_BEG   = int_code_gen.PROG_BEG
PRINT_HEAD = '("__PRINT__" '
INT        = "../../int_code_int/int_code_int"

def prog_to_int(program):
        return int_code_gen.int_code_gen(PARSER(program))

def prog_to_exec(program):
        int_    = int_code_gen.int_code_gen(PARSER(program))
        open("__int__", "w").write(int_)
        output_ = subprocess.check_output([INT, "__int__"]).decode()
        output_ = output_.split("\n")
        output  = []
        for i, e in enumerate(output_):
                if e.startswith(PRINT_HEAD) and e.endswith(")"):
                        output.append(e[len(PRINT_HEAD):-1])
        subprocess.call(["rm", "__int__"])

        return output

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)

        def test_True(self):
                output = prog_to_int("""
True
""")
                answer = PROG_BEG + "True"
                self.assertEqual(output, answer)

        def test_False(self):
                output = prog_to_int("""
False
""")
                answer = PROG_BEG + "False"
                self.assertEqual(output, answer)

        def test_naturals(self):
                output = prog_to_int("""
2345
""")
                answer = PROG_BEG + "2345"
                self.assertEqual(output, answer)

        def test_strings(self):
                output = prog_to_int("""
"hello"
""")
                answer = PROG_BEG + '"hello"'
                self.assertEqual(output, answer)

        def test_variables(self):
                output = prog_to_int("""
x
""")
                answer = PROG_BEG + "x"
                self.assertEqual(output, answer)

                output = prog_to_int("""
some_func
""")
                answer = PROG_BEG + "some_func"
                self.assertEqual(output, answer)

        def test_sums(self):
                output = prog_to_int("""
2 + 3
""")
                answer = PROG_BEG + "(+ 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 - 3
""")
                answer = PROG_BEG + "(- 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 + 3 + 4
""")
                answer = PROG_BEG + "(+ (+ 2 3) 4)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 + 3 + 4 - 5 - 6
""")
                answer = PROG_BEG + "(- (- (+ (+ 2 3) 4) 5) 6)"
                self.assertEqual(output, answer)

        def test_prods(self):
                output = prog_to_int("""
2 * 3
""")
                answer = PROG_BEG + "(* 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 / 3
""")
                answer = PROG_BEG + "(/ 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 * 3 / 4
""")
                answer = PROG_BEG + "(/ (* 2 3) 4)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 * 3 / 4 * 5 / 6
""")
                answer = PROG_BEG + "(/ (* (/ (* 2 3) 4) 5) 6)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 * 3 + 4
""")
                answer = PROG_BEG + "(+ (* 2 3) 4)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 + 3 * 4
""")
                answer = PROG_BEG + "(+ 2 (* 3 4))"
                self.assertEqual(output, answer)

        def test_bit_and(self):
                output = prog_to_int("""
2 & 3
""")
                answer = PROG_BEG + "(& 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 & 3 & 4
""")
                answer = PROG_BEG + "(& (& 2 3) 4)"
                self.assertEqual(output, answer)

        def test_bit_or(self):
                output = prog_to_int("""
2 | 3
""")
                answer = PROG_BEG + "(| 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 | 3 | 4
""")
                answer = PROG_BEG + "(| (| 2 3) 4)"
                self.assertEqual(output, answer)

        def test_bit_xor(self):
                output = prog_to_int("""
2 ^ 3
""")
                answer = PROG_BEG + "(^^ 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 ^ 3 ^ 4
""")
                answer = PROG_BEG + "(^^ (^^ 2 3) 4)"
                self.assertEqual(output, answer)

        def test_comps(self):
                output = prog_to_int("""
2 > 3
""")
                answer = PROG_BEG + "(> 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 <= 3
""")
                answer = PROG_BEG + "(<= 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 == 3
""")
                answer = PROG_BEG + "(= 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 != 3
""")
                answer = PROG_BEG + "(!= 2 3)"
                self.assertEqual(output, answer)

        def test_shifts(self):
                output = prog_to_int("""
2 >> 3
""")
                answer = PROG_BEG + "(>> 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 << 3
""")
                answer = PROG_BEG + "(<< 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 >> 3 - 4
""")
                answer = PROG_BEG + "(>> 2 (- 3 4))"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 + 3 << 4
""")
                answer = PROG_BEG + "(<< (+ 2 3) 4)"
                self.assertEqual(output, answer)

        def test_powers(self):
                output = prog_to_int("""
2 ** 3
""")
                answer = PROG_BEG + "(^ 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 ** 3 ** 4
""")
                answer = PROG_BEG + "(^ (^ 2 3) 4)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 ** 3 * 4
""")
                answer = PROG_BEG + "(* (^ 2 3) 4)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 * 3 ** 4
""")
                answer = PROG_BEG + "(* 2 (^ 3 4))"
                self.assertEqual(output, answer)

        def test_log_and(self):
                output = prog_to_int("""
2 and 3
""")
                answer = PROG_BEG + "(and 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 and "hello" and True
""")
                answer = PROG_BEG + '(and (and 2 "hello") True)'
                self.assertEqual(output, answer)

        def test_log_or(self):
                output = prog_to_int("""
2 or 3
""")
                answer = PROG_BEG + "(or 2 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 or "hello" or True
""")
                answer = PROG_BEG + '(or (or 2 "hello") True)'
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 and "hello" or True
""")
                answer = PROG_BEG + '(or (and 2 "hello") True)'
                self.assertEqual(output, answer)

                output = prog_to_int("""
2 or "hello" and True
""")
                answer = PROG_BEG + '(or 2 (and "hello" True))'
                self.assertEqual(output, answer)

        def test_log_not(self):
                output = prog_to_int("""
not 3
""")
                answer = PROG_BEG + "(not 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
not not not 3
""")
                answer = PROG_BEG + "(not (not (not 3)))"
                self.assertEqual(output, answer)

        def test_prefixes(self):
                output = prog_to_int("""
-3
""")
                answer = PROG_BEG + "(negate 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
~3
""")
                answer = PROG_BEG + "(~ 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
+3
""")
                answer = PROG_BEG + "3"
                self.assertEqual(output, answer)

                output = prog_to_int("""
- - ~ + - ~ 3
""")
                answer = PROG_BEG + "(negate (negate (~ (negate (~ 3)))))"
                self.assertEqual(output, answer)

        def test_func_calls(self):
                output = prog_to_int("""
f(x)
""")
                answer = PROG_BEG + "(f x)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f(x, y, 3)
""")
                answer = PROG_BEG + "(f x y 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
some_func(x + 5, y >> 9, 3 ** s(z))
""")
                answer = "(some_func (+ x 5) (>> y 9) (^ 3 (s z)))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
f(x)(y)
""")
                answer = PROG_BEG + "((f x) y)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f(x)(y)(z)
""")
                answer = PROG_BEG + "(((f x) y) z)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f()
""")
                answer = PROG_BEG + "(f)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f()()()(z)
""")
                answer = PROG_BEG + "((((f))) z)"
                self.assertEqual(output, answer)

        def test_indexing(self):
                output = prog_to_int("""
f[x]
""")
                answer = PROG_BEG + "(index f x)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f[x][7]
""")
                answer = PROG_BEG + "(index (index f x) 7)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f(t)[5]
""")
                answer = PROG_BEG + "(index (f t) 5)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f[5](t)
""")
                answer = PROG_BEG + "((index f 5) t)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
f[5](t)(x)[z](q)[5][2]
""")
                answer = "(index (index ((index (((index f 5) t) x) z) q) 5) 2)"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
f[5](t)()[z](q)[5][2]
""")
                answer = "(index (index ((index (((index f 5) t)) z) q) 5) 2)"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

        def test_stat_semicol(self):
                output = prog_to_int("""
x + 7 ; True ; range(10)
""")
                answer = PROG_BEG + "(+ x 7) True (range 10)"
                self.assertEqual(output, answer)

        def test_stat_if(self):
                output = prog_to_int("""
if 7:
        82
""")
                answer = PROG_BEG + "(if 7 (block 82) ())"
                self.assertEqual(output, answer)

                output = prog_to_int("""
if x + 1 < 9:
        f(x, y)
""")
                answer = "(if (< (+ x 1) 9) (block (f x y)) ())"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
if x + 1 < 9:
        f(x, y)
        g()
        z(w)
""")
                answer = "(if (< (+ x 1) 9) (block (f x y) (g) (z w)) ())"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
if 7:
        6
else:
        9
""")
                answer = PROG_BEG + "(if 7 (block 6) (block 9))"
                self.assertEqual(output, answer)

                output = prog_to_int("""
if   7:
        6
elif 8:
        2
else:
        9
""")
                answer = "(if 7 (block 6) (if 8 (block 2) (block 9)))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
if x + 1 < 9:
        f(x, y)
        g()
        z(w)
elif x < 9 * y:
        u(t)
        h(t)
else:
        a(t)
        b(t)
""")
                exp    = "(< (+ x 1) 9)"
                block  = "(block (f x y) (g) (z w))"
                else_  = "(block (a t) (b t))"
                elif_  = "(if (< x (* 9 y)) (block (u t) (h t)) {})"
                else_  = elif_.format(else_)
                answer = f"(if {exp} {block} {else_})"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

        def test_assignments(self):
                output = prog_to_int("""
x = 5
""")
                answer = PROG_BEG + "(def x 5)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
x = y % 5
""")
                answer = PROG_BEG + "(def x (% y 5))"
                self.assertEqual(output, answer)

                output = prog_to_int("""
x += 7
""")
                answer = PROG_BEG + "(def x (+ x 7))"
                self.assertEqual(output, answer)

                output = prog_to_int("""
x >>= g(x, y, z ** 4)
""")
                answer = PROG_BEG + "(def x (>> x (g x y (^ z 4))))"
                self.assertEqual(output, answer)

        def test_stat_loops(self):
                BEFORE = "(def <special> ())"
                F_BEG  = '(if (!= <special> "break") (def <special> ()) ())'
                W_BEG  = "(def <special> ())"
                W_COND = '(and {} (!= <special> "break"))'
                END    = "(if <special> <special> <None>)"
                WRAP   = "(if (not <special>) {} ())"
                ST_1   = WRAP.format("(def x (+ x 1))")
                ST_2   = WRAP.format("(def z (+ u v))")

                w_cond = W_COND.format("(< x 10)")
                stat   = WRAP.format("(def x (+ x 1))")
                output = prog_to_int("""
while x < 10:
        x += 1
""")
                answer = f"{BEFORE} (while {w_cond} (block {W_BEG} {stat}))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                w_cond = W_COND.format("(and (< x 10) y)")
                output = prog_to_int("""
while (x < 10) and y:
        x += 1
        z  = u + v
""")
                answer = f"{BEFORE} (while {w_cond} " + \
                                               f"(block {W_BEG} {ST_1} {ST_2}))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                stat   = WRAP.format("(def x (+ x 1))")
                output = prog_to_int("""
for i in range(10):
        x += 1
""")
                answer = f"{BEFORE} (for i (range 10) (block {F_BEG} {stat}))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                stat   = WRAP.format("(def x (+ x 1))")
                exp    = "((index (index z 3) 2) y)"
                output = prog_to_int("""
for j in z[3][2](y):
        x += 1
        z  = u + v
""")
                answer = f"{BEFORE} (for j {exp} (block {F_BEG} {ST_1} {ST_2}))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

        def test_stat_func(self):
                BEG    = "(def <special> ())"
                END    = "(if <special> <special> <None>)"
                WRAP   = "(if (not <special>) {} ())"

                stat   = WRAP.format("4")
                output = prog_to_int("""
def f(x):
        4
""")
                answer = f"(def f (func (x) (block {BEG} {stat} {END})))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
def f(x, y):
        y = range(x)
""")
                stat   = WRAP.format("(def y (range x))")
                answer = f"(def f (func (x y) (block {BEG} {stat} {END})))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
def f(x, y):
        y  = range(x)
        y += x
""")
                st_1   = WRAP.format("(def y (range x))")
                st_2   = WRAP.format("(def y (+ y x))")
                body   = f"{BEG} {st_1} {st_2} {END}"
                answer = f"(def f (func (x y) (block {body})))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

                output = prog_to_int("""
def f():
        94
""")
                stat   = WRAP.format("94")
                answer = f"(def f (func () (block {BEG} {stat} {END})))"
                answer = PROG_BEG + answer
                self.assertEqual(output, answer)

        def test_slices(self):
                output = prog_to_int("""
mylist[3]
""")
                answer = PROG_BEG + "(index mylist 3)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
mylist[3:5]
""")
                answer = PROG_BEG + "(slice mylist 3 5)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
mylist[3:]
""")
                answer = PROG_BEG + "(slice mylist 3 ())"
                self.assertEqual(output, answer)

                output = prog_to_int("""
mylist[:5]
""")
                answer = PROG_BEG + "(slice mylist 0 5)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
mylist[:]
""")
                answer = PROG_BEG + "(slice mylist 0 ())"
                self.assertEqual(output, answer)

        def test_lists(self):
                output = prog_to_int("""
[3, 4, 5]
""")
                answer = PROG_BEG + "(list 3 4 5)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
[z(u, v), x + y]
""")
                answer = PROG_BEG + "(list (z u v) (+ x y))"
                self.assertEqual(output, answer)

                output = prog_to_int("""
[]
""")
                answer = PROG_BEG + "(list)"
                self.assertEqual(output, answer)

        def test_return(self):
                output = prog_to_int("""
return
""")
                answer = PROG_BEG + "(def <special> <None>)"
                self.assertEqual(output, answer)

                output = prog_to_int("""
return (x < 7)
""")
                answer = PROG_BEG + "(def <special> (< x 7))"
                self.assertEqual(output, answer)

        def test_break_and_continue(self):
                output = prog_to_int("""
break
""")
                answer = PROG_BEG + '(def <special> "break")'
                self.assertEqual(output, answer)

                output = prog_to_int("""
continue
""")
                answer = PROG_BEG + '(def <special> "continue")'
                self.assertEqual(output, answer)

        def test_exec_exp(self):
                for e in [("7 + 3",      "10"),
                          ("7 - 3",       "4"),
                          ("7 * 3",      "21"),
                          ("7 / 3",       "2"),
                          ("2 ** 3",      "8"),
                          ("7 % 3",       "1"),
                          ("9 >> 2",      "2"),
                          ("9 << 2",     "36"),
                          ("44 & 7",      "4"),
                          ("44 | 7",     "47"),
                          ("44 ^ 7",     "43"),
                          ("3 < 7",    "True"),
                          ("3 <= 7",   "True"),
                          ("3 < 1",   "False"),
                          ("3 == 3",   "True"),
                          ("3 != 4",   "True"),
                          ("not 14",  "False"),
                          ("not 0",    "True"),
                          ("2 and 4",  "True"),
                          ("2 and 0", "False"),
                          ("2 or 0",   "True"),
                          ("2 or 2",   "True"),
                          ("0 or 0",  "False"),
                          ("~45",       "-46"),
                          ("-45",       "-45"),
                          ("--45",       "45"),
                          ("-~5",         "6"),
                          ("(4 + 5)",     "9"),
                ]:
                        output = prog_to_exec(f"print({e[0]})")
                        answer = [e[1]]
                        self.assertEqual(output, answer)

                output = prog_to_exec("""
7 + 3
""")
                answer = []
                self.assertEqual(output, answer)

                output = prog_to_exec("""
print((~3 + -8) * 7)
""")
                answer = ["-84"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
print( ( (~3 + -8) * 7 ) % 10 )
""")
                answer = ["6"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
print(3 + 9 * 2 / 5 ** 2 - 10)
""")
                answer = ["-7"]
                self.assertEqual(output, answer)

        def test_exec_assign(self):
                output = prog_to_exec("""
x = 5
print(x)
""")
                answer = ["5"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x  = 5
y  = 10
z  = x + y
z += 2
z -= 7
z *= 5
z /= 2
print(z)
""")
                answer = ["25"]
                self.assertEqual(output, answer)

        def test_exec_loops(self):
                output = prog_to_exec("""
y = 10
while y < 15:
        y = y + 1
print(y)
""")
                answer = ["15"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 5
y = 10
z = 1
while y < 15:
        x += 2
        z -= 10
        y  = y + 1
print(x)
print(y)
print(z)
""")
                answer = ["15", "15", "-49"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 0
for i in range(1, 11, 1):
        x += i
print(x)
""")
                answer = ["55"]
                self.assertEqual(output, answer)

        def test_exec_stat_semicol(self):
                output = prog_to_exec("""
x = 3 ; y = 4 ; z = 5 ; print(x) ; print(y) ; print(z)
""")
                answer = ["3", "4", "5"]
                self.assertEqual(output, answer)

        def test_exec_if(self):
                output = prog_to_exec("""
x = 1
if x == 5:
        x = 4
print(x)
""")
                answer = ["1"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 1
y = 4
if x == y - 3:
        x = 41
print(x)
""")
                answer = ["41"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 1
y = 4
if x == y - 3:
        x = 41
        y = 100
print(x)
print(y)
""")
                answer = ["41", "100"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 1
if x == 1:
        y = 3
else:
        y = 4
print(y)

x = 1
if x == 2:
        y = 3
else:
        y = 4
print(y)
""")
                answer = ["3", "4"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 1
if   x == 1:
        y = 10
elif x == 2:
        y = 20
else:
        y = 999
print(y)

x = 2
if   x == 1:
        y = 10
elif x == 2:
        y = 20
else:
        y = 999
print(y)

x = 25
if   x == 1:
        y = 10
elif x == 2:
        y = 20
else:
        y = 999
print(y)
""")
                answer = ["10", "20", "999"]
                self.assertEqual(output, answer)

        def test_exec_func(self):
                output = prog_to_exec("""
def f(x):
        return 2 * x

print(f(10))
""")
                answer = ["20"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
def adder(x, y):
        return x + y

print(adder(8, 14))
""")
                answer = ["22"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
def useless_1():
        return 4

print(useless_1())

def useless_2():
        4

print(useless_2())
""")
                answer = ["4", "<<None>>"]
                self.assertEqual(output, answer)

        def test_exec_indexing(self):
                output = prog_to_exec("""
data = [4, 5, 6]
print(data[1])
""")
                answer = ["5"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = ["apple", "boy", "pear", "cat", "dog"]
print(data[0])
print(data[4])
print(data[2])
""")
                answer = ['"apple"', '"dog"', '"pear"']
                self.assertEqual(output, answer)

        def test_exec_slicing(self):
                output = prog_to_exec("""
data = [4, 5, 6]
print(data[0:1])
""")
                answer = ["(4)"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = [4, 5, 6, 7, 8, 9, 10, 11]
print(data[2:5])
""")
                answer = ["(6 7 8)"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = ["a", "b", "c", 44, "e", "f"]
print(data[2:5])
""")
                answer = ['("c" 44 "e")']
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = ["a", "b", "c", 44, "e", "f"]
print(data[2:2])
""")
                answer = ["()"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = ["a", "b", "c", 44, "e", "f"]
print(data[2:])
""")
                answer = ['("c" 44 "e" "f")']
                self.assertEqual(output, answer)

                output = prog_to_exec("""
data = ["a", "b", "c", 44, "e", "f"]
print(data[:2])
""")
                answer = ['("a" "b")']
                self.assertEqual(output, answer)

        def test_exec_printing_lists(self):
                output = prog_to_exec("""
data = [4, 5, 6, "hello"]
print([data[0], data[-1], data[-2], data[99 - 98]])
""")
                answer = ['(4 "hello" 6 5)']
                self.assertEqual(output, answer)

        def test_exec_break(self):
                output = prog_to_exec("""
x = 0
while x < 300:
        x += 1
        if x == 127:
                break
print(x)
""")
                answer = ["127"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 0
for i in range(1, 11, 1):
        if i == 7:
                break
        x += i
print(x)
""")
                answer = ["21"]
                self.assertEqual(output, answer)

        def test_exec_continue(self):
                output = prog_to_exec("""
x = 0
y = 0
while x < 5:
        x += 1
        if x == 3:
                continue
        y += x
print(y)
""")
                answer = ["12"]
                self.assertEqual(output, answer)

                output = prog_to_exec("""
x = 0
for i in range(1, 11, 1):
        if i == 6:
                continue
        x += i
print(x)
""")
                answer = ["49"]
                self.assertEqual(output, answer)

        def test_exec_return(self):
                output = prog_to_exec("""
def f(x):
        if   x == 1:
                return 10
        elif x == 2:
                return 20
        elif x == 3:
                return 3 * 10
        else:
                return "Unknown value."

print([f(1), f(2), f(3), f("wow")])
""")
                answer = ['(10 20 30 "Unknown value.")']
                self.assertEqual(output, answer)

unittest.main()
