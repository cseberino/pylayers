import exps
import header
import env
import footer
import math

BOOLEAN   = 1 << 28
INTEGER   = 2 << 28
STRING    = 3 << 28
VARIABLE  = 4 << 28
LIST      = 5 << 28
WORD_SIZE = 4

def len_encoded(exp):
        if   isinstance(exp, bool):
                len_ = WORD_SIZE + WORD_SIZE
        elif isinstance(exp, int):
                len_ = WORD_SIZE + WORD_SIZE
        elif isinstance(exp, str):
                len_ = WORD_SIZE + len(exp)
        elif isinstance(exp, tuple):
                len_ = WORD_SIZE + len(exp[0])
        elif isinstance(exp, list):
                len_ = [len_encoded(e) for e in exp]
                len_ = [WORD_SIZE * math.ceil(e / WORD_SIZE) for e in len_]
                len_ = WORD_SIZE + sum(len_)

        return len_

def encode_exp(exp):
        def asm_lines(e):
                if isinstance(e, str):
                        asm_lines_ = ""
                        for i in range(0, len(e), WORD_SIZE):
                                word        = e[i: i + WORD_SIZE].encode().hex()
                                asm_lines_ += f"\t0x{word:0<8}\n"
                else:
                        asm_lines_ = f"\t0x{hex(e)[2:]:0>8}\n"

                return asm_lines_

        if   isinstance(exp, bool):
                header = BOOLEAN  + len_encoded(exp)
                exp_   = asm_lines(header) + asm_lines(exp)
        elif isinstance(exp, int):
                header = INTEGER  + len_encoded(exp)
                exp_   = asm_lines(header) + asm_lines(exp)
        elif isinstance(exp, str):
                header = STRING   + len_encoded(exp)
                exp_   = asm_lines(header) + asm_lines(exp)
        elif isinstance(exp, tuple):
                header = VARIABLE + len_encoded(exp)
                exp_   = asm_lines(header) + asm_lines(exp[0])
        elif isinstance(exp, list):
                header = LIST     + len_encoded(exp)
                exp_   = "".join([encode_exp(e) for e in exp])
                exp_   = asm_lines(header) + exp_

        return exp_

def asm_code_gen(int_code):
        asm_code  = header.HEADER
        asm_code += "first_exp: "
        for e in exps.exps(int_code):
                asm_code += encode_exp(e)
        asm_code += "\t0x00000000\n"
        asm_code += env.ENV
        asm_code += footer.FOOTER

        return asm_code
