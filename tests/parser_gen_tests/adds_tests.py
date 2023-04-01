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
import string

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)

        def test_adds_grammar(self):
                import adds_tokenizer
                import adds_grammar
                parser = parser_gen.parser_gen.parser_gen_(adds_tokenizer,
                                                      adds_grammar)

                # ========================================================

                for let in string.ascii_lowercase:
                        setattr(sys.modules[__name__], let, (let.upper(), let))

                answer = ("start", ("one_or_more", b))
                output = parser("b")
                self.assertEqual(output, answer)

                answer = ("start", ("one_or_more", b, b, b, b, b))
                output = parser("bbbbb")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d))
                output = parser("d")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d, a))
                output = parser("da")
                self.assertEqual(output, answer)

                answer = ("start", ("zero_or_more", d, a, a, a, a, a))
                output = parser("daaaaa")
                self.assertEqual(output, answer)

                answer = ("start", ("optional", c, e))
                output = parser("ce")
                self.assertEqual(output, answer)

                answer = ("start", ("optional", e))
                output = parser("e")
                self.assertEqual(output, answer)

                answer = ("start", ("group", f, g))
                output = parser("fg")
                self.assertEqual(output, answer)

                answer = ("start", ("group", f, h))
                output = parser("fh")
                self.assertEqual(output, answer)

                answer = ("start", ("set", i, j, k))
                output = parser("ijk")
                self.assertEqual(output, answer)

unittest.main()
