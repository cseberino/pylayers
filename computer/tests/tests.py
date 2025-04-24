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

Tests the computer.
"""

import unittest
import subprocess
import os

subprocess.call(["cp", "../computer", "comp.py"])
with open("comp.py") as f:
        comp = f.readlines()
        comp = "".join(comp[:89] + comp[89 + 4:-4])
with open("comp.py", "w") as f:
        f.write(comp)
import comp
os.remove("comp.py")

def pad_mem_str(n_lines_skip):
        offsets = range(4 * n_lines_skip, 2 ** 20, 4)

        return "\n".join([f"\t{i:#010x}: 0x00000000" for i in offsets]) + "\n"

def pad_mem_bin(bytearray_):
        return bytearray_ + bytearray((2 ** 20 - len(bytearray_)) * b"\x00")

def final_comp_state(asm):
        with open("__asm__", "w") as f:
                f.write(asm)
        mach_code = subprocess.check_output(["../../asm_to_mach/asm_to_mach",
                                             "__asm__"])
        os.remove("__asm__")
        with open("__memory__", "wb") as f:
                f.write(mach_code)
        final_comp_state_ = subprocess.check_output(["../computer",
                                                     "__memory__"])
        os.remove("__memory__")

        return final_comp_state_.decode()

class Tester(unittest.TestCase):
        def test_reg_args(self):
                output = comp.reg_args(bytes.fromhex("abcdef78"))
                answer = (11, 12, 13)
                self.assertEqual(output, answer)

                output = comp.reg_args(bytes.fromhex("a83fef78"))
                answer = (8, 3, 15)
                self.assertEqual(output, answer)

        def test_add(self):
                comp.regs  = list(range(10, 26))
                comp.add(bytes.fromhex("095f0000"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 19 + 15
                self.assertEqual(output, answer)

        def test_sub(self):
                comp.regs  = list(range(10, 26))
                comp.sub(bytes.fromhex("095f0000"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 19 - 15
                self.assertEqual(output, answer)

        def test_mul(self):
                comp.regs  = list(range(10, 26))
                comp.mul(bytes.fromhex("095f0000"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 19 * 15
                self.assertEqual(output, answer)

        def test_div(self):
                comp.regs    = list(range(10, 26))
                comp.div(bytes.fromhex("095f0000"), comp.regs, None)
                output       = comp.regs
                answer       = list(range(10, 26))
                answer[15]   = int(19 / 15)
                self.assertEqual(output, answer)

                comp.regs    = 16 * [1]
                comp.regs[9] = 234
                comp.regs[5] = 0
                comp.div(bytes.fromhex("095f0000"), comp.regs, None)
                output       = comp.regs
                answer       = 16 * [1]
                answer[9]    = 234
                answer[5]    = 0
                answer[15]   = 0
                self.assertEqual(output, answer)

        def test_and(self):
                comp.regs  = list(range(10, 26))
                comp.and_(bytes.fromhex("095f0000"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 19 & 15
                self.assertEqual(output, answer)

        def test_or(self):
                comp.regs  = list(range(10, 26))
                comp.or_(bytes.fromhex("095f0000"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 19 | 15
                self.assertEqual(output, answer)

        def test_zjump(self):
                comp.regs    = list(range(11, 27))
                comp.regs[4] = 9999
                comp.zjump(bytes.fromhex("04300000"), comp.regs, None)
                output       = comp.regs
                answer       = list(range(11, 27))
                answer[4]    = 9999
                self.assertEqual(output, answer)

                comp.regs    = list(range(11, 27))
                comp.regs[4] = 0
                comp.zjump(bytes.fromhex("04300000"), comp.regs, None)
                output       = comp.regs
                answer       = list(range(11, 27))
                answer[4]    = 0
                answer[0]    = 10
                self.assertEqual(output, answer)

        def test_gjump(self):
                comp.regs    = list(range(11, 27))
                comp.regs[4] = 9999
                comp.gjump(bytes.fromhex("03450000"), comp.regs, None)
                output       = comp.regs
                answer       = list(range(11, 27))
                answer[4]    = 9999
                self.assertEqual(output, answer)

                comp.regs    = list(range(11, 27))
                comp.regs[4] = 0
                comp.gjump(bytes.fromhex("03450000"), comp.regs, None)
                output       = comp.regs
                answer       = list(range(11, 27))
                answer[4]    = 0
                answer[0]    = 12
                self.assertEqual(output, answer)

        def test_copy(self):
                comp.regs  = list(range(10, 26))
                comp.copy(bytes.fromhex("deadbeef"), comp.regs, None)
                output     = comp.regs
                answer     = list(range(10, 26))
                answer[15] = 0xeadbee
                self.assertEqual(output, answer)

        def test_load(self):
                comp.memory = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs   = list(range(1, 17))
                comp.load(bytes.fromhex("01300000"), comp.regs, comp.memory)
                output      = comp.regs, comp.memory
                answer      = list(range(1, 17))
                answer[3]   = 0xccddeeff
                answer      = (answer,
                    pad_mem_bin(bytes.fromhex("aabbccddeeff")))
                self.assertEqual(output, answer)

                comp.memory = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs   = list(range(1, 17))
                comp.load(bytes.fromhex("03900000"), comp.regs, comp.memory)
                output      = comp.regs, comp.memory
                answer      = list(range(1, 17))
                answer[9]   = 0xeeff0000
                answer      = (answer,
                    pad_mem_bin(bytes.fromhex("aabbccddeeff0000")))
                self.assertEqual(output, answer)

                comp.memory = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs   = list(range(1, 17))
                comp.load(bytes.fromhex("06900000"), comp.regs, comp.memory)
                output      = comp.regs, comp.memory
                answer      = list(range(1, 17))
                answer[9]   = 0x00000000
                answer      = (answer,
                    pad_mem_bin(bytes.fromhex("aabbccddeeff0000000000")))
                self.assertEqual(output, answer)

        def test_store(self):
                comp.memory   = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs     = list(range(1, 17))
                comp.regs[11] = 0xdeadbeef
                comp.store(bytes.fromhex("0b100000"), comp.regs, comp.memory)
                output        = comp.regs, comp.memory
                answer        = list(range(1, 17))
                answer[11]    = 0xdeadbeef
                answer        = (answer,
                    pad_mem_bin(bytes.fromhex("aabbdeadbeef")))
                self.assertEqual(output, answer)

                comp.memory   = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs     = list(range(1, 17))
                comp.regs[11] = 0xdeadbeef
                comp.store(bytes.fromhex("0b300000"), comp.regs, comp.memory)
                output        = comp.regs, comp.memory
                answer        = list(range(1, 17))
                answer[11]    = 0xdeadbeef
                answer        = (answer,
                    pad_mem_bin(bytes.fromhex("aabbccdddeadbeef")))
                self.assertEqual(output, answer)

                comp.memory   = pad_mem_bin(bytearray.fromhex("aabbccddeeff"))
                comp.regs     = list(range(1, 17))
                comp.regs[11] = 0xdeadbeef
                comp.store(bytes.fromhex("0b600000"), comp.regs, comp.memory)
                output        = comp.regs, comp.memory
                answer        = list(range(1, 17))
                answer[11]    = 0xdeadbeef
                answer        = (answer,
                    pad_mem_bin(bytes.fromhex("aabbccddeeff00deadbeef")))
                self.assertEqual(output, answer)

        def test_stop(self):
                comp.regs = list(range(1, 17))
                comp.stop(bytes.fromhex("0b100000"), comp.regs, None)
                output    = comp.regs
                answer    = list(range(1, 17))
                self.assertEqual(output, answer)

        def test_lots_1(self):
                asm    = \
"""
copy 0x8      r1
copy 0x9      r2
copy 0xaabbcc r10
add  r1 r2 r3
stop
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x00000014
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00000000
	05: 0x00000000
	06: 0x00000000
	07: 0x00000000
	08: 0x00000000
	09: 0x00000000
	10: 0x00aabbcc
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8aabbcca
	0x0000000c: 0x01230000
	0x00000010: 0xb0000000
""".lstrip()
                answer = answer + pad_mem_str(5)
                self.assertEqual(output, answer)

        def test_lots_2(self):
                asm    = \
"""
copy 0x8      r1
copy 0x9      r2
copy 0xaabbcc r10
add  r1  r2 r3
sub  r10 r1 r4
stop
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x00000018
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00aabbc4
	05: 0x00000000
	06: 0x00000000
	07: 0x00000000
	08: 0x00000000
	09: 0x00000000
	10: 0x00aabbcc
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8aabbcca
	0x0000000c: 0x01230000
	0x00000010: 0x1a140000
	0x00000014: 0xb0000000
""".lstrip()
                answer = answer + pad_mem_str(6)
                self.assertEqual(output, answer)

        def test_lots_3(self):
                asm    = \
"""
copy 0x8      r1
copy 0x9      r2
copy 0xaabbcc r10
add  r1  r2 r3
sub  r10 r1 r4
and  r10 r2 r5
or   r10 r2 r6
stop
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x00000020
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00aabbc4
	05: 0x00000008
	06: 0x00aabbcd
	07: 0x00000000
	08: 0x00000000
	09: 0x00000000
	10: 0x00aabbcc
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8aabbcca
	0x0000000c: 0x01230000
	0x00000010: 0x1a140000
	0x00000014: 0x4a250000
	0x00000018: 0x5a260000
	0x0000001c: 0xb0000000
""".lstrip()
                answer = answer + pad_mem_str(8)
                self.assertEqual(output, answer)

        def test_lots_4(self):
                asm    = \
"""
      copy 0x8      r1
      copy 0x9      r2
      copy 0xaabbcc r10
      add  r1  r2 r3
      sub  r10 r1 r4
      and  r10 r2 r5
      or   r10 r2 r6
      copy data r7
      load r7   r8
      stop
data: 0xdeadbeef
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x00000028
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00aabbc4
	05: 0x00000008
	06: 0x00aabbcd
	07: 0x00000028
	08: 0xdeadbeef
	09: 0x00000000
	10: 0x00aabbcc
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8aabbcca
	0x0000000c: 0x01230000
	0x00000010: 0x1a140000
	0x00000014: 0x4a250000
	0x00000018: 0x5a260000
	0x0000001c: 0x80000287
	0x00000020: 0x97800000
	0x00000024: 0xb0000000
	0x00000028: 0xdeadbeef
""".lstrip()
                answer = answer + pad_mem_str(11)
                self.assertEqual(output, answer)

        def test_lots_5(self):
                asm    = \
"""
      copy  0x8      r1
      copy  0x9      r2
      copy  0xaabbcc r10
      add   r1  r2 r3
      sub   r10 r1 r4
      and   r10 r2 r5
      or    r10 r2 r6
      copy  data r7
      load  r7   r8
      store r8   r2
      stop
data: 0xdeadbeef
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x0000002c
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00aabbc4
	05: 0x00000008
	06: 0x00aabbcd
	07: 0x0000002c
	08: 0xdeadbeef
	09: 0x00000000
	10: 0x00aabbcc
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8adeadbe
	0x0000000c: 0xef230000
	0x00000010: 0x1a140000
	0x00000014: 0x4a250000
	0x00000018: 0x5a260000
	0x0000001c: 0x800002c7
	0x00000020: 0x97800000
	0x00000024: 0xa8200000
	0x00000028: 0xb0000000
	0x0000002c: 0xdeadbeef
""".lstrip()
                answer = answer + pad_mem_str(12)
                self.assertEqual(output, answer)

        def test_lots_6(self):
                asm    = \
"""
      copy  0xabc r1
      copy  0xdef r2
      copy      0 r3
      copy     bb r4
      zjump    r3 r4
aa:   copy  0x87c r5
bb:   copy  0xb31 r6
      stop
"""
                output = final_comp_state(asm)
                output = output[:output.find("memory")].strip()
                answer = \
"""
registers:

	00: 0x00000020
	01: 0x00000abc
	02: 0x00000def
	03: 0x00000000
	04: 0x00000018
	05: 0x00000000
	06: 0x00000b31
	07: 0x00000000
	08: 0x00000000
	09: 0x00000000
	10: 0x00000000
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000
""".strip()
                self.assertEqual(output, answer)

        def test_lots_7(self):
                asm    = \
"""
      copy  0xabc r1
      copy  0xdef r2
      copy   0xab r3
      copy     bb r4
      zjump    r3 r4
aa:   copy  0x87c r5
bb:   copy  0xb31 r6
      stop
"""
                output = final_comp_state(asm)
                output = output[:output.find("memory")].strip()
                answer = \
"""
registers:

	00: 0x00000020
	01: 0x00000abc
	02: 0x00000def
	03: 0x000000ab
	04: 0x00000018
	05: 0x0000087c
	06: 0x00000b31
	07: 0x00000000
	08: 0x00000000
	09: 0x00000000
	10: 0x00000000
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000
""".strip()
                self.assertEqual(output, answer)

        def test_lots_8(self):
                asm    = \
"""
      copy  0x8      r1
      copy  0x9      r2
      copy  0xaabbcc r10
      add   r1  r2 r3
      sub   r10 r1 r4
      mul   r1  r2 r5
      div   r4  r3 r6
      and   r6  r4 r7
      or    r7  r1 r8
      copy  data r9
      load  r9   r10
      add   r9   r2  r9
      store r10  r9
      stop
data: 0xdeadbeef
"""
                output = final_comp_state(asm)
                answer = \
"""
registers:

	00: 0x00000038
	01: 0x00000008
	02: 0x00000009
	03: 0x00000011
	04: 0x00aabbc4
	05: 0x00000048
	06: 0x000a0b0b
	07: 0x000a0b00
	08: 0x000a0b08
	09: 0x00000041
	10: 0xdeadbeef
	11: 0x00000000
	12: 0x00000000
	13: 0x00000000
	14: 0x00000000
	15: 0x00000000

memory:

	0x00000000: 0x80000081
	0x00000004: 0x80000092
	0x00000008: 0x8aabbcca
	0x0000000c: 0x01230000
	0x00000010: 0x1a140000
	0x00000014: 0x21250000
	0x00000018: 0x34360000
	0x0000001c: 0x46470000
	0x00000020: 0x57180000
	0x00000024: 0x80000389
	0x00000028: 0x99a00000
	0x0000002c: 0x09290000
	0x00000030: 0xaa900000
	0x00000034: 0xb0000000
	0x00000038: 0xdeadbeef
	0x0000003c: 0x00000000
	0x00000040: 0x00deadbe
	0x00000044: 0xef000000
""".lstrip()
                answer = answer + pad_mem_str(18)
                self.assertEqual(output, answer)

        def test_func_calls(self):
                asm    = \
"""
# ------------------------------------------------------------------------------
# initial steps
# ------------------------------------------------------------------------------

# Sets r13 to zero for zjump instructions.
# Sets r14 to the address of f.

        copy  0x0  r13
        copy    f  r14

# Load word beginning at db, doubles it and stores in r10.

        copy  db   r10
        load  r10  r10
        add   r10  r10  r10

# Stores results in r10 at dbx2 using r11.

        copy  dbx2 r11
        store r10  r11

# ------------------------------------------------------------------------------
# first calculation
# ------------------------------------------------------------------------------

# Sets r1, r2, r3, r4 and r5 to be used as the arguments of f.
# Sets r15 to the return value.
# Invokes f.

c_1_b:  copy  0x1   r1
        copy  0x2   r2
        copy  0x3   r3
        copy  0x4   r4
        copy  0x5   r5
        copy  c_1_e r15
        zjump r13   r14

# Stores the result from r6 at ans_1 using r7.

c_1_e:  copy  ans_1 r7
        store r6    r7

# ------------------------------------------------------------------------------
# second calculation
# ------------------------------------------------------------------------------

# Sets r1, r2, r3, r4 and r5 to be used as the arguments of f.
# Sets r15 to the return value.
# Invokes f.

c_2_b:  copy  0xabcd r1
        copy  0x4a8d r2
        copy  0x9a7e r3
        copy  0xab23 r4
        copy  0xbb33 r5
        copy  c_2_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_1 using r7.

c_2_e:  copy  ans_2 r7
        store r6    r7

# ------------------------------------------------------------------------------
# third calculation
# ------------------------------------------------------------------------------

# Sets r1, r2, r3, r4 and r5 to be used as the arguments of f.
# Sets r15 to the return value.
# Invokes f.

c_3_b:  copy  0x1f  r1
        copy  0x2f  r2
        copy  0x3f  r3
        copy  0x4f  r4
        copy  0x5f  r5
        copy  c_3_e r15
        zjump r13   r14

# Stores the result from r6 at ans_1 using r7.

c_3_e:  copy  ans_3 r7
        store r6    r7

# ------------------------------------------------------------------------------
# fourth calculation
# ------------------------------------------------------------------------------

# Sets r1, r2, r3, r4 and r5 to be used as the arguments of f.
# Sets r15 to the return value.
# Invokes f.

c_4_b:  copy  0x1ab r1
        copy  0x2bc r2
        copy  0x3cd r3
        copy  0x4de r4
        copy  0x5ef r5
        copy  c_4_e r15
        zjump r13   r14

# Stores the result from r6 at ans_1 using r7.

c_4_e:  copy  ans_4 r7
        store r6    r7

# ------------------------------------------------------------------------------
# Stop
# ------------------------------------------------------------------------------

        stop

# ------------------------------------------------------------------------------
# function definition
# ------------------------------------------------------------------------------

# f(a, b, c, d, e) = [(a + b - c) & d] | e

f:      add   r1  r2   r6
        sub   r6  r3   r6
        and   r6  r4   r6
        or    r6  r5   r6
        zjump r13 r15

# ------------------------------------------------------------------------------
# storage
# ------------------------------------------------------------------------------

ans_1:  0x0
ans_2:  0x0
ans_3:  0x0
ans_4:  0x0
db:     0xdeadbeef
dbx2:   0x0
"""
                output = final_comp_state(asm)
                output = output[output.find("	0x000000c4:") - 1:]
                output = output[:output.find("	0x000000dc:")]
                answer = \
"""
	0x000000c4: 0x00000005
	0x000000c8: 0x0000bb33
	0x000000cc: 0x0000005f
	0x000000d0: 0x000005ff
	0x000000d4: 0xdeadbeef
	0x000000d8: 0xbd5b7dde
"""
                self.assertEqual(output, answer)

        def test_gt(self):
                asm    = \
"""
# This is a partial implementation of the greater than function.
# a > b is found, for some cases only, from the most significant bit of b - a.

# ------------------------------------------------------------------------------
# initial steps
# ------------------------------------------------------------------------------

# Sets r11 to the word length in bytes.
# Sets r12 to the value used to determine the most significant bits.
# Sets r13 to zero so zjump instructions will always jump.
# Sets r14 to the address of gt.

        copy  word r11
        load  r11  r11
        copy  mask r12
        load  r12  r12
        copy  0x0  r13
        copy  gt   r14

# ------------------------------------------------------------------------------
# c_1
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_1_b:  copy  args_1 r1
        load  r1     r1
        copy  args_1 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_1_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_1 using r7.

c_1_e:  copy  ans_1 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_2
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_2_b:  copy  args_2 r1
        load  r1     r1
        copy  args_2 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_2_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_2 using r7.

c_2_e:  copy  ans_2 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_3
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_3_b:  copy  args_3 r1
        load  r1     r1
        copy  args_3 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_3_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_3 using r7.

c_3_e:  copy  ans_3 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_4
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_4_b:  copy  args_4 r1
        load  r1     r1
        copy  args_4 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_4_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_4 using r7.

c_4_e:  copy  ans_4 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_5
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_5_b:  copy  args_5 r1
        load  r1     r1
        copy  args_5 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_5_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_5 using r7.

c_5_e:  copy  ans_5 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_6
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_6_b:  copy  args_6 r1
        load  r1     r1
        copy  args_6 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_6_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_6 using r7.

c_6_e:  copy  ans_6 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_7
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_7_b:  copy  args_7 r1
        load  r1     r1
        copy  args_7 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_7_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_7 using r7.

c_7_e:  copy  ans_7 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_8
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_8_b:  copy  args_8 r1
        load  r1     r1
        copy  args_8 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_8_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_8 using r7.

c_8_e:  copy  ans_8 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_9
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_9_b:  copy  args_9 r1
        load  r1     r1
        copy  args_9 r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_9_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_9 using r7.

c_9_e:  copy  ans_9 r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_a
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_a_b:  copy  args_a r1
        load  r1     r1
        copy  args_a r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_a_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_a using r7.

c_a_e:  copy  ans_a r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_b
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_b_b:  copy  args_b r1
        load  r1     r1
        copy  args_b r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_b_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_b using r7.

c_b_e:  copy  ans_b r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_c
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_c_b:  copy  args_c r1
        load  r1     r1
        copy  args_c r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_c_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_c using r7.

c_c_e:  copy  ans_c r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_d
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_d_b:  copy  args_d r1
        load  r1     r1
        copy  args_d r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_d_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_d using r7.

c_d_e:  copy  ans_d r7
        store r6    r7

# ------------------------------------------------------------------------------
# c_e
# ------------------------------------------------------------------------------

# Sets r1 and r2 to be used as the arguments of gt.
# Sets r15 to the return value.
# Invokes gt.

c_e_b:  copy  args_e r1
        load  r1     r1
        copy  args_e r2
        add   r11    r2  r2
        load  r2     r2
        copy  c_e_e  r15
        zjump r13    r14

# Stores the result from r6 at ans_e using r7.

c_e_e:  copy  ans_e r7
        store r6    r7

# ------------------------------------------------------------------------------
# Stop
# ------------------------------------------------------------------------------

        stop

# ------------------------------------------------------------------------------
# function definition
# ------------------------------------------------------------------------------

# gt(a, b) = 1 if a > b else 0

gt:     sub   r2     r1 r3
        and   r12    r3 r3
        copy  gt_ret    r4
        copy  gt_no     r5
        zjump r3        r5
gt_yes: copy  0x1       r6
        zjump r13       r4
gt_no:  copy  0x0       r6
gt_ret: zjump r13       r15

# ------------------------------------------------------------------------------
# storage
# ------------------------------------------------------------------------------

word:   0x0000004
mask:   0x8000000
args_1: 0xaaaaaaa
        0xf000000
args_2: 0xaaaaaaa
        0x1000000
args_3: 0xaaaaaaa
        0x0000006
args_4: 0xaaaaaaa
        0x8000000
args_5: 0xaaaaaaa
        0x0000000
args_6: 0xaaaaaaa
        0xfffffff
args_7: 0xaaaaaaa
        0x7ffffff
args_8: 0x000cccc
        0xf000000
args_9: 0x000cccc
        0x1000000
args_a: 0x000cccc
        0x0000006
args_b: 0x000cccc
        0x8000000
args_c: 0x000cccc
        0x0000000
args_d: 0x000cccc
        0xfffffff
args_e: 0x000cccc
        0x7ffffff

# 32 set bits denotes the beginning of the answers.

        0xffffffff

ans_1:  0x0
ans_2:  0x0
ans_3:  0x0
ans_4:  0x0
ans_5:  0x0
ans_6:  0x0
ans_7:  0x0
ans_8:  0x0
ans_9:  0x0
ans_a:  0x0
ans_b:  0x0
ans_c:  0x0
ans_d:  0x0
ans_e:  0x0

"""
                output = final_comp_state(asm)
                output = output[output.find("	0x000002b4:") - 1:]
                output = output[:output.find("	0x000002ec:")]
                answer = \
"""
	0x000002b4: 0x00000000
	0x000002b8: 0x00000000
	0x000002bc: 0x00000000
	0x000002c0: 0x00000001
	0x000002c4: 0x00000000
	0x000002c8: 0x00000000
	0x000002cc: 0x00000001
	0x000002d0: 0x00000001
	0x000002d4: 0x00000000
	0x000002d8: 0x00000001
	0x000002dc: 0x00000000
	0x000002e0: 0x00000001
	0x000002e4: 0x00000001
	0x000002e8: 0x00000000
"""
                self.assertEqual(output, answer)

unittest.main()
