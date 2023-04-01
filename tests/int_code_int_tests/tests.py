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
sys.path.append("../../int_code_int")

import evaluate
import unittest
import warnings
import subprocess
import string
import re

FUNC  = "<function (core_{}|eval_args\.<locals>\.decor\.<locals>\.func_) "
FUNC += "at 0x[0-9a-f]*>"
INT   = "../../int_code_int/int_code_int"

def create_int_mod():
        subprocess.call(["cp", INT, "__int__.py"])
        contents = open("__int__.py").readlines()
        open("__int__.py", "w").write("".join(contents[:-2]))

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)
                warnings.simplefilter("ignore", DeprecationWarning)

        def test_type_identifiers(self):
                self.assertTrue( evaluate.is_int(34))
                self.assertTrue( evaluate.is_int(-34))
                self.assertTrue( evaluate.is_int(0))
                self.assertTrue( evaluate.is_int(1))
                self.assertTrue( evaluate.is_int(-1))
                self.assertFalse(evaluate.is_int(True))
                self.assertFalse(evaluate.is_int(False))
                self.assertFalse(evaluate.is_int("abc"))
                self.assertFalse(evaluate.is_int([]))

                self.assertTrue( evaluate.is_var(("abc",)))
                self.assertTrue( evaluate.is_var(("a3",)))
                self.assertTrue( evaluate.is_var(("@^@^@%*",)))
                self.assertTrue( evaluate.is_var(("#3a",)))
                self.assertTrue( evaluate.is_var(("4abc",)))
                self.assertTrue( evaluate.is_var(('ab"cd',)))
                self.assertTrue( evaluate.is_var(('ab cd',)))
                self.assertTrue( evaluate.is_var(("",)))
                self.assertTrue( evaluate.is_var(("True",)))
                self.assertTrue( evaluate.is_var(("False",)))
                self.assertTrue( evaluate.is_var(("89",)))
                self.assertTrue( evaluate.is_var(("-12",)))
                self.assertFalse(evaluate.is_var((True,)))
                self.assertFalse(evaluate.is_var((False,)))
                self.assertFalse(evaluate.is_var((244,)))
                self.assertFalse(evaluate.is_var((-92,)))
                self.assertFalse(evaluate.is_var((6.1,)))
                self.assertFalse(evaluate.is_var(True))
                self.assertFalse(evaluate.is_var(False))
                self.assertFalse(evaluate.is_var(51))
                self.assertFalse(evaluate.is_var(-93))
                self.assertFalse(evaluate.is_var("abc"))
                self.assertFalse(evaluate.is_var(2.6))
                self.assertFalse(evaluate.is_var(("a", "b")))
                self.assertFalse(evaluate.is_var("True"))
                self.assertFalse(evaluate.is_var("False"))
                self.assertFalse(evaluate.is_var("89"))
                self.assertFalse(evaluate.is_var("-12"))
                self.assertFalse(evaluate.is_var("4abc"))
                self.assertFalse(evaluate.is_var(""))

                self.assertTrue( evaluate.is_atom(True))
                self.assertTrue( evaluate.is_atom(False))
                self.assertTrue( evaluate.is_atom(53))
                self.assertTrue( evaluate.is_atom(-53))
                self.assertTrue( evaluate.is_atom("abc"))
                self.assertTrue( evaluate.is_atom(evaluate.core_noeval))
                self.assertTrue( evaluate.is_atom(evaluate.core_if))
                self.assertTrue( evaluate.is_atom(("abc",)))
                self.assertTrue( evaluate.is_atom(("a3",)))
                self.assertTrue( evaluate.is_atom(("@^@^@%*",)))
                self.assertTrue( evaluate.is_atom(("#3a",)))
                self.assertTrue( evaluate.is_atom(("4abc",)))
                self.assertTrue( evaluate.is_atom(('ab"cd',)))
                self.assertTrue( evaluate.is_atom(('ab cd',)))
                self.assertTrue( evaluate.is_atom(("",)))
                self.assertTrue( evaluate.is_atom(("True",)))
                self.assertTrue( evaluate.is_atom(("False",)))
                self.assertTrue( evaluate.is_atom(("89",)))
                self.assertTrue( evaluate.is_atom(("-12",)))
                self.assertTrue( evaluate.is_atom("True"))
                self.assertTrue( evaluate.is_atom("False"))
                self.assertTrue( evaluate.is_atom("89"))
                self.assertTrue( evaluate.is_atom("-12"))
                self.assertTrue( evaluate.is_atom("4abc"))
                self.assertTrue( evaluate.is_atom(""))
                self.assertFalse(evaluate.is_atom((True,)))
                self.assertFalse(evaluate.is_atom((False,)))
                self.assertFalse(evaluate.is_atom((244,)))
                self.assertFalse(evaluate.is_atom((-92,)))
                self.assertFalse(evaluate.is_atom((6.1,)))
                self.assertFalse(evaluate.is_atom(("a", "b")))
                self.assertFalse(evaluate.is_atom(3.2))
                self.assertFalse(evaluate.is_atom(-75.8))
                self.assertFalse(evaluate.is_atom(None))
                self.assertFalse(evaluate.is_atom([]))
                self.assertFalse(evaluate.is_atom([4]))
                self.assertFalse(evaluate.is_atom(["abc"]))

                self.assertTrue( evaluate.is_list(["abc"]))
                self.assertTrue( evaluate.is_list(["abc", "def"]))
                self.assertTrue( evaluate.is_list([3, ["a", "b"]]))
                self.assertTrue( evaluate.is_list([3, [["a", "b"], "c"]]))
                self.assertTrue( evaluate.is_list([False]))
                self.assertTrue( evaluate.is_list(["abc",]))
                self.assertTrue( evaluate.is_list([True, 3, "def"]))
                self.assertTrue( evaluate.is_list([[True], [3], ["def"]]))
                self.assertFalse(evaluate.is_list("abc"))
                self.assertFalse(evaluate.is_list(True))
                self.assertFalse(evaluate.is_list(False))
                self.assertFalse(evaluate.is_list(3))
                self.assertFalse(evaluate.is_list(-3))
                self.assertFalse(evaluate.is_list([2.6]))
                self.assertFalse(evaluate.is_list([None]))

        def test_noeval(self):
                output = evaluate.core_noeval([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([4], {})
                answer = 4
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([-234], {})
                answer = -234
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_noeval(["abc"], {})
                answer = "abc"
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([[True, 4, "abc"]], {})
                answer = [True, 4, "abc"]
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([True, 4], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([True, 4, "abc"], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([True, []], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_noeval([], {})
                answer = None
                self.assertEqual(output, answer)

        def test_if(self):
                output = evaluate.core_if([True, 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = evaluate.core_if([98, 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = evaluate.core_if(["abc", 345, 678], {})
                answer = 345
                self.assertEqual(output, answer)

                output = evaluate.core_if([False, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = evaluate.core_if([0, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = evaluate.core_if(["", 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = evaluate.core_if([[], 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

                output = evaluate.core_if([0, 345, 678], {})
                answer = 678
                self.assertEqual(output, answer)

        def test_eval_args(self):
                eval_args_ = evaluate.eval_args(3)
                func_      = eval_args_(lambda args, extra : 999)

                output = func_([1, 2], {})
                answer = None
                self.assertEqual(output, answer)

                output = func_([1, 2, 3], {})
                answer = 999
                self.assertEqual(output, answer)

                output = func_([1, 2, 3.5], {})
                answer = None
                self.assertEqual(output, answer)

        def test_atom(self):
                output = evaluate.core_atom([False], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([True], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([63], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([-63], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom(["abc"], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([""], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([evaluate.core_noeval], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([[]], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_atom([[("noeval",), 4]], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_atom([[("noeval",), [3]]], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_atom([4, 5], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_atom([2.7], {})
                answer = None
                self.assertEqual(output, answer)

        def test_equal(self):
                output = evaluate.core_equal([True, True], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal([False, False], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal([34, 34], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal([-92, -92], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal(["abc", "abc"], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal([True, False], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_equal([1, 2], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_equal([-6, -9], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_equal(["abc", "abd"], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_equal([[], []], {})
                answer = True
                self.assertEqual(output, answer)

                e = [("noeval",), [3, 4]]
                f = [("noeval",), [3, 5]]

                output = evaluate.core_equal([e, e], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_equal([e, e, e], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_equal([e, f], {})
                answer = False
                self.assertEqual(output, answer)

        def test_first(self):
                l      = [("noeval",), [3, 5]]
                output = evaluate.core_first([l], {})
                answer = 3
                self.assertEqual(output, answer)

                l      = [("noeval",), True]
                output = evaluate.core_first([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), False]
                output = evaluate.core_first([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), 57]
                output = evaluate.core_first([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), -57]
                output = evaluate.core_first([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), "abc"]
                output = evaluate.core_first([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), [[], 5]]
                output = evaluate.core_first([l], {})
                answer = []
                self.assertEqual(output, answer)

                l      = [("noeval",), [[False, "abc"], True]]
                output = evaluate.core_first([l], {})
                answer = [False, "abc"]
                self.assertEqual(output, answer)

                l      = [("noeval",), [[False, "abc"], [6, "abc", False]]]
                output = evaluate.core_first([l], {})
                answer = [False, "abc"]
                self.assertEqual(output, answer)

                l      = []
                output = evaluate.core_first([l], {})
                answer = []
                self.assertEqual(output, answer)

        def test_rest(self):
                l      = [("noeval",), [3, 5]]
                output = evaluate.core_rest([l], {})
                answer = [5]
                self.assertEqual(output, answer)

                l      = [("noeval",), True]
                output = evaluate.core_rest([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), False]
                output = evaluate.core_rest([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), 57]
                output = evaluate.core_rest([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), -57]
                output = evaluate.core_rest([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), "abc"]
                output = evaluate.core_rest([l], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), [[], 5]]
                output = evaluate.core_rest([l], {})
                answer = [5]
                self.assertEqual(output, answer)

                l      = [("noeval",), [[False, "abc"], True]]
                output = evaluate.core_rest([l], {})
                answer = [True]
                self.assertEqual(output, answer)

                l      = [("noeval",), [[False, "abc"], [6, "abc", False]]]
                output = evaluate.core_rest([l], {})
                answer = [[6, "abc", False]]
                self.assertEqual(output, answer)

                l      = []
                output = evaluate.core_rest([l], {})
                answer = []
                self.assertEqual(output, answer)

        def test_append(self):
                l      = []
                output = evaluate.core_append([l, 3], {})
                answer = [3]
                self.assertEqual(output, answer)

                l      = [("noeval",), [True, -4]]
                output = evaluate.core_append([l, False], {})
                answer = [True, -4, False]
                self.assertEqual(output, answer)

                l      = [("noeval",), ["abc", []]]
                output = evaluate.core_append([l, l], {})
                answer = ["abc", [], ["abc", []]]
                self.assertEqual(output, answer)

                output = evaluate.core_append([4, 3], {})
                answer = None
                self.assertEqual(output, answer)

                l      = [("noeval",), ["abc", []]]
                output = evaluate.core_append([l, 3, 4], {})
                answer = None
                self.assertEqual(output, answer)

        def test_add(self):
                output = evaluate.core_add([3, 4], {})
                answer = 7
                self.assertEqual(output, answer)

                output = evaluate.core_add([-3, -4], {})
                answer = -7
                self.assertEqual(output, answer)

                output = evaluate.core_add([-3, 4], {})
                answer = 1
                self.assertEqual(output, answer)

                output = evaluate.core_add([3, -4], {})
                answer = -1
                self.assertEqual(output, answer)

                output = evaluate.core_add([3, 4, 16], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_add([3, True], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_add(["abc", 4], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_add([3, []], {})
                answer = None
                self.assertEqual(output, answer)

        def test_negate(self):
                output = evaluate.core_negate([3], {})
                answer = -3
                self.assertEqual(output, answer)

                output = evaluate.core_negate([-4], {})
                answer = 4
                self.assertEqual(output, answer)

                output = evaluate.core_negate([0], {})
                answer = 0
                self.assertEqual(output, answer)

                output = evaluate.core_negate([1], {})
                answer = -1
                self.assertEqual(output, answer)

                output = evaluate.core_negate([-1], {})
                answer = 1
                self.assertEqual(output, answer)

                output = evaluate.core_negate([3, 4], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_negate([True], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_negate([False], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_negate(["abc"], {})
                answer = None
                self.assertEqual(output, answer)

        def test_gt(self):
                output = evaluate.core_gt([5, 4], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_gt([3, 4], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_gt([-3, -4], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_gt([-24, -4], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_gt([-24, 4], {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.core_gt([24, -4], {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.core_gt([3, 4, 16], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_gt([3, True], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_gt(["abc", 4], {})
                answer = None
                self.assertEqual(output, answer)

                output = evaluate.core_gt([3, []], {})
                answer = None
                self.assertEqual(output, answer)

        def test_def(self):
                extra  = {}
                output = evaluate.core_def([("x",), True], extra)
                answer = True
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], True)

                extra  = {}
                output = evaluate.core_def([("abc",), 4], extra)
                answer = 4
                self.assertEqual(output, answer)
                self.assertEqual(extra["abc",], 4)

                extra  = {}
                output = evaluate.core_def([("&^%",), -62], extra)
                answer = -62
                self.assertEqual(output, answer)
                self.assertEqual(extra["&^%",], -62)

                extra  = {}
                l      = [("noeval",), [2, 4]]
                output = evaluate.core_def([("k9;",), l], extra)
                answer = l[1]
                self.assertEqual(output, answer)
                self.assertEqual(extra["k9;",], [2, 4])

                extra  = {}
                l      = [("noeval",), [2, True, []]]
                output = evaluate.core_def([("x",), l], extra)
                answer = l[1]
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], [2, True, []])

                extra  = {}
                output = evaluate.core_def([("x",), []], extra)
                answer = []
                self.assertEqual(output, answer)
                self.assertEqual(extra["x",], [])

                extra  = {}
                output = evaluate.core_def([("[n9",), 3, 2], extra)
                answer = None
                self.assertEqual(output, answer)
                self.assertTrue(("[n9",) not in extra)

        def test_func(self):
                uf     = evaluate.core_func([[("a",)], 3], {})
                output = uf([45], {})
                answer = 3
                self.assertEqual(output, answer)

                uf     = evaluate.core_func([[("b",)], ("b",)], {})
                output = uf([56], {})
                answer = 56
                self.assertEqual(output, answer)

                params = [("c",), ("d",)]
                body   = [("equal",), ("c",), ("d",)]
                args   = [4, 4]
                answer = True
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("e",), ("f",)]
                body   = [("equal",), ("e",), ("f",)]
                args   = [4, 8]
                answer = False
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("g",), ("h",)]
                body   = [("first",),
                          [("append",), [("append",), [], ("g",)], ("h",)]]
                args   = [5, 6]
                answer = 5
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("i",), ("j",)]
                body   = [("rest",),
                          [("append",), [("append",), [], ("i",)], ("j",)]]
                args   = [5, 6]
                answer = [6]
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("k",), ("l",)]
                body   = [("add",), ("k",), ("l",)]
                args   = [-62, 100]
                answer = 38
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

                params = [("m",), True]
                body   = 2
                args   = [4, 8]
                answer = None
                uf     = evaluate.core_func([params, body], {})
                output = uf
                self.assertEqual(output, answer)

                params = [("n",)]
                body   = 2
                args   = [9, 1]
                answer = None
                uf     = evaluate.core_func([params, body], {})
                output = uf(args, {})
                self.assertEqual(output, answer)

        def test_evaluate(self):
                output = evaluate.evaluate(True, {})
                answer = True
                self.assertEqual(output, answer)

                output = evaluate.evaluate(False, {})
                answer = False
                self.assertEqual(output, answer)

                output = evaluate.evaluate(234, {})
                answer = 234
                self.assertEqual(output, answer)

                output = evaluate.evaluate(-79203987423, {})
                answer = -79203987423
                self.assertEqual(output, answer)

                output = evaluate.evaluate("abc", {})
                answer = "abc"
                self.assertEqual(output, answer)

                output = evaluate.evaluate(("noeval",), {})
                answer = evaluate.core_noeval
                self.assertEqual(output, answer)

                output = evaluate.evaluate(evaluate.core_negate, {})
                answer = evaluate.core_negate
                self.assertEqual(output, answer)

                output = evaluate.evaluate(("xv3",), {("xv3",) : -773})
                answer = -773
                self.assertEqual(output, answer)

                output = evaluate.evaluate([], {})
                answer = []
                self.assertEqual(output, answer)

                output = evaluate.evaluate([("noeval",), [4, True]], {})
                answer = [4, True]
                self.assertEqual(output, answer)

                l      = [("append",), [("noeval",), ["abc", 5]], False]
                output = evaluate.evaluate(l, {})
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

                output = evaluate.evaluate([add5, 100], {})
                answer = 105
                self.assertEqual(output, answer)

                output = evaluate.evaluate([sub, 57, 17], {})
                answer = 40
                self.assertEqual(output, answer)

                output = evaluate.evaluate([sub, [add5, 10], [add5, 3]], {})
                answer = 7
                self.assertEqual(output, answer)

                l      = [sub, [add5, -6], [sub, [add5, 95], 900]]
                output = evaluate.evaluate(l, {})
                answer = (-6 + 5) - ( (95 + 5) - 900 )
                self.assertEqual(output, answer)

        def test_tokenize(self):
                create_int_mod()
                import __int__ as int
                subprocess.call(["rm", "__int__.py"])

                output = int.tokenize("abc")
                answer = ["abc"]
                self.assertEqual(output, answer)

                output = int.tokenize("a b c")
                answer = ["a", "b", "c"]
                self.assertEqual(output, answer)

                output = int.tokenize("a (b c)")
                answer = ["a", "(", "b", "c", ")"]
                self.assertEqual(output, answer)

                output = int.tokenize("a (b c) efg (True 34) hij")
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                                                                     ")", "hij"]
                self.assertEqual(output, answer)

                prog   = 'x "Ala ka" y'
                output = int.tokenize(prog)
                answer = ["x", '"Ala ka"', "y"]
                self.assertEqual(output, answer)

                prog   = \
"""
a
(b c) efg
   (True 34)
      hij


"""
                output = int.tokenize(prog)
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
                output = int.tokenize(prog)
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
                output = int.tokenize(prog)
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
                output = int.tokenize(prog)
                answer = ["a", "(", "b", "c", ")", "efg", "(", "True", "34",
                          '"Ala\t ska"', ")", "hij", '" b \r "', "k",
                          '"hello world"']
                self.assertEqual(output, answer)

        def test_productionize(self):
                create_int_mod()
                import __int__ as int
                subprocess.call(["rm", "__int__.py"])

                output = int.productionize(["True"])
                answer = True
                self.assertEqual(output, answer)

                output = int.productionize(["False"])
                answer = False
                self.assertEqual(output, answer)

                output = int.productionize(["42"])
                answer = 42
                self.assertEqual(output, answer)

                output = int.productionize(["-789"])
                answer = -789
                self.assertEqual(output, answer)

                output = int.productionize(['"hello"'])
                answer = "hello"
                self.assertEqual(output, answer)

                output = int.productionize(["abc"])
                answer = ("abc",)
                self.assertEqual(output, answer)

                output = int.productionize(["(", "42", ")"])
                answer = [42]
                self.assertEqual(output, answer)

                tokens = ["(", "424", "True", '"abc"', "abc", ")"]
                output = int.productionize(tokens)
                answer = [424, True, "abc", ("abc",)]
                self.assertEqual(output, answer)

                tokens = ["(", "True", "(", "@#$", "b", ")", '"o%3"', "89", ")"]
                output = int.productionize(tokens)
                answer = [True, [("@#$",), ("b",)], "o%3", 89]
                self.assertEqual(output, answer)

                tokens = ["(", "(", "(", "-1", "False", "(", ")", ")", ")", ")"]
                output = int.productionize(tokens)
                answer = [[[-1, False, []]]]
                self.assertEqual(output, answer)

        def test_parse(self):
                create_int_mod()
                import __int__ as int
                subprocess.call(["rm", "__int__.py"])

                input_ = '23 True "abc"'
                output = int.parse(input_)
                answer = [23, True, "abc"]
                self.assertEqual(output, answer)

                input_ = '23 True "abc" (a b c)'
                output = int.parse(input_)
                answer = [23, True, "abc", [("a",), ("b",), ("c",)]]
                self.assertEqual(output, answer)

                input_ = '23 True "abc" (a b ("hello" True -23 (4)) c)'
                output = int.parse(input_)
                answer = [23,
                          True,
                          "abc",
                          [("a",),
                           ("b",),
                           ["hello", True, -23, [4]],
                           ("c",)]]
                self.assertEqual(output, answer)

        def test_format_(self):
                program =  "True"
                answer  = b"True\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "False"
                answer  = b"False\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "345"
                answer  = b"345\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "-26726"
                answer  = b"-26726\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"hello"'
                answer  = b'"hello"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"y@H@h \n a \t abc \t kki"'
                answer  = b'"y@H@h \n a \t abc \t kki"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '" \t\n\x0b\x0c"'
                answer  = b'" \t\n\x0b\x0c"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  ' True   False   915   -61   "hello"  '
                answer  = \
b'''\
True
False
915
-61
"hello"
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
(noeval ( 4 6 ))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
True
False
-15
"hello"
(noeval (5 False))
(noeval (5 "hello" False))
(if (add 5 -5) -26 -91)
((func (x) (add x 5)) 10)
(def x 5)
(add -2 (negate x))
(atom True)
(atom ())
(atom noeval)
(equal 4 4)
(equal -9 9)
(first (noeval (4 5 6)))
(rest (noeval (4 5 6)))
(append (noeval (4 5 6)) 7)
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "(atom noeval)"
                answer  = b"True\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '(noeval (5 "hello" False))'
                answer  = b'(5 "hello" False)\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "((func (x) (add x 5)) 10)"
                answer  = b"15\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_int_code_int(self):
                program = "noeval"
                answer  = FUNC.format("noeval").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = "append"
                answer  = FUNC.format("append").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = "if"
                answer  = FUNC.format("if").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = "rest"
                answer  = FUNC.format("rest").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = "func"
                answer  = FUNC.format("func").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program =  '"abc"'
                answer  = b'"abc"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"True"'
                answer  = b'"True"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"False"'
                answer  = b'"False"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"916"'
                answer  = b'"916"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"-179"'
                answer  = b'"-179"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '"4abc"'
                answer  = b'"4abc"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  '""'
                answer  = b'""\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "(4 5)"
                answer  = b"None\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  ")"
                answer  = b"None\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "abc"
                answer  = b"None\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
(noeval ( 4 6 ))
(add 80 21)

(6 7)

(negate -6)

(if 4 5 6)
'''
                answer  = \
b'''\
(4 6)
101
None
6
5
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "(noeval (3 5()"
                answer  = b"None\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program =  "(def αβΔ 46) αβΔ"
                answer  = b"46\n46\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = '"hello\nthere"\n'
                answer  = b'"hello\nthere"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = '"hello\\"there"\n'
                answer  = b'"hello\\"there"\n'
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_early_binding(self):
                program = \
'''
(def x 1)
(def f (func () x))
(def g (func (x) (f)))
(g 2)
(def x 3)
(g 2)
'''
                answer  = \
b'''\
1
3
3
'''
                answer  = answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[3:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_macro(self):
                program = "macro"
                answer  = FUNC.format("macro").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = "(macro foo (x) 5)"
                answer  = FUNC.format("macro.<locals>.macro").encode() + b"\n"
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertTrue(re.match(answer, output))
                subprocess.call(["rm", "__program__"])

                program = \
'''
# Macros are code generating codes.
# Macros can receive arguments to make the code generation more flexible.
# Macros receive any arguments unevaluated unlike regular functions.
# Can make functions with invocations involving special evaluation procedures.

# Leads to "(if <argument 1> True <argument 2>)".
# Defining the macro as "(noeval (if a True b))" avoids inserting the arguments!
(macro true-or-second (a b) (append (append (append (noeval (if)) a) True) b))

# Gets replaced with "(if (add 1 5) True (negate 6))".
(true-or-second (add 1 5)  (negate 6))
(true-or-second (add 1 -1) (negate 6))
(true-or-second (negate 6) (add 1 -1))
(true-or-second (add 1 -1) (add 1 -1))
("This cannot be evaluated.")
(true-or-second (add 1 -1) ("This cannot be evaluated."))
(true-or-second (add 1 45) ("This cannot be evaluated."))
'''
                answer  = \
b'''\
True
-6
True
0
None
None
True
'''
                answer  = [FUNC.format("macro.<locals>.macro").encode()] +     \
                                   answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")
                self.assertTrue(re.match(answer[0], output[0]) and             \
                                                   (output[1:] == answer[1:]))
                subprocess.call(["rm", "__program__"])

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
(and True  (noeval (1 2)))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(or True  (noeval (1 2)))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_recursion(self):
                program = \
'''
(def adder
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(/   2   0)
(/  -2   0)
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
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_len(self):
                program = \
'''
(len ())
(len (noeval (1)))
(len (noeval (1 2)))
(len (noeval (1 2 3)))
(len (noeval ( (+ 1 2) True "hello" ("a" "b" "c" 4) )))
'''
                answer  = \
b'''\
0
1
2
3
4
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_index(self):
                program = \
'''
(index (noeval (10 11 12))  0)
(index (noeval (10 11 12))  1)
(index (noeval (10 11 12))  2)
(index (noeval (10 11 12)) -1)
(index (noeval (10 11 12)) -2)
(index (noeval (10 11 12)) -3)
(index (noeval (34 35))  0)
(index (noeval (34 35))  1)
(index (noeval (34 35)) -1)
(index (noeval (34 35)) -2)
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_dash(self):
                program = \
'''
(- 4)
(- 4)
(- -98)
(- "hello")
(-  9  5)
(-  9 -5)
(- -9  5)
(- -9 -5)
(-  9  5  2)
'''
                answer  = \
b'''\
-4
-4
98
None
4
14
-14
-4
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_block(self):
                program = \
'''
(block 1 2 3 4)
(block "hello")
(block (def a 2) (def b 3))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_reverse(self):
                program = \
'''
(reverse (noeval (1 2 3 4)))
(reverse (noeval (1 2 3)))
(reverse (noeval (1 2)))
(reverse (noeval (1)))
(reverse (noeval ()))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_zip(self):
                program = \
'''
(zip (list 1 2)   (list 3 4))
(zip (list 1 2 3) (list 3 4 5))
(zip (list 1)     (list 3))
(zip ()           ())
(zip (list 1 2)   (list 3 4 5))
'''
                answer  = \
b'''\
((1 3) (2 4))
((1 3) (2 4) (3 5))
((1 3))
()
()
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_macro_any_len(self):
                program = \
'''
(macro four args 4)
(four 1 2 3)
'''
                answer  = \
b'''\
4
'''
                answer  = answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
(macro head args (append (noeval (first)) (extend (noeval (list)) args)))
(head 1 2 3)
(head "bat" "ball" "rock")
'''
                answer  = \
b'''\
1
"bat"
'''
                answer  = answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
(macro tail args (append (noeval (rest)) (extend (noeval (list)) args)))
(tail "bat" "ball" "rock")
'''
                answer  = \
b'''\
("ball" "rock")
'''
                answer  = answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_while(self):
                program = \
'''
(def i 5)
(while (< i 10)
       (def i (+ i 1)))
i

(def i 100)
(while (< i 150)
       (def i (+ i 1)))
i

(def i 100)
(def j 200)
(while (< i 150)
       (def i (+ i 1))
       (def j (+ j 1)))
i
j

(def i 100)
(def j 200)
(while (< (+ i j) 400)
       (def i (+ i 1))
       (def j (+ j 1)))
i
j

(def i 100)
(def j 200)
(while (< (+ i j) 400)
       (+ 1 1 1)
       (def i (+ i 1))
       (def j (+ j 1)))
i
j

(while)
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
100
200
None
150
250
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

                program = \
'''
(def fact
     (func (n)
           (def sum 1)
           (while (>= n 1)
                  (def sum (* sum n))
                  (def n   (- n   1)))
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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_for(self):
                program = \
'''
(def p 10)
(for i (list 3 4 5)
     (def p (+ p i)))
p

(def squares ())
(for i (list 0 1 2 3 4 5 6 7 8 9 10)
     (def squares (append squares (^ i 2))))
squares

(def p 10)
(for i (noeval (3 4 5))
     (def p (+ p i)))
p

(def squares ())
(for i (noeval (0 1 2 3 4 5 6 7 8 9 10))
     (def squares (append squares (^ i 2))))
squares

(def cubes ())
(for i (range 0 5 1)
     (def cubes (append cubes (^ i 3))))
cubes

(for)
(for i)
(for True)
(for False)
(for 2)
(for (list 1 2))
(for True        (list 1 2))
(for False       (list 1 2))
(for 2           (list 1 2))
(for (list 1 2)  (list 1 2))
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
None
None
None
None
None
None
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_evaluation_model(self):
                program = \
'''
# In the environment, f and g will be associated with the results of evaluating
#    (func (x) (g x)) and (func (x) x).
# (func (x) (g x)) and (func (x) x) are not functions but rather lists that
#    evaluate to functions.

(def f (func (x) (g x)))
(def g (func (x) x))

# Evaluating lists involves evaluating all the list elements.
# f evaluates to a function and (noeval k) evaluates to k.
# In the environment, x will be associated with k.
# The result involves evaluating (g x) with the new environment.
# The result of evaluating (g x) with the new environment is the result of
#    invoking the function associated with g on k.

(f (noeval k))

# g evaluates to a function and (noeval k) evaluates to k.
# In the environment, x will be associated with k.
# The result involves evaluating x with the new environment.

(g (noeval k))

# g evaluates to a function and k cannot be evaluated.

(g k)
'''
                answer  = \
b'''\
k
k
None
'''
                answer  = answer.split(b"\n")
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[2:]
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_wrong_numbers_of_args(self):
                program = \
'''
(noeval 1 2 3 4 5 6)
(if     1 2 3 4 5 6)
(def x  1 2 3 4 5 6)
(atom   1 2 3 4 5 6)
(equal  1 2 3 4 5 6)
(first  (noeval (1 2 3)) (noeval (4 5 6)))
(rest   (noeval (1 2 3)) (noeval (4 5 6)))
(append (noeval (1 2 3)) 4 5 6)
(add    1 2 3 4 5 6)
(negate 1 2 3 4 5 6)
(gt     1 2 3 4 5 6)
(abs    1 2 3 4 5 6)
(+      1 2 3 4 5 6)
(-      1 2 3 4 5 6)
(*      1 2 3 4 5 6)
(/      1 2 3 4 5 6)
(^      1 2 3 4 5 6)
(=      1 2 3 4 5 6)
(>      1 2 3 4 5 6)
(>=     1 2 3 4 5 6)
(<      1 2 3 4 5 6)
(<=     1 2 3 4 5 6)
(!=     1 2 3 4 5 6)
(and    1 2 3 4 5 6)
(not    1 2 3 4 5 6)
(or     1 2 3 4 5 6)
(map not (noeval (1 2 3)) (noeval (4 5 6)))
(extend  (noeval (1 2 3)) (noeval (4 5 6)) (noeval (7 8 9)))
(last    (noeval (1 2 3)) (noeval (4 5 6)))
(reverse (noeval (1 2 3)) (noeval (4 5 6)))
(slice   (noeval (1 2 3)) 4 5 6)
(zip     (noeval (1 2 3)) (noeval (4 5 6)) (noeval (7 8 9)))
(index   (noeval (1 2 3)) 4 5 6)
(len     (noeval (1 2 3)) (noeval (4 5 6)))
(range  1 2 3 4 5 6)
(second  (noeval (1 2 3)) (noeval (4 5 6)))
(third   (noeval (1 2 3)) (noeval (4 5 6)))
'''
                answer  = len([e for e in program.split("\n") if e]) * \
b'''\
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_wrong_types(self):
                program = \
'''
(def  1 2)
(func 1 2)
(macro x   1  2)
(macro 1 (x)  2)
(macro 1 args 2)
(first 1)
(rest  1)
(append 1 2)
(add "a"   1)
(add   1 "a")
(negate "a")
(gt   1 "a")
(gt "a"   1)
(abs "a")
(-    1 "a")
(-  "a"   1)
(/    1 "a")
(/  "a"   1)
(^    1 "a")
(^  "a"   1)
(*    1 "a")
(*  "a"   1)
(>=   1 "a")
(>= "a"   1)
(<    1 "a")
(<  "a"   1)
(<=   1 "a")
(<= "a"   1)
(map 4 (list 1 2))
(map not 1)
(for 1 (list 1 2) 3)
(for i          1 2)
(extend (list 1 2)          3)
(extend          3 (list 1 2))
(last    1)
(reverse 1)
(slice 1 0 1)
(slice (list 1 2) "a"   1)
(slice (list 1 2)   1 "a")
(zip (list 1 2)          1)
(zip          1 (list 1 2))
(index          0   1)
(index (list 1 2) "a")
(len 1)
(range   0   1 "a")
(range "a"   0   1)
(range   0 "a"   1)
(second 1)
(third  1)
'''
                answer  = len([e for e in program.split("\n") if e]) * \
b'''\
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_failed_evaluations(self):
                program = \
'''
(if (+ 1 1 1)         2         3)
(if 2         (+ 1 1 1)         3)
(def x (+ 1 1 1))
(atom  (+ 1 1 1))
(equal (+ 1 1 1)         2)
(equal 2         (+ 1 1 1))
(first (+ 1 1 1))
(rest  (+ 1 1 1))
(append        () (+ 1 1 1))
(append (+ 1 1 1)        ())
(add (+ 1 1 1)         2)
(add 2         (+ 1 1 1))
(negate (+ 1 1 1))
(gt (+ 1 1 1)         2)
(gt 2         (+ 1 1 1))
(abs (+ 1 1 1))
(-   (+ 1 1 1)         2)
(-   2         (+ 1 1 1))
(/   (+ 1 1 1)         2)
(/   2         (+ 1 1 1))
(^   (+ 1 1 1)         2)
(^   2         (+ 1 1 1))
(*   (+ 1 1 1)         2)
(*   2         (+ 1 1 1))
(=   (+ 1 1 1)         2)
(=   2         (+ 1 1 1))
(>=  (+ 1 1 1)         2)
(>=  2         (+ 1 1 1))
(<   (+ 1 1 1)         2)
(<   2         (+ 1 1 1))
(<=  (+ 1 1 1)         2)
(<=  2         (+ 1 1 1))
(!=  (+ 1 1 1)         2)
(!=  2         (+ 1 1 1))
(and (+ 1 1 1)         2)
(and 2         (+ 1 1 1))
(or  (+ 1 1 1)         2)
(not (+ 1 1 1))
(map (+ 1 1 1) (list 1 2))
(map    negate  (+ 1 1 1))
(for i (+ 1 1 1)         2)
(for i (list 1 2) (+ 1 1 1))
(while (+ 1 1 1)         2)
(extend (+ 1 1 1) (list 1 2))
(extend (list 1 2) (+ 1 1 1))
(last (+ 1 1 1))
(list 1 (+ 1 1 1))
(reverse (+ 1 1 1))
(slice (+ 1 1 1)          0         1)
(slice (list 1 2) (+ 1 1 1)         1)
(slice (list 1 2)         0 (+ 1 1 1))
(zip   (list 1 2)  (+ 1 1 1))
(zip   (+ 1 1 1)  (list 1 2))
(index  (+ 1 1 1)         0)
(index (list 1 2) (+ 1 1 1))
(len (+ 1 1 1))
(range (+ 1 1 1)         1         2)
(range         1 (+ 1 1 1)         2)
(range         1         2 (+ 1 1 1))
(second (+ 1 1 1))
(third  (+ 1 1 1))
'''
                answer  = len([e for e in program.split("\n") if e]) * \
b'''\
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_no_args(self):
                program = \
'''
(noeval)
(if)
(def)
(func)
(macro)
(atom)
(equal)
(first)
(rest)
(append)
(add)
(negate)
(gt)

(abs)
(add)
(dash)
(div)
(exp)
(mult)
(equal)
(gt)
(gtoe)
(lt)
(ltoe)
(not_eq)
(and)
(not)
(or)
(map)
(extend)
(last)
(reverse)
(slice)
(zip)
(index)
(len)
(range)
(second)
(third)
(for)
(while)
'''
                answer  = len([e for e in program.split("\n") if e]) * \
b'''\
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_filter(self):
                program = \
'''
(filter (func (x) (> x 3)) (list 0 1 2 3 4 5 6))
(filter (func (x) (< x 3)) (list 0 1 2 3 4 5 6))
(filter not (list 0 1 2))
(filter)
(filter not)
(filter not (list 1 2) (list 3 4))
(filter not 1 2 3 4 5)
(filter not 1)
(filter 1   (list 1 2))
(filter 1   1)
'''
                answer  = \
b'''\
(4 5 6)
(0 1 2)
(0)
None
None
None
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_reduce(self):
                program = \
'''
(reduce + (list 1 2 3 4 5))
(reduce * (list 1 2 3 4 5))
(reduce)
(reduce +)
(reduce + (list 1 2) (list 3 4))
(reduce + 1 2 3 4)
(reduce 1 (list 1 2))
(reduce + 1)
'''
                answer  = \
b'''\
15
120
None
None
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_macros_inside_functions(self):
                program = \
'''
# The for loop must find a corresponding list for l in the environment.

(def adder
     (func (l beg)
           (def sum beg)
           (for i l (def sum (+ sum i)))
           sum))

# The first argument passed to the adder is (5 10 15 20).
# The for loop will evaluate l which will return (5 10 15 20).

(adder (list 5 10 15 20) 6)
'''
                answer  = \
b'''\
56
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                output  = output.split(b"\n")[1] + b"\n"
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_mod(self):
                program = \
'''
(% 6 0)
(% 6 1)
(% 6 2)
(% 6 3)
(% 6 4)
(% 6 5)
(% 6 6)
(% 6 7)
(% 6 9)

(% 7 0)
(% 7 1)
(% 7 2)
(% 7 3)
(% 7 4)
(% 7 5)
(% 7 6)
(% 7 7)
(% 7 9)
(%)
(% 1 2 3 4)
(% "hello" 1)
(% 1 "hello")
(% -84 10)
'''
                answer  = \
b'''\
None
0
0
0
2
1
0
6
6
None
0
1
1
3
2
1
0
7
None
None
None
None
6
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_l_shift(self):
                program = \
'''
(<< 1   1)
(<< 8   2)
(<< 0   4)
(<< 230 5)
(<< 231 5)
(<<)
(<< 1 2 3 4 5)
(<< 1 "hello")
(<< "hello" 1)
'''
                answer  = \
b'''\
2
32
0
7360
7392
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

        def test_r_shift(self):
                program = \
'''
(>> 2   1)
(>> 1   1)
(>> 8   2)
(>> 0   4)
(>> 230 5)
(>> 231 5)
(>>)
(>> 1 2 3 4 5)
(>> 1 "hello")
(>> "hello" 1)
'''
                answer  = \
b'''\
1
0
2
0
7
7
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(&)
(& 1 2 3 4 5)
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
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(|)
(| 1 2 3 4 5)
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
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(xor True  (noeval (1 2)))

(xor)
(xor 1 2 3 4 5)
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
None
None
False
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(^^)
(^^ 1 2 3 4 5)
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
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

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
(~)
(~ 1 2 3 4 5)
(~ "hello")
(~ True)
(~ ())
(~ (list 1 2 3))
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
None
None
None
None
None
None
'''
                open("__program__", "w").write(program)
                output  = subprocess.check_output([INT, "__program__"])
                self.assertEqual(output, answer)
                subprocess.call(["rm", "__program__"])

unittest.main()
