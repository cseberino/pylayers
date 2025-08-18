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

Tests the script, evaluator and library.
"""

import sys
sys.path.append("..")

import eval_
import exps
import unittest
import subprocess
import string
import re
import os

FUNC = r"<function (eval_{}|prep_args\.<locals>\.func_) at 0x[0-9a-f]*>"
ENV  = [e for e in dir(eval_) if e.startswith("eval_")]
ENV  = {(e[len("eval_"):],) : getattr(eval_, e) for e in ENV}

def run_and_print_all(program):
        with open("__program__", "w") as f:
                f.write(program)
        output = subprocess.check_output(["python3",
                                          "../interpreter_print_all",
                                          "__program__"])
        os.remove("__program__")

        return output

def run_only(program):
        with open("__program__", "w") as f:
                f.write(program)
        output = subprocess.check_output(["python3",
                                          "../interpreter",
                                          "__program__"])
        os.remove("__program__")

        return output

class Tester(unittest.TestCase):
        def setUp(self):
                with open("../interpreter") as f:
                        with open("../interpreter_print_all", "w") as g:
                                interpreter_     = f.readlines()
                                interpreter_[-1] = interpreter_[-1].replace(   \
                                                     "e,", '[("print",), e],')
                                g.write("".join(interpreter_))

        def tearDown(self):
                os.remove("../interpreter_print_all")

        def test_type_identifiers(self):
                self.assertTrue( eval_.is_var(("abc",)))
                self.assertTrue( eval_.is_var(("a3",)))
                self.assertTrue( eval_.is_var(("@^@^@%*",)))
                self.assertTrue( eval_.is_var(("#3a",)))
                self.assertTrue( eval_.is_var(("4abc",)))
                self.assertTrue( eval_.is_var(('ab"cd',)))
                self.assertTrue( eval_.is_var(('ab cd',)))
                self.assertTrue( eval_.is_var(("",)))
                self.assertTrue( eval_.is_var(("True",)))
                self.assertTrue( eval_.is_var(("False",)))
                self.assertTrue( eval_.is_var(("89",)))
                self.assertTrue( eval_.is_var(("-12",)))
                self.assertFalse(eval_.is_var(True))
                self.assertFalse(eval_.is_var(False))
                self.assertFalse(eval_.is_var(51))
                self.assertFalse(eval_.is_var(-93))
                self.assertFalse(eval_.is_var("abc"))
                self.assertFalse(eval_.is_var(2.6))
                self.assertFalse(eval_.is_var("True"))
                self.assertFalse(eval_.is_var("False"))
                self.assertFalse(eval_.is_var("89"))
                self.assertFalse(eval_.is_var("-12"))
                self.assertFalse(eval_.is_var("4abc"))
                self.assertFalse(eval_.is_var(""))

                self.assertTrue( eval_.is_atom(True))
                self.assertTrue( eval_.is_atom(False))
                self.assertTrue( eval_.is_atom(53))
                self.assertTrue( eval_.is_atom(-53))
                self.assertTrue( eval_.is_atom("abc"))
                self.assertTrue( eval_.is_atom(eval_.eval_quote))
                self.assertTrue( eval_.is_atom(eval_.eval_if))
                self.assertTrue( eval_.is_atom(("abc",)))
                self.assertTrue( eval_.is_atom(("a3",)))
                self.assertTrue( eval_.is_atom(("@^@^@%*",)))
                self.assertTrue( eval_.is_atom(("#3a",)))
                self.assertTrue( eval_.is_atom(("4abc",)))
                self.assertTrue( eval_.is_atom(('ab"cd',)))
                self.assertTrue( eval_.is_atom(('ab cd',)))
                self.assertTrue( eval_.is_atom(("",)))
                self.assertTrue( eval_.is_atom(("True",)))
                self.assertTrue( eval_.is_atom(("False",)))
                self.assertTrue( eval_.is_atom(("89",)))
                self.assertTrue( eval_.is_atom(("-12",)))
                self.assertTrue( eval_.is_atom("True"))
                self.assertTrue( eval_.is_atom("False"))
                self.assertTrue( eval_.is_atom("89"))
                self.assertTrue( eval_.is_atom("-12"))
                self.assertTrue( eval_.is_atom("4abc"))
                self.assertTrue( eval_.is_atom(""))
                self.assertFalse(eval_.is_atom(3.2))
                self.assertFalse(eval_.is_atom(-75.8))
                self.assertFalse(eval_.is_atom([]))
                self.assertFalse(eval_.is_atom([4]))
                self.assertFalse(eval_.is_atom(["abc"]))

                self.assertTrue( eval_.is_list(["abc"]))
                self.assertTrue( eval_.is_list(["abc", "set"]))
                self.assertTrue( eval_.is_list([3, ["a", "b"]]))
                self.assertTrue( eval_.is_list([3, [["a", "b"], "c"]]))
                self.assertTrue( eval_.is_list([False]))
                self.assertTrue( eval_.is_list(["abc",]))
                self.assertTrue( eval_.is_list([True, 3, "set"]))
                self.assertTrue( eval_.is_list([[True], [3], ["set"]]))
                self.assertFalse(eval_.is_list("abc"))
                self.assertFalse(eval_.is_list(True))
                self.assertFalse(eval_.is_list(False))
                self.assertFalse(eval_.is_list(3))
                self.assertFalse(eval_.is_list(-3))

        def test_quote(self):
                output = eval_.eval_quote([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_quote([4], {})
                answer = 4
                self.assertEqual(output, answer)

                output = eval_.eval_quote([-234], {})
                answer = -234
                self.assertEqual(output, answer)

                output = eval_.eval_quote([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_quote(["abc"], {})
                answer = "abc"
                self.assertEqual(output, answer)

                output = eval_.eval_quote([[True, 4, "abc"]], {})
                answer = [True, 4, "abc"]
                self.assertEqual(output, answer)

        def test_if(self):
                output = eval_.eval_if([True, 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = eval_.eval_if([98, 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = eval_.eval_if(["abc", 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = eval_.eval_if([False, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = eval_.eval_if([0, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = eval_.eval_if(["", 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = eval_.eval_if([[], 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = eval_.eval_if([0, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

        def test_prep_args(self):
                func_  = eval_.prep_args(lambda args, extra : 999)

                output = func_([1, 2, 3], {})
                answer = 999
                self.assertEqual(output, answer)

        def test_atom(self):
                output = eval_.eval_atom([False], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([63], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([-63], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom(["abc"], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([""], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([eval_.eval_quote], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([[]], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_atom([[("quote",), 4]], ENV)
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_atom([[("quote",), [3]]], ENV)
                answer = False
                self.assertEqual(output, answer)

        def test_equal(self):
                output = eval_.eval_equal([True, True], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal([False, False], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal([34, 34], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal([-92, -92], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal(["abc", "abc"], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal([True, False], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_equal([1, 2], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_equal([-6, -9], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_equal(["abc", "abd"], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_equal([[], []], {})
                answer = True
                self.assertEqual(output, answer)

                e = [("quote",), [3, 4]]
                f = [("quote",), [3, 5]]

                output = eval_.eval_equal([e, e], ENV)
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_equal([e, f], ENV)
                answer = False
                self.assertEqual(output, answer)

        def test_first(self):
                l      = [("quote",), [3, 5]]
                output = eval_.eval_first([l], ENV)
                answer = 3
                self.assertEqual(output, answer)

                l      = [("quote",), [[], 5]]
                output = eval_.eval_first([l], ENV)
                answer = []
                self.assertEqual(output, answer)

                l      = [("quote",), [[False, "abc"], True]]
                output = eval_.eval_first([l], ENV)
                answer = [False, "abc"]
                self.assertEqual(output, answer)

                l      = [("quote",), [[False, "abc"], [6, "abc", False]]]
                output = eval_.eval_first([l], ENV)
                answer = [False, "abc"]
                self.assertEqual(output, answer)

                l      = []
                output = eval_.eval_first([l], {})
                answer = []
                self.assertEqual(output, answer)

        def test_rest(self):
                l      = [("quote",), [3, 5]]
                output = eval_.eval_rest([l], ENV)
                answer = [5]
                self.assertEqual(output, answer)

                l      = [("quote",), [[], 5]]
                output = eval_.eval_rest([l], ENV)
                answer = [5]
                self.assertEqual(output, answer)

                l      = [("quote",), [[False, "abc"], True]]
                output = eval_.eval_rest([l], ENV)
                answer = [True]
                self.assertEqual(output, answer)

                l      = [("quote",), [[False, "abc"], [6, "abc", False]]]
                output = eval_.eval_rest([l], ENV)
                answer = [[6, "abc", False]]
                self.assertEqual(output, answer)

                l      = []
                output = eval_.eval_rest([l], {})
                answer = []
                self.assertEqual(output, answer)

        def test_append(self):
                l      = []
                output = eval_.eval_append([l, 3], {})
                answer = [3]
                self.assertEqual(output, answer)

                l      = [("quote",), [True, -4]]
                output = eval_.eval_append([l, False], ENV)
                answer = [True, -4, False]
                self.assertEqual(output, answer)

                l      = [("quote",), ["abc", []]]
                output = eval_.eval_append([l, l], ENV)
                answer = ["abc", [], ["abc", []]]
                self.assertEqual(output, answer)

        def test_add(self):
                output = eval_.eval_add([3, 4], {})
                answer = 7
                self.assertEqual(output, answer)

                output = eval_.eval_add([-3, -4], {})
                answer = -7
                self.assertEqual(output, answer)

                output = eval_.eval_add([-3, 4], {})
                answer = 1
                self.assertEqual(output, answer)

                output = eval_.eval_add([3, -4], {})
                answer = -1
                self.assertEqual(output, answer)

        def test_negate(self):
                output = eval_.eval_negate([3], {})
                answer = -3
                self.assertEqual(output, answer)

                output = eval_.eval_negate([-4], {})
                answer = 4
                self.assertEqual(output, answer)

                output = eval_.eval_negate([0], {})
                answer = 0
                self.assertEqual(output, answer)

                output = eval_.eval_negate([1], {})
                answer = -1
                self.assertEqual(output, answer)

                output = eval_.eval_negate([-1], {})
                answer = 1
                self.assertEqual(output, answer)

        def test_gt(self):
                output = eval_.eval_gt([5, 4], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_gt([3, 4], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_gt([-3, -4], {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_gt([-24, -4], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_gt([-24, 4], {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_gt([24, -4], {})
                answer = True
                self.assertEqual(output, answer)

        def test_set(self):
                extra  = ENV
                output = eval_.eval_set([("x",), True], extra)
                answer = True
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], True)

                extra  = ENV
                output = eval_.eval_set([("abc",), 4], extra)
                answer = 4
                self.assertEqual(output, answer)
                self.assertEqual(extra["abc",], 4)

                extra  = ENV
                output = eval_.eval_set([("&^%",), -62], extra)
                answer = -62
                self.assertEqual(output, answer)
                self.assertEqual(extra["&^%",], -62)

                extra  = ENV
                l      = [("quote",), [2, 4]]
                output = eval_.eval_set([("k9;",), l], extra)
                answer = l[1]
                self.assertEqual(output, answer)
                self.assertEqual(extra["k9;",], [2, 4])

                extra  = ENV
                l      = [("quote",), [2, True, []]]
                output = eval_.eval_set([("x",), l], extra)
                answer = l[1]
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], [2, True, []])

                extra  = ENV
                output = eval_.eval_set([("x",), []], extra)
                answer = []
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], [])

        def test_func(self):
                uf     = eval_.eval_func([[("a",)], 3], {})
                output = uf([45], {})
                answer = 3
                self.assertEqual(output, answer)

                uf     = eval_.eval_func([[("b",)], ("b",)], {})
                output = uf([56], {})
                answer = 56
                self.assertEqual(output, answer)

                params = [("c",), ("d",)]
                body   = [("equal",), ("c",), ("d",)]
                args   = [4, 4]
                answer = True
                uf     = eval_.eval_func([params, body], ENV)
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("e",), ("f",)]
                body   = [("equal",), ("e",), ("f",)]
                args   = [4, 8]
                answer = False
                uf     = eval_.eval_func([params, body], ENV)
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("g",), ("h",)]
                body   = [("first",),
                          [("append",), [("append",), [], ("g",)], ("h",)]]
                args   = [5, 6]
                answer = 5
                uf     = eval_.eval_func([params, body], ENV)
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("i",), ("j",)]
                body   = [("rest",),
                          [("append",), [("append",), [], ("i",)], ("j",)]]
                args   = [5, 6]
                answer = [6]
                uf     = eval_.eval_func([params, body], ENV)
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("k",), ("l",)]
                body   = [("add",), ("k",), ("l",)]
                args   = [-62, 100]
                answer = 38
                uf     = eval_.eval_func([params, body], ENV)
                output = uf(args, {})
                self.assertEqual(output, answer)

        def test_eval_(self):
                output = eval_.eval_(True, {})
                answer = True
                self.assertEqual(output, answer)

                output = eval_.eval_(False, {})
                answer = False
                self.assertEqual(output, answer)

                output = eval_.eval_(234, {})
                answer = 234
                self.assertEqual(output, answer)

                output = eval_.eval_(-79203987423, {})
                answer = -79203987423
                self.assertEqual(output, answer)

                output = eval_.eval_("abc", {})
                answer = "abc"
                self.assertEqual(output, answer)

                output = eval_.eval_(("quote",), ENV)
                answer = eval_.eval_quote
                self.assertEqual(output, answer)

                output = eval_.eval_(eval_.eval_negate, {})
                answer = eval_.eval_negate
                self.assertEqual(output, answer)

                output = eval_.eval_(("xv3",), {("xv3",) : -773})
                answer = -773
                self.assertEqual(output, answer)

                output = eval_.eval_([], {})
                answer = []
                self.assertEqual(output, answer)

                output = eval_.eval_([("quote",), [4, True]], ENV)
                answer = [4, True]
                self.assertEqual(output, answer)

                l      = [("append",), [("quote",), ["abc", 5]], False]
                output = eval_.eval_(l, ENV)
                answer = ["abc", 5, False]
                self.assertEqual(output, answer)

                addx   = [("func",),
                          [("x",), ("y",)],
                          [("add",), ("x",), ("y",)]]
                negx   = [("func",), [("x",)], [("negate",), ("x",)]]
                sub    = [("func",),
                          [("x",), ("y",)],
                          [addx, ("x",), [negx, ("y",)]]]
                add5   = [("func",), [("x",)], [addx, ("x",), 5]]

                output = eval_.eval_([add5, 100], ENV)
                answer = 105
                self.assertEqual(output, answer)

                output = eval_.eval_([sub, 57, 17], ENV)
                answer = 40
                self.assertEqual(output, answer)

                output = eval_.eval_([sub, [add5, 10], [add5, 3]], ENV)
                answer = 7
                self.assertEqual(output, answer)

                l      = [sub, [add5, -6], [sub, [add5, 95], 900]]
                output = eval_.eval_(l, ENV)
                answer = (-6 + 5) - ( (95 + 5) - 900 )
                self.assertEqual(output, answer)

        def test_tokenizer(self):
                output = exps.tokenizer("abc")
                answer = ["abc"]
                self.assertEqual(output, answer)

                output = exps.tokenizer("a b c")
                answer = ["a", "b", "c"]
                self.assertEqual(output, answer)

                output = exps.tokenizer("a (b c)")
                answer = ["a", "(", "b", "c", ")"]
                self.assertEqual(output, answer)

                output = exps.tokenizer("a (b c) efg (True 34) hij")
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                                                                     ")", "hij"]
                self.assertEqual(output, answer)

                prog   = 'x "Ala ka" y'
                output = exps.tokenizer(prog)
                answer = ["x", '"Ala ka"', "y"]
                self.assertEqual(output, answer)

                prog   = \
"""
a
(b c) efg
   (True 34)
      hij


"""
                output = exps.tokenizer(prog)
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                                                                     ")", "hij"]
                self.assertEqual(output, answer)

                prog   = \
"""
a
(b c) efg
   (True 34 "Alaska")
      hij


"""
                output = exps.tokenizer(prog)
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                                                         '"Alaska"', ")", "hij"]
                self.assertEqual(output, answer)

                prog   = \
"""
a
(b c) efg
   (True 34 "Ala\t ska")
      hij


"""
                output = exps.tokenizer(prog)
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                                                    '"Ala\t ska"', ")", "hij"]
                self.assertEqual(output, answer)

                prog   = \
"""
a
(b c) efg
   (True 34 "Ala\t ska")
      hij
  " b \r " k
 "hello world"
"""
                output = exps.tokenizer(prog)
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                          '"Ala\t ska"', ")", "hij", '" b \r "', "k",
                          '"hello world"']
                self.assertEqual(output, answer)

        def test_parser(self):
                input_ = '23 True "abc"'
                output = exps.parser(exps.tokenizer(input_))
                answer = [23, True, "abc"]
                self.assertEqual(output, answer)

                input_ = '23 True "abc" (a b c)'
                output = exps.parser(exps.tokenizer(input_))
                answer = [23, True, "abc", [("a",), ("b",), ("c",)]]
                self.assertEqual(output, answer)

                input_ = '23 True "abc" (a b ("hello" True -23 (4)) c)'
                output = exps.parser(exps.tokenizer(input_))
                answer = [23,
                          True,
                          "abc",
                          [("a",),
                           ("b",),
                           ["hello", True, -23, [4]],
                           ("c",)]]
                self.assertEqual(output, answer)

        def test_print_(self):
                program =  "True"
                answer  = b"True\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "False"
                answer  = b"False\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "345"
                answer  = b"345\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "-26726"
                answer  = b"-26726\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"hello"'
                answer  = b'"hello"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"y@H@h \n a \t abc \t kki"'
                answer  = b'"y@H@h \n a \t abc \t kki"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '" \t\n\x0b\x0c"'
                answer  = b'" \t\n\x0b\x0c"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  ' True   False   915   -61   "hello"  '
                answer  = \
b'''\
True
False
915
-61
"hello"
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
(quote ( 4 6 ))
(add 80 21)

(negate -6)

(if 4 5 6)
'''
                answer  = \
b'''\
(4 6)
101
6
5
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
True
False
-15
"hello"
(quote (5 False))
(quote (5 "hello" False))
(if (add 5 -5) -26 -91)
((func (x) (add x 5)) 10)
(set x 5)
(add -2 (negate x))
(atom True)
(atom ())
(atom quote)
(equal 4 4)
(equal -9 9)
(first  (quote (4 5 6)))
(rest   (quote (4 5 6)))
(append (quote (4 5 6)) 7)
(add 1 2)
(negate 9)
(gt 9 8)
(gt 8 9)
'''
                answer  = \
b'''\
True
False
-15
"hello"
(5 False)
(5 "hello" False)
-91
15
5
-7
True
False
True
True
False
4
(5 6)
(4 5 6 7)
3
-9
True
False
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "(atom quote)"
                answer  = b"True\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '(quote (5 "hello" False))'
                answer  = b'(5 "hello" False)\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "((func (x) (add x 5)) 10)"
                answer  = b"15\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_interpreter(self):
                program = "quote"
                answer  = FUNC.format("quote").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = "append"
                answer  = FUNC.format("append").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = "if"
                answer  = FUNC.format("if").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = "rest"
                answer  = FUNC.format("rest").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = "func"
                answer  = FUNC.format("func").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program =  '"abc"'
                answer  = b'"abc"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"True"'
                answer  = b'"True"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"False"'
                answer  = b'"False"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"916"'
                answer  = b'"916"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"-179"'
                answer  = b'"-179"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '"4abc"'
                answer  = b'"4abc"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  '""'
                answer  = b'""\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
(quote ( 4 6 ))
(add 80 21)

(negate -6)

(if 4 5 6)
'''
                answer  = \
b'''\
(4 6)
101
6
5
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program =  "(set αβΔ 46) αβΔ"
                answer  = b"46\n46\n"
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
# Comments must be ignored.
# Must allow strings with parens and whitespace!

"hello(there"

"hello)there"

"hello there"

"hello\nthere"

# Putting parens and spaces all in one string:
"hello ) ( \n there"
'''
                answer  = \
b'''\
"hello(there"
"hello)there"
"hello there"
"hello\nthere"
"hello ) ( \n there"
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = '"hello\nthere"\n'
                answer  = b'"hello\nthere"\n'
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_early_binding(self):
                program = \
'''
(set x 1)
(set f (func () x))
(set g (func (x) (f)))
(g 2)
(set x 3)
(g 2)
'''
                answer  = \
b'''\
1
3
3
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[3:]
                self.assertEqual(output, answer)

        def test_macro(self):
                program = "macro"
                answer  = FUNC.format("macro").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = "(macro (x) 5)"
                answer  = FUNC.format("macro.<locals>.macro").encode() + b"\n"
                output  = run_and_print_all(program)
                self.assertTrue(re.match(answer, output))

                program = \
'''
# Macros are code generation codes.
# Macros can receive arguments to make the code generation more flexible.
# Macros receive arguments unevaluated unlike regular functions.
# Macros can create special (irregular) functions.

# The following macro leads to "(if a True b)".
(set true-or-second (macro (a b) (append (append (append (quote (if)) a) True) b)))

# Gets replaced with "(if (add 1 5) True (negate 6))".
(true-or-second (add 1 5)  (negate 6))

(true-or-second (add 1 -1) (negate 6))
(true-or-second (negate 6) (add 1 -1))
(true-or-second (add 1 -1) (add 1 -1))
(true-or-second (add 1 45) ("This cannot be evaluated."))
'''
                answer  = \
b'''\
True
-6
True
0
True
'''
                answer  = [FUNC.format("macro.<locals>.macro").encode()] +     \
                                   answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")
                self.assertTrue(re.match(answer[0], output[0]) and             \
                                                   (output[1:] == answer[1:]))

        def test_log_and(self):
                program = \
'''
(and ""    1)
(and False 1)
(and ()    1)
(and 0     1)

(and ""    False)
(and False 0)
(and ()    "")
(and 0     ())

(and 24    "hello")
(and True  (quote (1 2)))
'''
                answer  = \
b'''\
False
False
False
False
False
False
False
False
True
True
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_log_or(self):
                program = \
'''
(or ""    1)
(or False 1)
(or ()    1)
(or 0     1)

(or ""    False)
(or False 0)
(or ()    "")
(or 0     ())

(or 24    "hello")
(or True  (quote (1 2)))
'''
                answer  = \
b'''\
True
True
True
True
False
False
False
False
True
True
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_basic_math(self):
                program = \
'''
(>   8  6)
(>   6  8)
(<   4 22)
(<  22  4)
(+   4  5)
(=   4  5)
(=  -7 -7)
(>=  5  6)
(>=  6  5)
(>=  5  5)
(<=  5  6)
(<=  6  5)
(<=  5  5)
(abs -9)
(abs  9)
(!= 3 4)
(!= 3 3)
'''
                answer  = \
b'''\
True
False
True
False
9
False
True
False
True
True
True
False
True
9
9
True
False
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_recursion(self):
                program = \
'''
(set adder
     (func (n)
           (if (<= n 1)
               n
               (+ n (adder (- n 1))))))

(adder   0)
(adder   1)
(adder   4)
(adder 100)
'''
                answer  = \
b'''\
0
1
10
5050
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)

        def test_mult(self):
                program = \
'''
(*   2  3)
(*  -2  3)
(*   2 -3)
(*  -2 -3)
(*   0  9)
(*   9  0)
(*  12 50)
(* 100 50)
'''
                answer  = \
b'''\
6
-6
-6
6
0
0
600
5000
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_div(self):
                program = \
'''
(/  10   2)
(/ -10   2)
(/  10  -2)
(/ -10  -2)
(/   0   2)
(/   0  -2)
(/   2  10)
(/  -2  10)
(/   2 -10)
(/  -2 -10)
(/  -2   0)
(/   2   0)
(/   0   0)
'''
                answer  = \
b'''\
5
-5
-5
5
0
0
0
0
0
0
()
()
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_exp(self):
                program = \
'''
(^  0  0)
(^  0  1)
(^  0 -1)
(^  0  2)
(^  0 -2)
(^  1  0)
(^  1  1)
(^  1 -1)
(^  1  2)
(^  1 -2)
(^  2  0)
(^  2  1)
(^  2 -1)
(^  2  2)
(^  2 -2)
(^ -1  0)
(^ -1  1)
(^ -1 -1)
(^ -1  2)
(^ -1 -2)
(^ -2  0)
(^ -2  1)
(^ -2 -1)
(^ -2  2)
(^ -2 -2)
(^  2  3)
(^ 10  2)
(^  2  7)
'''
                answer  = \
b'''\
()
0
()
0
()
1
1
1
1
1
1
2
0
4
0
1
-1
-1
1
1
1
-2
0
4
0
8
100
128
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_not(self):
                program = \
'''
(not 1)
(not 0)
(not ())
(not False)
(not "")
(not (+ 9 -9))
(not (+ 9  9))
'''
                answer  = \
b'''\
False
True
True
True
True
True
False
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_len(self):
                program = \
'''
(len ())
(len (quote (1)))
(len (quote (1 2)))
(len (quote (1 2 3)))
(len (quote ( (+ 1 2) True "hello" ("a" "b" "c" 4) )))
'''
                answer  = \
b'''\
0
1
2
3
4
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_func_any_len(self):
                program = \
'''
((func args        args ) 1 2 3 4)
((func args (first args)) 1 2 3 4)
((func args (rest  args)) 1 2 3 4)
'''
                answer  = \
b'''\
(1 2 3 4)
1
(2 3 4)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_index(self):
                program = \
'''
(index (quote (10 11 12))  0)
(index (quote (10 11 12))  1)
(index (quote (10 11 12))  2)
(index (quote (10 11 12)) -1)
(index (quote (10 11 12)) -2)
(index (quote (10 11 12)) -3)
(index (quote (34 35))  0)
(index (quote (34 35))  1)
(index (quote (34 35)) -1)
(index (quote (34 35)) -2)
'''
                answer  = \
b'''\
10
11
12
12
11
10
34
35
35
34
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_dash(self):
                program = \
'''
(- 4)
(- 4)
(- -98)
(-  9  5)
(-  9 -5)
(- -9  5)
(- -9 -5)
'''
                answer  = \
b'''\
-4
-4
98
4
14
-14
-4
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_block(self):
                program = \
'''
(block 1 2 3 4)
(block "hello")
(block (set a 2) (set b 3))
(* a b)
(block)
'''
                answer  = \
b'''\
4
"hello"
3
6
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_list(self):
                program = \
'''
(list 1 2)
(list 1)
(list)
(list (+ 1 2) (- 9 3) (* 3 4))
'''
                answer  = \
b'''\
(1 2)
(1)
()
(3 6 12)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_reverse(self):
                program = \
'''
(reverse (quote (1 2 3 4)))
(reverse (quote (1 2 3)))
(reverse (quote (1 2)))
(reverse (quote (1)))
(reverse (quote ()))
(reverse (list (+ 10 3) (* 3 4) (- 99 88)))
'''
                answer  = \
b'''\
(4 3 2 1)
(3 2 1)
(2 1)
(1)
()
(11 12 13)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_range(self):
                program = \
'''
(range 1  4  1)
(range 2 10  2)
(range 2 11  2)
(range 5  1 -1)
(range 5  1 -2)
(range 5  0 -2)
'''
                answer  = \
b'''\
(1 2 3)
(2 4 6 8)
(2 4 6 8 10)
(5 4 3 2)
(5 3)
(5 3 1)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_extend(self):
                program = \
'''
(extend (list 1 2) (list 3 4))
(extend (list 1 2) (list 3))
(extend (list 1 2) ())
(extend (list 1) (list 3 4))
(extend (list 1) (list 3))
(extend (list 1) ())
(extend () (list 3 4))
(extend () (list 3))
(extend () ())
'''
                answer  = \
b'''\
(1 2 3 4)
(1 2 3)
(1 2)
(1 3 4)
(1 3)
(1)
(3 4)
(3)
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_slice(self):
                program = \
'''
(slice (list "a" "b" "c" "d") 0 0)
(slice (list "a" "b" "c" "d") 0 1)
(slice (list "a" "b" "c" "d") 0 2)
(slice (list "a" "b" "c" "d") 0 3)
(slice (list "a" "b" "c" "d") 0 4)
(slice (list "a" "b" "c" "d") 1 0)
(slice (list "a" "b" "c" "d") 1 1)
(slice (list "a" "b" "c" "d") 1 2)
(slice (list "a" "b" "c" "d") 1 3)
(slice (list "a" "b" "c" "d") 1 4)
(slice (list "a" "b") 0 0)
(slice (list "a" "b") 0 1)
(slice (list "a" "b") 0 2)
(slice (list "a" "b") 1 0)
(slice (list "a" "b") 1 1)
(slice (list "a" "b") 1 2)
(slice (list "a") 0 0)
(slice (list "a") 0 1)
(slice (list "a") 1 0)
(slice (list "a") 1 1)
(slice () 0 0)
(slice () 0 1)
(slice (list "a" "b" "c" "d") -3 -1)
(slice (list "a" "b" "c" "d") -3 -2)
(slice (list "a" "b" "c" "d") -3  4)
(slice (list "a" "b" "c" "d")  0 ())
(slice (list "a" "b" "c" "d")  1 ())
(slice (list "a" "b" "c" "d")  2 ())
(slice (list "a" "b" "c" "d")  3 ())
(slice (list "a" "b" "c" "d")  3  1)
'''
                answer  = \
b'''\
()
("a")
("a" "b")
("a" "b" "c")
("a" "b" "c" "d")
()
()
("b")
("b" "c")
("b" "c" "d")
()
("a")
("a" "b")
()
()
("b")
()
("a")
()
()
()
()
("b" "c")
("b")
("b" "c" "d")
("a" "b" "c" "d")
("b" "c" "d")
("c" "d")
("d")
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_map(self):
                program = \
'''
(map not (list "" False 0 "hello" 8))
(map not (list "" False 0 () 1 "hello"))
(map not (list 1 0))
(map not (list 1))
(map not (list 0))
(map not ())
'''
                answer  = \
b'''\
(True True True False False)
(True True True True False False)
(False True)
(False)
(True)
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_zip(self):
                program = \
'''
(zip (list 1 2)   (list 3 4))
(zip (list 1 2 3) (list 3 4 5))
(zip (list 1)     (list 3))
(zip ()           ())
'''
                answer  = \
b'''\
((1 3) (2 4))
((1 3) (2 4) (3 5))
((1 3))
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_macro_any_len(self):
                program = \
'''
(set four (macro args 4))
(four 1 2 3)
'''
                answer  = \
b'''\
4
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)

                program = \
'''
(set head (macro args (append (quote (first)) (extend (quote (list)) args))))
(head 1 2 3)
(head "bat" "ball" "rock")
'''
                answer  = \
b'''\
1
"bat"
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)

                program = \
'''
(set tail (macro args (append (quote (rest)) (extend (quote (list)) args))))
(tail "bat" "ball" "rock")
'''
                answer  = \
b'''\
("ball" "rock")
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)

        def test_while(self):
                program = \
'''
(set i 5)
(while (< i 10)
       (set i (+ i 1)))
i

(set i 100)
(while (< i 150)
       (set i (+ i 1)))
i

(set i 100)
(set j 200)
(while (< i 150)
       (set i (+ i 1))
       (set j (+ j 1)))
i
j

(set i 100)
(set j 200)
(while (< (+ i j) 400)
       (set i (+ i 1))
       (set j (+ j 1)))
i
j
'''
                answer  = \
b'''\
5
True
10
100
True
150
100
200
True
150
250
100
200
True
150
250
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
(set fact
     (func (n)
           (set sum 1)
           (while (>= n 1)
                  (set sum (* sum n))
                  (set n   (- n   1)))
           sum))
(fact  3)
(fact 10)
(fact  0)
(fact  1)
'''
                answer  = \
b'''\
6
3628800
1
1
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)

        def test_second_third_last(self):
                program = \
'''
(second (list 5 6 7))
(third  (list 5 6 7))
(last   (list 5 6 7))
(second (list "a" "b" "c" "d"))
(third  (list "a" "b" "c" "d"))
(last   (list "a" "b" "c" "d"))
'''
                answer  = \
b'''\
6
7
7
"b"
"c"
"d"
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_for(self):
                program = \
'''
(set p 10)
(for i (list 3 4 5)
     (set p (+ p i)))
p

(set squares ())
(for i (list 0 1 2 3 4 5 6 7 8 9 10)
     (set squares (append squares (^ i 2))))
squares

(set p 10)
(for i (quote (3 4 5))
     (set p (+ p i)))
p

(set squares ())
(for i (quote (0 1 2 3 4 5 6 7 8 9 10))
     (set squares (append squares (^ i 2))))
squares

(set cubes ())
(for i (range 0 5 1)
     (set cubes (append cubes (^ i 3))))
cubes
'''
                answer  = \
b'''\
10
True
22
()
True
(0 1 4 9 16 25 36 49 64 81 100)
10
True
22
()
True
(0 1 4 9 16 25 36 49 64 81 100)
()
True
(0 1 8 27 64)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_evaluation_model(self):
                program = \
'''
# In the environment, f and g will be associated with the results of evaluating
#    (func (x) (g x)) and (func (x) x).
# (func (x) (g x)) and (func (x) x) are not functions but rather lists that
#    evaluate to functions.

(set f (func (x) (g x)))
(set g (func (x) x))

# Evaluating lists involves evaluating all the list elements.
# f evaluates to a function and (quote k) evaluates to k.
# In the environment, x will be associated with k.
# The result involves evaluating (g x) with the new environment.
# The result of evaluating (g x) with the new environment is the result of
#    invoking the function associated with g on k.

(f (quote k))

# g evaluates to a function and (quote k) evaluates to k.
# In the environment, x will be associated with k.
# The result involves evaluating x with the new environment.

(g (quote k))
'''
                answer  = \
b'''\
k
k
'''
                answer  = answer.split(b"\n")
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[2:]
                self.assertEqual(output, answer)

        def test_no_args(self):
                program = \
'''
(list)
(block)
'''
                answer  = \
b'''\
()
()
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_filter(self):
                program = \
'''
(filter (func (x) (> x 3)) (list 0 1 2 3 4 5 6))
(filter (func (x) (< x 3)) (list 0 1 2 3 4 5 6))
(filter not (list 0 1 2))
'''
                answer  = \
b'''\
(4 5 6)
(0 1 2)
(0)
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_reduce(self):
                program = \
'''
(reduce + (list 1 2 3 4))
(reduce * (list 1 2 3 4))
'''
                answer  = \
b'''\
10
24
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_macros_inside_functions(self):
                program = \
'''
# The for loop must find a corresponding list for l in the environment.

(set adder
     (func (l beg)
           (set sum beg)
           (for i l (set sum (+ sum i)))
           sum))

# The first argument passed to the adder is (5 10 15 20).
# The for loop will evaluate l which will return (5 10 15 20).

(adder (list 5 10 15 20) 6)
'''
                answer  = \
b'''\
56
'''
                output  = run_and_print_all(program)
                output  = output.split(b"\n")[1] + b"\n"
                self.assertEqual(output, answer)

        def test_mod(self):
                program = \
'''
(% 6 1)
(% 6 2)
(% 6 3)
(% 6 4)
(% 6 5)
(% 6 6)
(% 6 7)
(% 6 9)

(% 7 1)
(% 7 2)
(% 7 3)
(% 7 4)
(% 7 5)
(% 7 6)
(% 7 7)
(% 7 9)

(% -84 10)
(%  -7  5)
(%  -6  5)
(%  -5  5)
(%  -4  5)
(%  -3  5)
(%  -2  5)
(%  -1  5)
(%   0  5)
'''
                answer  = \
b'''\
0
0
0
2
1
0
6
6
0
1
1
3
2
1
0
7
6
3
4
0
1
2
3
4
0
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_l_shift(self):
                program = \
'''
(<< 1   1)
(<< 8   2)
(<< 0   4)
(<< 230 5)
(<< 231 5)
'''
                answer  = \
b'''\
2
32
0
7360
7392
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_r_shift(self):
                program = \
'''
(>> 2   1)
(>> 1   1)
(>> 8   2)
(>> 0   4)
(>> 230 5)
(>> 231 5)
'''
                answer  = \
b'''\
1
0
2
0
7
7
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_bit_and(self):
                program = \
'''
(& 37   0)
(&  8  49)
(& 15  38)
(& 41  46)
(& 82  74)
(& 66  54)
(& 84 100)
(& 22  50)
(& 39  58)
(& 12  85)
(&  0   0)
(&  1   0)
(&  0   1)
(&  1   1)
'''
                answer  = \
b'''\
0
0
6
40
66
2
68
18
34
4
0
0
0
1
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_bit_or(self):
                program = \
'''
(| 37   0)
(|  8  49)
(| 15  38)
(| 41  46)
(| 82  74)
(| 66  54)
(| 84 100)
(| 22  50)
(| 39  58)
(| 12  85)
(|  0   0)
(|  1   0)
(|  0   1)
(|  1   1)
'''
                answer  = \
b'''\
37
57
47
47
90
118
116
54
63
93
0
1
1
1
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_log_xor(self):
                program = \
'''
(xor ""    1)
(xor False 1)
(xor ()    1)
(xor 0     1)

(xor 1 ""   )
(xor 1 False)
(xor 1 ()   )
(xor 1 0    )

(xor 1 3)

(xor ""    False)
(xor False 0)
(xor ()    "")
(xor 0     ())

(xor 24    "hello")
(xor True  (quote (1 2)))

(xor 0 0)
'''
                answer  = \
b'''\
True
True
True
True
True
True
True
True
False
False
False
False
False
False
False
False
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_bit_xor(self):
                program = \
'''
(^^ 37   0)
(^^  8  49)
(^^ 15  38)
(^^ 41  46)
(^^ 82  74)
(^^ 66  54)
(^^ 84 100)
(^^ 22  50)
(^^ 39  58)
(^^ 12  85)
(^^  0   0)
(^^  1   0)
(^^  0   1)
(^^  1   1)
'''
                answer  = \
b'''\
37
57
41
7
24
116
48
36
29
89
0
1
1
0
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_bit_not(self):
                program = \
'''
(~ 1)
(~ 2)
(~ 0)
(~ -5)
(~ -2)
(~ -1)
(~ -0)
'''
                answer  = \
b'''\
-2
-3
-1
4
1
0
-1
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_prepend(self):
                program = \
'''
(prepend 7            (quote (4 5 6)))
(prepend ()           (quote (4 5 6)))
(prepend (list 1 2 3) (quote (4 5 6)))
(prepend 7            ())
(prepend ()           ())
(prepend (list 1 2 3) ())
'''
                answer  = \
b'''\
(7 4 5 6)
(() 4 5 6)
((1 2 3) 4 5 6)
(7)
(())
((1 2 3))
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

        def test_with_print(self):
                program = \
'''
(set i 10)
(set j 20)
(set k 30)
(set l (+ (+ i j) k))
'''
                answer  = \
b'''\
10
20
30
60
'''
                output  = run_and_print_all(program)
                self.assertEqual(output, answer)

                program = \
'''
(set i 10)
(set j 20)
(set k 30)
(set l (+ (+ i j) k))
(print l)
'''
                answer  = \
b'''\
60
'''
                output  = run_only(program)
                self.assertEqual(output, answer)

                program = \
'''
(set i 10)
(set j 20)
(set k 30)
(print (+ (+ i j) k))
'''
                answer  = \
b'''\
60
'''
                output  = run_only(program)
                self.assertEqual(output, answer)
