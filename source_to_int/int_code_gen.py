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


Contains the intermediate code generator.

Converts abtract syntax trees into intermediate code which is a more compact
encoding.
"""

def _exp_bin(inner_func):
        """
        helper function for binary expressions

        Returns functions converting abstract syntax trees to intermediate code.
        """

        def exp_bin(ast):
                result = globals()[inner_func](ast[1])
                index  = 2
                while index < len(ast):
                        bin_op  = ast[index][1]
                        if inner_func == "exp_bit_or":
                                bin_op = comp(ast[index])
                        arg     = globals()[inner_func](ast[index + 1])
                        result  = f"({bin_op} {result} {arg})"
                        index  += 2

                return result

        return exp_bin

for e in [("expression",  "exp_log_and"),
          ("exp_log_and", "exp_log_not"),
          ("exp_comp",    "exp_bit_or"),
          ("exp_bit_or",  "exp_bit_xor"),
          ("exp_bit_xor", "exp_bit_and"),
          ("exp_bit_and", "exp_shift"),
          ("exp_shift",   "exp_sum"),
          ("exp_sum",     "exp_prod"),
          ("exp_prod",    "exp_pdbn"),
          ("exp_pow",     "exp_iis")]:
        globals()[e[0]] = _exp_bin(e[1])

def comp(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        return ast[1][1]

def assign(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        return ast[1][1]

def exp_(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        if   len(ast[1:]) == 1:
                result = ast[1][1]
        elif ast[1][0] == "L_PAREN":
                result = f"({expression(ast[2])})"
        elif ast[1][0] == "L_BRACK":
                result = f"({' '.join([expression(e) for e in ast[2:-1:2]])})"

        return result

def exp_iis_(first, rest):
        if   rest[0][0] == "L_PAREN":
                result = " ".join([expression(e) for e in rest[1:-1:2]])
                result = f"({first} {result})"
                if result.endswith(" )"):
                        result  = f"{result[:-2]})"
        elif rest[0][0] == "L_BRACK":
                if   len(rest) == 3:
                        if rest[1] == ("COLON", ":"):
                                result = f"(slice {first} None None)"
                        else:
                                arg    = expression(rest[1])
                                result = f"(index {first} {arg})"
                elif len(rest) == 4:
                        if rest[1] == ("COLON", ":"):
                                arg    = expression(rest[2])
                                result = f"(slice {first} None {arg})"
                        else:
                                arg    = expression(rest[1])
                                result = f"(slice {first} {arg} None)"
                else:
                        arg_1  = expression(rest[1])
                        arg_2  = expression(rest[3])
                        result = f"(slice {first} {arg_1} {arg_2})"

        return result

def exp_iis(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        def find_end(ast, beg):
                for i, e in enumerate(ast[beg:]):
                        if e in [("R_PAREN", ")"), ("R_BRACK", "]")]:
                                end_ = i
                                break

                return beg + end_

        result = exp_(ast[1])
        if len(ast[1:]) > 1:
                beg    = 2
                end_   = find_end(ast, beg) + 1
                result = exp_iis_(result, ast[beg:end_])
                while end_ < len(ast):
                        beg    = end_
                        end_   = find_end(ast, beg) + 1
                        result = exp_iis_(result, ast[beg:end_])

        return result

def exp_pdbn(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        result = exp_pow(ast[-1])
        for e in reversed(ast[1:-1]):
                result = f"({e[1]} {result})"

        return result

def exp_log_not(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        result = exp_comp(ast[-1])
        for e in ast[1:-1]:
                result = f"(not {result})"

        return result

def block(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        return  f"(block {' '.join([statement(e) for e in ast[2:-1]])})"

def stat_semicol_(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        if   ast[1][0] == "CONTINUE":
                result = f"({ast[1][1]})"
        elif ast[1][0] == "BREAK":
                result = f"({ast[1][1]})"
        elif ast[1][0] == "RETURN":
                result = f"({ast[1][1]})"
                if len(ast[1:]) == 2:
                        result = f"({ast[1][1]} {expression(ast[2])})"
        else:
                result = expression(ast[1])
                if len(ast[1:]) == 3:
                        arg_2  = expression(ast[3])
                        result = f"({assign(ast[2])} {result} {arg_2})"

        return result

def stat_semicol(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        return "\n".join([stat_semicol_(e) for e in ast[1::2]])

def stat_func_def(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        name   = ast[2][1]
        params = ""
        index  = 4
        while ast[index][0] == "VARIABLE":
                params += f"{ast[index][1]} "
                index  += 2
        params = f"({params.rstrip()})"
        block_ = block(ast[-1])

        return f"(set {name} (func {params} {block_}))"

def stat_loop(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        if ast[1][0] == "FOR":
                var    = ast[2][1]
                result = f"(for {var} {expression(ast[4])} {block(ast[-1])})"
        else:
                result = f"(while {expression(ast[2])} {block(ast[-1])})"

        return result

def stat_if(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        result  = f"(if {expression(ast[2])} {block(ast[5])} "
        index   = 10
        while index < len(ast):
                cond    = expression(ast[index - 3])
                result += f"(if {cond} {block(ast[index])} "
                index  += 5
        result += block(ast[-1]) if index - 1 < len(ast) else str(None)
        result += ((len(ast) - 6) // 5 + 1) * ")"

        return result

def statement(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        if   ast[1][1][0] == "IF":
                result = stat_if(ast[1])
        elif ast[1][1][0] in ("FOR", "WHILE"):
                result = stat_loop(ast[1])
        elif ast[1][1][0] == "DEF":
                result = stat_func_def(ast[1])
        else:
                result = stat_semicol(ast[1])

        return result

def program(ast):
        """
        Converts abstract syntax trees to intermediate code.

        Corresponds to a production.
        """

        return "\n".join([statement(e) for e in ast[1:]])

int_code_gen = program
