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


Contains the parser generator.

Does all the pattern matching required to adhere to all the production rules of
grammars to create abstract syntax trees.  The types of parsers created are
referred to as recursive descent parsers.  The strategy used first replaces
complex productions with multiple simpler productions in the given grammars.
Parsers are then created for the modified grammars.  Final parsers are then
created that modify the abstract syntax tree outputs to correspond to the
original grammars.
"""

import hashlib
import re

PROD_DEF_RE   = r"(.*?(?=\n\w)|.*)"
PROD_OPT_RE   = r"\[[^\[\]]*\]"
PROD_GROUP_RE = r"\([^()]*\)"
PROD_STAR_RE  = r"\w+\*"
PROD_PLUS_RE  = r"\w+\+"
NEW_PROD_RE   = r"__\w{40}__"
NEW_TOKEN     = ("__NEW_TOKEN__", "")

def remove_new_tokens(ast):
        """
        Removes new tokens.

        Called recursively.  Lists are required to allow modifications.
        """

        ast = [e for e in ast if e != NEW_TOKEN]
        for i, e in enumerate(ast):
                if isinstance(e, tuple):
                        ast[i] = remove_new_tokens(e)
        ast = tuple(ast)

        return ast

def remove_new_prods(ast):
        """
        Removes new productions.

        Called recursively.  Lists are required to allow modifications.
        """

        ast_ = []
        for e in ast:
                if isinstance(e, str):
                        ast_.append(e)
                else:
                        e_ = remove_new_prods(e)
                        if re.match(NEW_PROD_RE, e_[0]):
                                ast_ += e_[1:]
                        else:
                                ast_.append(e_)
        ast_ = tuple(ast_)

        return ast_

def remove_new(ast):
        """
        Removes new tokens and productions.

        Separate functions are required because they must be called recursively.
        """

        return remove_new_prods(remove_new_tokens(ast))

def add_new_(old_def, grammar_):
        """
        add_new helper function

        [a]         corresponds to: new_prod : a | NEW_TOKEN.
        (a | b | c) corresponds to: new_prod : a | b | c.
        a*          corresponds to: new_prod : a new_prod | NEW_TOKEN.
        a+          corresponds to: new_prod : a new_prod | A.
        """

        new_prod = f"__{hashlib.sha1(old_def.encode()).hexdigest()}__"
        for e in grammar_:
                grammar_[e] = grammar_[e].replace(old_def, new_prod)
        if   re.match(PROD_OPT_RE,   old_def):
                new_def = f"{old_def[1:-1]} | __NEW_TOKEN__"
        elif re.match(PROD_GROUP_RE, old_def):
                new_def = old_def[1:-1]
        elif re.match(PROD_STAR_RE,  old_def):
                new_def = f"{old_def[:-1]} {new_prod} | __NEW_TOKEN__"
        elif re.match(PROD_PLUS_RE,  old_def):
                new_def = f"{old_def[:-1]} {new_prod} | {old_def[:-1]}"
        grammar_[new_prod] = new_def

def add_new(grammar_):
        """
        Adds new productions and their definitions based on old definitions.

        The inner for loop restarts after every regex match until none are prod.
        """

        for e in [PROD_OPT_RE, PROD_GROUP_RE, PROD_STAR_RE, PROD_PLUS_RE]:
                match = True
                while match:
                        for prod in grammar_:
                                match = re.search(e, grammar_[prod])
                                if match:
                                        add_new_(match.group(0), grammar_)
                                        break

def cache(func):
        """
        caching decorator

        Avoids repeating the same parser function invocations.
        """

        cache_ = globals()[func.__name__ + "_cache"] = {}

        def func_(prod, prod_def, tokens, parser_):
                key = (prod, prod_def, tuple(tokens))
                if isinstance(prod_def, list):
                        key = (prod, tuple(tuple(prod_def)), tuple(tokens))
                if key not in cache_:
                        cache_[key] = func(prod, prod_def, tokens, parser_)

                return cache_[key]

        return func_

@cache
def parser_func_sing(prod, prod_def, tokens, parser_):
        """
        Creates productions from tokens.

        For production definitions composed of one element.
        """

        if   (len(tokens) == 0) and (prod_def == NEW_TOKEN[0]):
                prod_ = (prod, NEW_TOKEN)
        elif (len(tokens) == 1) and (prod_def == tokens[0][0]):
                prod_ = (prod, tokens[0])
        elif prod_def in parser_:
                prod_ = parser_[prod_def](tokens, parser_)
                prod_ = (prod, prod_) if prod_ else None
        else:
                prod_ = None

        return prod_

@cache
def parser_func_or(prod, prod_def, tokens, parser_):
        """
        Creates productions from tokens.

        For production defintions composed of logical ORs.
        """

        prod_ = None
        for e in prod_def:
                if isinstance(e, tuple):
                        prod_ = parser_func_and(prod, e, tokens, parser_)
                else:
                        prod_ = parser_func_sing(prod, e, tokens, parser_)
                if prod_:
                        break

        return prod_

@cache
def parser_func_and(prod, prod_def, tokens, parser_):
        """
        Creates productions from tokens.

        For production defintions composed of logical ANDs.  Modifies tokens.
        """

        prods = []
        for e in prod_def:
                if tokens:
                        for i in range(len(tokens), -1, -1):
                                args  = (e, e, tokens[:i], parser_)
                                prod_ = parser_func_sing(*args)
                                if prod_:
                                        tokens = tokens[i:]
                                        break
                else:
                        prod_ = parser_func_sing(e, e, [], parser_)
                if prod_:
                        prods.append(prod_[1])
                else:
                        prods = None
                        break
        prod_ = tuple([prod] + prods) if prods and not tokens else None

        return prod_

def parser_gen_(prod, prod_def):
        """
        parser_gen helper function

        Creates parser functions.
        """

        if   "|" in prod_def:
                prod_def = [e.strip() for e in prod_def.split("|")]
                for i, e in enumerate(prod_def):
                        prod_def[i] = tuple(e.split()) if " " in e else e
        elif " " in prod_def:
                prod_def = tuple(prod_def.split())

        def parser_func(tokens, parser_):
                args = (prod, prod_def, tokens, parser_)
                if   isinstance(prod_def, list):
                        prod_ = parser_func_or(*args)
                elif isinstance(prod_def, tuple):
                        prod_ = parser_func_and(*args)
                else:
                        prod_ = parser_func_sing(*args)

                return prod_

        return parser_func

def parser_gen(grammar):
        """
        Creates and returns parsers based on grammars.

        Grammars are converted to equivalent dictionaries and then modified.
        """

        grammar_ = re.findall(PROD_DEF_RE, grammar, re.DOTALL)
        grammar_ = [e.split(":") for e in grammar_ if e]
        grammar_ = dict([(e[0].strip(), e[1].strip()) for e in grammar_])
        add_new(grammar_)
        parser_  = dict([(e, parser_gen_(e, grammar_[e])) for e in grammar_])

        return lambda e: remove_new(parser_["program"](e, parser_))
