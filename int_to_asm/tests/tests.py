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

Tests the asdfasdf
"""

import sys
sys.path.append("..")

import asm_code_gen
import unittest
import subprocess
import os

def asm_code(program):
        with open("__program__", "w") as f:
                f.write(program)
        asm_code_ = subprocess.check_output(["../int_to_asm", "__program__"])
        asm_code_ = asm_code_.decode()
        os.remove("__program__")

        return asm_code_

class Tester(unittest.TestCase):
        def test_encode_exp(self):
                output  = asm_code_gen.encode_exp(True)
                answer  = "\t0x10000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(False)
                answer  = "\t0x10000008\n"
                answer += "\t0x00000000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(0)
                answer  = "\t0x20000008\n"
                answer += "\t0x00000000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(1)
                answer  = "\t0x20000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(0xbeef)
                answer  = "\t0x20000008\n"
                answer += "\t0x0000beef\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(2 ** 32 - 1)
                answer  = "\t0x20000008\n"
                answer += "\t0xffffffff\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp("a")
                answer  = "\t0x30000005\n"
                answer += "\t0x61000000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp("hello")
                answer  = "\t0x30000009\n"
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                self.assertEqual(output, answer)

                string_ = "515The quick brown fox jumps over the lazy dogs!@#@"
                output  = asm_code_gen.encode_exp(string_)
                answer  = "\t0x30000037\n"
                answer += "\t0x35313554\n"
                answer += "\t0x68652071\n"
                answer += "\t0x7569636b\n"
                answer += "\t0x2062726f\n"
                answer += "\t0x776e2066\n"
                answer += "\t0x6f78206a\n"
                answer += "\t0x756d7073\n"
                answer += "\t0x206f7665\n"
                answer += "\t0x72207468\n"
                answer += "\t0x65206c61\n"
                answer += "\t0x7a792064\n"
                answer += "\t0x6f677321\n"
                answer += "\t0x40234000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(("a",))
                answer  = "\t0x40000005\n"
                answer += "\t0x61000000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp(("hello",))
                answer  = "\t0x40000009\n"
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                self.assertEqual(output, answer)

                var     = "515The quick brown fox jumps over the lazy dogs!@#@"
                var     = (var,)
                output  = asm_code_gen.encode_exp(var)
                answer  = "\t0x40000037\n"
                answer += "\t0x35313554\n"
                answer += "\t0x68652071\n"
                answer += "\t0x7569636b\n"
                answer += "\t0x2062726f\n"
                answer += "\t0x776e2066\n"
                answer += "\t0x6f78206a\n"
                answer += "\t0x756d7073\n"
                answer += "\t0x206f7665\n"
                answer += "\t0x72207468\n"
                answer += "\t0x65206c61\n"
                answer += "\t0x7a792064\n"
                answer += "\t0x6f677321\n"
                answer += "\t0x40234000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp([])
                answer  = "\t0x50000004\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp([True])
                answer  = "\t0x5000000c\n"
                answer += "\t0x10000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

                list_   = [True, 0xbeef, "hello", ("hello",)]
                output  = asm_code_gen.encode_exp(list_)
                answer  = "\t0x5000002c\n"
                answer += "\t0x10000008\n" # True    (8 bytes)
                answer += "\t0x00000001\n"
                answer += "\t0x20000008\n" # 0xbeef  (8 bytes)
                answer += "\t0x0000beef\n"
                answer += "\t0x30000009\n" # "hello" (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                answer += "\t0x40000009\n" # hello   (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                self.assertEqual(output, answer)

                list_   = 2 * [True, 0xbeef, "hello", ("hello",)]
                output  = asm_code_gen.encode_exp(list_)
                answer  = "\t0x50000054\n"
                answer += "\t0x10000008\n" # True    (8 bytes)
                answer += "\t0x00000001\n"
                answer += "\t0x20000008\n" # 0xbeef  (8 bytes)
                answer += "\t0x0000beef\n"
                answer += "\t0x30000009\n" # "hello" (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                answer += "\t0x40000009\n" # hello   (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                answer += "\t0x10000008\n" # True    (8 bytes)
                answer += "\t0x00000001\n"
                answer += "\t0x20000008\n" # 0xbeef  (8 bytes)
                answer += "\t0x0000beef\n"
                answer += "\t0x30000009\n" # "hello" (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                answer += "\t0x40000009\n" # hello   (9 bytes)
                answer += "\t0x68656c6c\n"
                answer += "\t0x6f000000\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp([[True]])
                answer  = "\t0x50000010\n"
                answer += "\t0x5000000c\n"
                answer += "\t0x10000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp([[[True]]])
                answer  = "\t0x50000014\n"
                answer += "\t0x50000010\n"
                answer += "\t0x5000000c\n"
                answer += "\t0x10000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

                output  = asm_code_gen.encode_exp([[[[[True]]]]])
                answer  = "\t0x5000001c\n"
                answer += "\t0x50000018\n"
                answer += "\t0x50000014\n"
                answer += "\t0x50000010\n"
                answer += "\t0x5000000c\n"
                answer += "\t0x10000008\n"
                answer += "\t0x00000001\n"
                self.assertEqual(output, answer)

        def test_int_exp(self):
                program = \
"""
5
"""
                output  = asm_code(program)
                with open("output", "w") as f:
                        f.write(output)

unittest.main()
