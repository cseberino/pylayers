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

import parser_gen.add_prods
import unittest
import warnings

class Tester(unittest.TestCase):
        def setUp(self):
                warnings.simplefilter("ignore", ResourceWarning)

        def test_find_group(self):
                text   = "[abc(def)ghi]"
                output = parser_gen.add_prods.find_group(text)
                self.assertEqual(output, "(def)")

                text   = "[abc(defg(hijk)lmnop)]"
                output = parser_gen.add_prods.find_group(text)
                self.assertEqual(output, "(hijk)")

                text   = "[abcdefghij(((kl)))mno]"
                output = parser_gen.add_prods.find_group(text)
                self.assertEqual(output, "(kl)")

                text   = "[abce(fg)hijk(l)]"
                output = parser_gen.add_prods.find_group(text)
                self.assertEqual(output, "(fg)")

                text   = "[abcdefghij(((kl) ()))mno]"
                output = parser_gen.add_prods.find_group(text)
                self.assertEqual(output, "(kl)")

        def test_find_optional(self):
                text   = "(abc[def]ghi)"
                output = parser_gen.add_prods.find_optional(text)
                self.assertEqual(output, "[def]")

                text   = "(abc[defg[hijk]lmnop])"
                output = parser_gen.add_prods.find_optional(text)
                self.assertEqual(output, "[hijk]")

                text   = "(abcdefghij[[[kl]]]mno)"
                output = parser_gen.add_prods.find_optional(text)
                self.assertEqual(output, "[kl]")

                text   = "(abce[fg]hijk[l])"
                output = parser_gen.add_prods.find_optional(text)
                self.assertEqual(output, "[fg]")

                text   = "(abcdefghij[[[kl] []]]mno)"
                output = parser_gen.add_prods.find_optional(text)
                self.assertEqual(output, "[kl]")

unittest.main()
