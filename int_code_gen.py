ATOMS     = ["NONE", "TRUE", "FALSE", "NATURAL", "STRING", "VARIABLE"]
FUNC_DEF  = "(def {} (func ({}) {}))"
FUNC_END  = "(if <special> <special> <None>)"
COND_WRAP = '(and {} (!= <special> "break"))'
STAT_WRAP = "(if (not <special>) {} ())"
FOR_BEG   = '(if (!= <special> "break") (def <special> ()) ())'
PROG_BEG  = """\
(def print (func (e) (list "__PRINT__" e)))

(def <None> (noeval <<None>>))

"=============================================================================="

"""

def spec_def(val):
        return f"(def <special> {val})"

def list_(*args):
        return "({})".format(" ".join(args))

def block_(ast_):
        stats = " ".join([STAT_WRAP.format(program_(e)) for e in ast_[1:-1]])

        return list_("block", stats)

def program_(ast_):
        func = ast_[0]
        if func.startswith("exp"):
                if   func in ["exp_log_not", "exp_pdbn"]:
                        func = "exp_unary_op"
                elif func not in globals():
                        func = "exp_binary_op"

        return globals()[func](ast_[1:])

def program(ast):
        return PROG_BEG + "\n\n".join([program_(e) for e in ast[1:]])

def statement(ast_):
        return program_(ast_[0])

def stat_semicol(ast_):
        return " ".join([program_(e) for e in ast_[::2]])

def stat_if(ast_):
        cond  = program_(ast_[1])
        block = program_(ast_[4])
        else_ = program_(ast_[-1]) if ast_[-4][0] == "ELSE" else "()"
        index = len(ast_) - 9 if ast_[-4][0] == "ELSE" else len(ast_) - 5
        while (index > 4) and (ast_[index][0] == "ELIF"):
                cond_   = program_(ast_[index + 1])
                block_  = program_(ast_[index + 4])
                else_   = list_("if", cond_, block_, else_)
                index  -= 5

        return list_("if", cond, block, else_)

def stat_loop(ast_):
        if ast_[0][0] == "WHILE":
                cond   = COND_WRAP.format(program_(ast_[1]))
                block  = block_(ast_[4][1:])[len("(block "):-1]
                block  = list_("block", spec_def("()"), block)
                result = spec_def("()") + " " + list_("while", cond, block)
        else:
                var    = ast_[1][1]
                list__ = program_(ast_[3])
                block  = block_(ast_[6][1:])[len("(block "):-1]
                block  = list_("block", FOR_BEG, block)
                result = spec_def("()") + " " + list_("for", var, list__, block)

        return result

def stat_func(ast_):
        params = " ".join([e[1] for e in ast_[3:-4] if e[0] == "VARIABLE"])
        block  = block_(ast_[-1][1:])[len("(block "):-1]
        block  = list_("block", spec_def("()"), block, FUNC_END)

        return FUNC_DEF.format(ast_[1][1], params, block)

def semicol_base(ast_):
        if   ast_[0][0] in ["CONTINUE", "BREAK"]:
                result = spec_def('"' + ast_[0][0].lower() + '"')
        elif ast_[0][0] == "RETURN":
                val    = program_(ast_[1]) if len(ast_) > 1 else "<None>"
                result = spec_def(val)
        else:
                result = program_(ast_[0])
                if len(ast_) > 1:
                        value  = program_(ast_[2])
                        if ast_[1][1][1] != "=":
                                value = list_(ast_[1][1][1][:-1], result, value)
                        result = list_("def", result, value)

        return result

def block(ast_):
        return list_("block", *[program_(e) for e in ast_[1:-1]])

def exp_unary_op(ast_):
        result = program_(ast_[-1])
        for e in reversed(ast_[:-1]):
                if e[0] != "PLUS":
                        func   = e[1] if e[1] != "-" else "negate"
                        result = list_(func, result)

        return result

def exp_binary_op(ast_):
        result = program_(ast_[0])
        for i, e in enumerate([program_(e) for e in ast_[2::2]]):
                if ast_[1][0] == "comp_op":
                        func = ast_[2 * i + 1][1][1]
                        if func == "==":
                                func = "="
                else:
                        func = ast_[2 * i + 1][1]
                        if   func == "**":
                                func = "^"
                        elif func == "^":
                                func = "^^"
                result = list_(func, result, e)

        return result

def exp_inv_elems(ast_):
        result = program_(ast_[0])
        index  = 1
        while index < len(ast_):
                if   ast_[index][0] == "L_PAREN":
                        end     = index + ast_[index:].index(("R_PAREN", ")"))
                        args    = [program_(e) for e in ast_[index + 1:end:2]]
                        result  = list_(result, *args)
                        index   = end + 1
                else:
                        elems   = program_(ast_[index + 1])
                        if "COLON" in [e[0] for e in ast_[index + 1][1:]]:
                                result = list_("slice", result, elems)
                        else:
                                result = list_("index", result, elems)
                        index  += 3

        return result

def exp_base(ast_):
        if   ast_[0][0] in ATOMS:
                result = ast_[0][1] if ast_[0][0] != "NONE" else "<None>"
        elif ast_[0][0] == "L_PAREN":
                result = program_(ast_[1])
        elif ast_[0][0] == "L_BRACK":
                elems  = [program_(e) for e in ast_ if e[0] == "expression"]
                result = list_("list", *elems)

        return result

def elements(ast_):
        if "COLON" not in [e[0] for e in ast_]:
                result = program_(ast_[0])
        else:
                if   len(ast_) == 1:
                        result  = "0 ()"
                elif len(ast_) == 2:
                        if ast_[0][0] == "COLON":
                                result = "0 " + program_(ast_[1])
                        else:
                                result = program_(ast_[0]) + " ()"
                else:
                        result = program_(ast_[0]) + " " + program_(ast_[2])

        return result

def int_code_gen(ast):
        return program(ast)
