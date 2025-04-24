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


Contains the assembler.

Assemblers convert assembly code into machine code.  Assembly code and machine
code are composed of instructions and data.  Assembly code has one instruction
or datum per line.  Assembly code lines may also have labels.  Both assembly
code and machine code instructions are composed of commands and their arguments.
Command arguments can be computer registers or data where computer registers are
devices that store data.  Machine code is composed of bits or zeroes and ones.
Four bits are referred to as nibbles.  Eight bits are referred to as bytes.  32
bits are referred to as words but different computers may have different word
sizes.  Assembly code may use hexadecimal representations of data.  This is a
compact bit representation composed of digits and the first six letters where
each represents a different nibble.  All sizes in the assembler are given in
bytes.
"""

CMDS      = ["add", "sub", "mul", "div", "and", "or", "zjump", "gjump", "copy",
                                                        "load", "store", "stop"]
NIBB_SIZE = 0.5
WORD_SIZE = 4
HEX       = 16

def bits(datum, size):
        """
        Converts data to bit representations.

        Hexadecimal representations in assembly code are denoted with "0x".
        """

        base = HEX if str(datum).startswith("0x") else 10

        return bin(int(str(datum), base))[2:].zfill(int(8 * size))

def machine_code(line, labels):
        """
        Converts one line of assembly code into machine code.

        The machine code output has 32 bits.
        """

        line = line.split()[1:] if ":" in line else line.split()
        if line[0] in CMDS:
                cmd = bits(CMDS.index(line[0]), NIBB_SIZE)
                if line[0] == "copy":
                        datum = line[1]
                        datum = labels[datum] if datum in labels else datum
                        datum = bits(datum,       WORD_SIZE - 2 * NIBB_SIZE)
                        reg   = bits(line[2][1:], NIBB_SIZE)
                        line  = cmd + datum + reg
                else:
                        regs  = [bits(r[1:], NIBB_SIZE) for r in line[1:]]
                        pad   = (8 * WORD_SIZE - 4 - 4 * len(regs)) * "0"
                        line  = cmd + "".join(regs) + pad
        else:
                datum = labels[line[0]] if line[0] in labels else line[0]
                datum = bits(datum, WORD_SIZE)
                line  = datum

        return int(line, 2).to_bytes(WORD_SIZE, "big")

def assembler(asm_code):
        """
        Converts assembly code into machine code.

        Conversions happen one assembly code line at a time.  Line labels are
        replaced with numbers while blank and comment lines are ignored.
        """

        lines  = [e.strip() for e in asm_code.split("\n")]
        lines  = [e for e in lines if e and not e.startswith("#")]
        labels = {e : WORD_SIZE * i for i, e in enumerate(lines)}
        labels = {e[:e.find(":")] : labels[e] for e in labels if ":" in e}

        return b"".join([machine_code(e, labels) for e in lines])
