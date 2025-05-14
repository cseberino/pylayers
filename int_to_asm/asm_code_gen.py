import eval_
import interpreter
import env_

BOOLEAN   = 1 << 28
INTEGER   = 2 << 28
STRING    = 3 << 28
VARIABLE  = 4 << 28
LIST      = 5 << 28
WORD_SIZE = 4

def encode_exp(exp):
        def hex_line(e):
                if isinstance(e, str):
                        hex_line_ = ""
                        for i in range(0, len(e), WORD_SIZE):
                                word       = e[i: i + WORD_SIZE].encode().hex()
                                hex_line_ += f"\t0x{word:0>8}\n"
                else:
                        hex_line_ = f"\t0x{hex(e)[2:]:0>8}\n"

                return hex_line_

        if   isinstance(exp, bool):
                exp_ = hex_line(BOOLEAN + exp)
        elif isinstance(exp, int):
                exp_ = hex_line(INTEGER)                + hex_line(exp)
        elif isinstance(exp, str):
                exp_ = hex_line(STRING   + len(exp))    + hex_line(exp)
        elif isinstance(exp, tuple):
                exp_ = hex_line(VARIABLE + len(exp[0])) + hex_line(exp[0])
        elif isinstance(exp, list):
                exp_ = "".join([encode_exp(e) for e in exp])
                exp_ = hex_line(LIST + len(exp_.split("\n"))) + exp_

        return exp_

def asm_code_gen(int_code):
        asm_code  = eval_.EVAL
        for e in interpreter.parser(interpreter.tokenizer(int_code)):
                asm_code += encode_exp(e)
        asm_code += env_.ENV

        return asm_code
