import ast.parser_gen.add_prods
import ast.parser_gen.remove_temp

NOTHING = ("___NOTHING___", "___NOTHING___")

def cache(func):
        cache_ = globals()[func.__name__ + "_cache"] = {}

        def func_(left, right, objects, prods):
                if isinstance(right, list):
                        right_ = tuple(tuple(right))
                else:
                        right_ = right
                key = (left, right_, tuple(objects))
                if key not in cache_:
                        cache_[key] = func(left, right, objects, prods)

                return cache_[key]

        return func_

@cache
def prodizer_one(left, right, tokens, prodizer):
        """
        helper function
        """

        if   (len(tokens) == 0) and (right == NOTHING[0]):
                ast = (left, NOTHING)
        elif right in prodizer:
                ast = prodizer[right](tokens, prodizer)
                if ast:
                        ast = (left, ast)
        elif (len(tokens) == 1) and (right == tokens[0][0]):
                ast = (left, tokens[0])
        else:
                ast = None

        return ast

@cache
def prodizer_list(left, right, tokens, prodizer):
        """
        helper function
        """

        ast = None
        for e in right:
                if isinstance(e, tuple):
                        ast = prodizer_tuple(left, e, tokens, prodizer)
                else:
                        ast = prodizer_one(left, e, tokens, prodizer)
                if ast:
                        break

        return ast

@cache
def prodizer_tuple(left, right, tokens, prodizer):
        """
        helper function
        """

        asts = []
        for e in right:
                if tokens:
                        for i in range(len(tokens), -1, -1):
                                ast = prodizer_one(e, e, tokens[:i], prodizer)
                                if ast:
                                        tokens = tokens[i:]
                                        break
                else:
                        ast = prodizer_one(e, e, [], prodizer)
                if ast:
                        asts.append(ast[1])
                else:
                        asts = None
                        break
        ast = (left,) + tuple(asts) if asts and not tokens else None

        return ast

def make_prodizer(left, right):
        """
        Makes productionizers.
        """

        right_ = right
        if   "|" in right_:
                right_ = [e.strip() for e in right_.split("|")]
                for i, e in enumerate(right_):
                        if " " in e:
                                right_[i] = tuple(e.split())
        elif " " in right_:
                right_ = tuple(right_.split())

        def prodizer(tokens, prodizer):
                if   isinstance(right_, list):
                        ast = prodizer_list( left, right_, tokens, prodizer)
                elif isinstance(right_, tuple):
                        ast = prodizer_tuple(left, right_, tokens, prodizer)
                else:
                        ast = prodizer_one(  left, right_, tokens, prodizer)

                return ast

        return prodizer

def parser_gen_(tokenizer, grammar):
        """
        Makes parsers.
        """

        names    = ast.parser_gen.add_prods.add_prods(grammar)
        prodizer = dict([(e, make_prodizer(e, grammar.prods[e]))
                         for e in grammar.prods])

        def parser(text):
                tokens = tokenizer.tokenizer(text)
                ast_   = prodizer[grammar.start](tokens, prodizer)
                ast_   = ast.parser_gen.remove_temp.remove_temp(ast_, names)

                return ast_

        return parser
