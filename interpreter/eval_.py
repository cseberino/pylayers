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


Contains the evaluator.

Evaluates expressions.
"""

import types

FUNC = types.FunctionType

def is_var(exp):
        """
        Identifies variables.

        Variables are represented internally by tuples.
        """

        return isinstance(exp, tuple)

def is_atom(exp):
        """
        Identifies atoms.

        Functions and macros are represented internally by Python functions.
        """

        return isinstance(exp, (bool, int, str, FUNC)) or is_var(exp)

def is_list(exp):
        """
        Identifies lists.

        List are represented internally by Python lists.
        """

        return isinstance(exp, list)

def prep_args(func):
        """
        Adds argument evaluation to functions.

        Used by all functions except for quote, if, set, func and macro.
        """

        def func_(args, env):
                return func([eval_(e, env) for e in args], env)

        return func_

def eval_quote(args, env):
        """
        Implements the quote function.

        Does not evalute arguments.
        """

        return args[0]

def eval_if(args, env):
        """
        Implements the if function.

        Evaluates one of two expressions based on a condition.
        """

        if eval_(args[0], env):
                result = eval_(args[1], env)
        else:
                result = eval_(args[2], env)

        return result

def eval_set(args, env):
        """
        Implements the set function.

        Adds to environments.  Returns the values added to environments.
        """

        env[args[0]] = eval_(args[1], env)

        return env[args[0]]

def eval_func(args, env):
        """
        Implements the func function.

        Returns functions.  Special environments are used.
        """

        @prep_args
        def func(args_, env_, params = args[0], body = args[1:]):
                if is_var(params):
                        params, args_ = [params], [args_]
                env__ = env | dict(zip(params, args_))
                for e in body:
                        result = eval_(e, env__)

                return result

        return func

def eval_macro(args, env):
        """
        Implements the macro function.

        Returns macros.  Macros require two evaluations for every body
        expression.  Special environments are used.
        """

        def macro(args_, env_, params = args[0], body = args[1:]):
                if is_var(params):
                        params, args_ = [params], [args_]
                env__  = env | dict(zip(params, args_))
                for e in body:
                        result = eval_(eval_(e, env__), env_)

                return result

        return macro

@prep_args
def eval_equal(args, env):
        """
        Implements the equal function.

        Operates on more than numbers.
        """

        return args[0] == args[1]

@prep_args
def eval_atom(args, env):
        """
        Implements the atom function.

        Returns a boolean denoting whether the argument is an atom.
        """

        return is_atom(args[0])

@prep_args
def eval_first(args, env):
        """
        Implements the first function.

        Returns the first element or an empty list.
        """

        return args[0][0] if args[0] else []

@prep_args
def eval_rest(args, env):
        """
        Implements the rest function.

        Returns lists with the first element removed.
        """

        return args[0][1:]

@prep_args
def eval_append(args, env):
        """
        Implements the append function.

        Appends to lists.
        """

        return args[0] + [args[1]]

@prep_args
def eval_add(args, env):
        """
        Implements the addition function.

        Only operates on numbers.
        """

        return args[0] + args[1]

@prep_args
def eval_negate(args, env):
        """
        Implements the negation function.

        Only operates on numbers.
        """

        return -args[0]

@prep_args
def eval_gt(args, env):
        """
        Implements the greater than function.

        Only operates on numbers.
        """

        return args[0] > args[1]

@prep_args
def eval_print(args, env):
        """
        Implements the print function.

        Prints string representations of expressions and returns expressions.
        """

        def exp_str(exp):
                exp_ = str(exp)
                if   isinstance(exp, str):
                        exp_ = f'"{exp}"'
                elif isinstance(exp, tuple):
                        exp_ = exp[0]
                elif isinstance(exp, list):
                        exp_ = f"({' '.join([exp_str(e) for e in exp])})"

                return exp_

        print(exp_str(args[0]))

        return args[0]

def eval_(exp, env):
        """
        Implements the evaluator.

        Results depend on whether expressions are atoms or lists.
        """

        if   is_atom(exp):
                result = env[exp] if is_var(exp) else exp
        elif is_list(exp):
                result = eval_(exp[0], env)(exp[1:], env) if exp else []

        return result
