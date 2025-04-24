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

Converts assembly code into machine code.  Assembly code has one instruction or
datum per line.  Each assembly code line will be converted to 32 bits.  All bits
are either zero or one.  Four bits are referred to as a nibble.  Eight bits are
referred to as a byte.  On the computer, 32 bits is referred to as a word.
Different computers may have different word sizes.  Assembly code lines can have
labels.  Both assembly code and machine code instructions are composed of
commands and their arguments.  Command arguments can be data and computer
registers.  Computer registers store data.  Hexadecimal is a compact
representation of bits composed of digits and the letters a through f.  Each
character in a hexadecimal representation of data represents a nibble.  All
sizes are given in bytes.
"""

CMDS      = ["add", "sub", "mult", "div", "and", "or", "zjump", "gjump",
                                                "copy", "load", "store", "stop"]
NIBB_SIZE = 0.5
INST_SIZE = 4
HEX       = 16

def hex_(e, size):
        e = int(e, HEX) if str(e).startswith("0x") else e

        return hex(int(e))[2:].zfill(int(2 * size))

def machine_code(inst, labels):
        inst = inst.split()[1:] if ":" in inst else inst.split()
        if inst[0] in CMDS:
                cmd = hex_(CMDS.index(inst[0]), NIBB_SIZE)
                if inst[0] == "copy":
                        datum = inst[1]
                        datum = labels[datum] if datum in labels else datum
                        datum = hex_(datum,       INST_SIZE - 2 * NIBB_SIZE)
                        reg   = hex_(inst[2][1:], NIBB_SIZE)
                        inst  = cmd + datum + reg
                else:
                        regs  = [hex_(r[1:], NIBB_SIZE) for r in inst[1:]]
                        pad   = (2 * INST_SIZE - 1 - len(regs)) * "0"
                        inst  = cmd + "".join(regs) + pad
        else:
                datum = labels[inst[0]] if inst[0] in labels else inst[0]
                datum = hex_(datum, INST_SIZE)
                inst  = datum

        return inst

def assembler(asm_code):
        insts  = [e.strip() for e in asm_code.split("\n")]
        insts  = [e for e in insts if e and not e.startswith("#")]
        labels = {e : INST_SIZE * i for i, e in enumerate(insts)}
        labels = {e[:e.find(":")] : labels[e] for e in labels if ":" in e}

        return "".join([machine_code(e, labels) for e in insts])
