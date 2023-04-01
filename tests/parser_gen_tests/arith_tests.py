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

        def test_arith_grammar(self):
                import arith_tokenizer
                import arith_grammar
                parser = parser_gen.parser_gen.parser_gen_(arith_tokenizer,
                                                      arith_grammar)

                # ========================================================

                plus   = ("PLUS", "+")
                minus  = ("MINUS", "-")
                mult   = ("MULT", "*")
                div    = ("DIV", "/")
                lprns  = ("LPARENS", "(")
                rprns  = ("RPARENS", ")")

                # ========================================================

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, plus, prod_1)
                answer = ("exp", sum_x)
                output = parser("1+1")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("1234+328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1, minus, prod_1)
                answer = ("exp", sum_x)
                output = parser("1-1")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("exp", sum_x)
                output = parser("1234-328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "823")
                val_1  = ("value", nat_1)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("823")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)
                prod_1 = ("product", val_1)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)*(87924)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("exp", sum_x)
                output = parser("1234*328")
                self.assertEqual(output, answer)

                # ========================================================

                nat_1  = ("NATURAL", "1234")
                val_1  = ("value", nat_1)
                nat_2  = ("NATURAL", "328")
                val_2  = ("value", nat_2)
                prod_x = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_x)
                answer = ("exp", sum_x)
                output = parser("1234/328")
                self.assertEqual(output, answer)

                # ========================================================

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
                answer = ("exp", sum_x)
                output = parser("11*22+3*5")
                self.assertEqual(output, answer)

                # ========================================================

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
                answer = ("exp", sum_x)
                output = parser("11/22+3*5")
                self.assertEqual(output, answer)

                # ========================================================

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
                answer = ("exp", sum_x)
                output = parser("11/22-3*5")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x  = ("NATURAL", "342")
                val_x  = ("value", nat_x)
                prod_x = ("product", val_x)
                sum_x  = ("sum", prod_x)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y  = ("NATURAL", "87924")
                val_y  = ("value", nat_y)
                prod_y = ("product", val_y)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(342)/(87924)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23+25)/(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, plus, prod_2)
                answer = ("exp", sum_x)
                output = parser("(23+25)+(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, mult, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23+25)*(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, plus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, mult, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1)
                prod_2 = ("product", val_2)
                sum_x  = ("sum", prod_1, minus, prod_2)
                answer = ("exp", sum_x)
                output = parser("(23+25)-(8*723)")
                self.assertEqual(output, answer)

                # ========================================================

                nat_x1 = ("NATURAL", "23")
                val_x1 = ("value", nat_x1)
                prodx1 = ("product", val_x1)
                nat_x2 = ("NATURAL", "25")
                val_x2 = ("value", nat_x2)
                prodx2 = ("product", val_x2)
                sum_x  = ("sum", prodx1, minus, prodx2)
                exp_x  = ("exp", sum_x)
                val_1  = ("value", lprns, exp_x, rprns)

                nat_y1 = ("NATURAL", "8")
                val_y1 = ("value", nat_y1)
                nat_y2 = ("NATURAL", "723")
                val_y2 = ("value", nat_y2)
                prod_y = ("product", val_y1, div, val_y2)
                sum_y  = ("sum", prod_y)
                exp_y  = ("exp", sum_y)
                val_2  = ("value", lprns, exp_y, rprns)

                prod_1 = ("product", val_1, div, val_2)
                sum_x  = ("sum", prod_1)
                answer = ("exp", sum_x)
                output = parser("(23-25)/(8/723)")
                self.assertEqual(output, answer)

                # ========================================================

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

                expone = ("exp", sumone)
                exptwo = ("exp", sumtwo)

                valone = ("value", lprns, expone, rprns)
                valtwo = ("value", lprns, exptwo, rprns)

                pone   = ("product", valone, div, valtwo)
                sone   = ("sum", pone)
                answer = ("exp", sone)
                output = parser("(11/22+3)/(8/17-4)")
                self.assertEqual(output, answer)

                # ========================================================

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
                exp_x  = ("exp", sum_x)
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
                exp_y  = ("exp", sum_y)
                val_b  = ("value", lprns, exp_y, rprns)

                prod_z = ("product", val_a, div, val_b)
                sum_z  = ("sum", prod_z)
                answer = ("exp", sum_z)
                output = parser("(11/22+3*5)/(8/17-4*6)")
                self.assertEqual(output, answer)

                n      = 10 * [[]]
                v      = 10 * [[]]
                p      = 10 * [[]]
                for i in range(1, 10):
                        n[i] = ("NATURAL", str(i))
                        v[i] = ("value",   n[i])
                        p[i] = ("product", v[i])

                # ========================================================

                s      = ("sum", p[1], plus, p[2], plus, p[3])
                answer = ("exp", s)
                output = parser("1+2+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], plus, p[9], plus, p[3])
                answer = ("exp", s)
                output = parser("7+8+9+3")
                self.assertEqual(output, answer)

                s      = ("sum", p[7], plus, p[8], minus, p[9], plus, p[3])
                answer = ("exp", s)
                output = parser("7+8-9+3")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], mult, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4*2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4/2*7")
                self.assertEqual(output, answer)

                p      = ("product", v[5], mult, v[4], div, v[2], mult, v[7])
                s      = ("sum", p)
                answer = ("exp", s)
                output = parser("5*4/2*7")
                self.assertEqual(output, answer)

                p5t4   = ("product", v[5], mult, v[4])
                s5t4   = ("sum", p5t4)
                e5t4   = ("exp", s5t4)
                v5t4   = ("value", lprns, e5t4, rprns)
                pxd2t7 = ("product", v5t4, div, v[2], mult, v[7])
                p9t1d3 = ("product", v[9], mult, v[1], div, v[3])
                p8t3d5 = ("product", v[8], mult, v[3], div, v[5])
                p6     = ("product", v[6])
                p3     = ("product", v[3])
                sxm6   = ("sum", p8t3d5, minus, p6)
                exm6   = ("exp", sxm6)
                vxm6   = ("value", lprns, exm6, rprns)
                pxm6   = ("product", vxm6)
                s      = ("sum", pxd2t7, plus, p3, minus, p9t1d3, plus, pxm6)
                answer = ("exp", s)
                output = parser("(5*4)/2*7+3-9*1/3+(8*3/5-6)")
                self.assertEqual(output, answer)

unittest.main()
