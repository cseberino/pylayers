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

Tests the script and assembler.
"""

import unittest
import subprocess
import os

def mach_code(program):
        with open("__program__", "w") as f:
                f.write(program)
        mach_code_ = subprocess.check_output(["../asm_to_mach", "__program__"])
        mach_code_ = bytes.fromhex(mach_code_.decode())
        os.remove("__program__")

        return mach_code_

class Tester(unittest.TestCase):
        def test_add_assem(self):
                program = \
"""
add r2 r3 r4
add r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "02340000"
                answer += "06120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_sub_assem(self):
                program = \
"""
sub r2 r3 r4
sub r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "12340000"
                answer += "16120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_mult_assem(self):
                program = \
"""
mult r2 r3 r4
mult r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "22340000"
                answer += "26120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_div_assem(self):
                program = \
"""
div r2 r3 r4
div r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "32340000"
                answer += "36120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_and_assem(self):
                program = \
"""
and r2 r3 r4
and r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "42340000"
                answer += "46120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_or_assem(self):
                program = \
"""
or r2 r3 r4
or r6 r1 r2
"""
                output  = mach_code(program)
                answer  = "52340000"
                answer += "56120000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_zjump_assem(self):
                program = \
"""
zjump r1 r4
zjump r8 r7
"""
                output  = mach_code(program)
                answer  = "61400000"
                answer += "68700000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_gjump_assem(self):
                program = \
"""
gjump r1 r4 r11
gjump r8 r7 r3
"""
                output  = mach_code(program)
                answer  = "714b0000"
                answer += "78730000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_copy_assem(self):
                program = \
"""
copy 15       r6
copy 0x3f     r4
copy 16724940 r2
copy 0xaabbcc r4
"""
                output  = mach_code(program)
                answer  = "800000f6"
                answer += "800003f4"
                answer += "8ff33cc2"
                answer += "8aabbcc4"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_load_assem(self):
                program = \
"""
load r2 r3
load r6 r1
"""
                output  = mach_code(program)
                answer  = "92300000"
                answer += "96100000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_store_assem(self):
                program = \
"""
store r2 r3
store r6 r1
"""
                output  = mach_code(program)
                answer  = "a2300000"
                answer += "a6100000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_stop_assem(self):
                program = \
"""
stop
stop
"""
                output  = mach_code(program)
                answer  = "b0000000"
                answer += "b0000000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_comments_assem(self):
                program = \
"""
# This is comment #1.
add r2 r3 r4
# This is comment #2.
# This is comment #3.
copy 16724940 r2
# This is comment #4.

"""
                output  = mach_code(program)
                answer  = "02340000"
                answer += "8ff33cc2"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_labels_assem(self):
                program = \
"""
# This comment and blank lines should not affect labels.

         add r2 r3 r4
         add r6 r1 r2

label_1: sub r2 r3 r4
         add r2 r3 r4


         add r6 r1 r2
         copy label_1 r6
label_2: zjump r1 r2
         label_2
         stop
"""
                output  = mach_code(program)
                answer  = "02340000"
                answer += "06120000"
                answer += "12340000"
                answer += "02340000"
                answer += "06120000"
                answer += "80000086"
                answer += "61200000"
                answer += "00000018"
                answer += "b0000000"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

        def test_data_assem(self):
                program = \
"""
         # This is a comment.
         add r2 r3 r4
         add r6 r1 r2
label_1: sub r2 r3 r4
         add r2 r3 r4
         add r6 r1 r2
         copy label_1 r6
label_2: zjump r1 r2
         label_2
         stop
         # This is another comment.
         14
         0xabcd
         # This is yet another comment.
         0xdeadbeef
         4294902051
"""
                output  = mach_code(program)
                answer  = "02340000"
                answer += "06120000"
                answer += "12340000"
                answer += "02340000"
                answer += "06120000"
                answer += "80000086"
                answer += "61200000"
                answer += "00000018"
                answer += "b0000000"
                answer += "0000000e"
                answer += "0000abcd"
                answer += "deadbeef"
                answer += "ffff0123"
                answer  = bytes.fromhex(answer)
                self.assertEqual(output, answer)

unittest.main()
