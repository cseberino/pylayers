NOTHING = ("___NOTHING___", "___NOTHING___")

def remove_prods(ast, names):
        """
        Removes productions.
        """

        ast_ = []
        for e in ast:
                if isinstance(e, str):
                        ast_.append(e)
                else:
                        e = remove_prods(e, names)
                        if e[0] in names:
                                ast_ += e[1:]
                        else:
                                ast_.append(e)
        ast_ = tuple(ast_)

        return ast_

def remove_tuples(ast):
        """
        Removes tuples.
        """

        ast = list(ast)
        for i, e in enumerate(ast):
                if isinstance(e, tuple):
                        ast[i] = remove_tuples(e)
        if not isinstance(ast[0], str):
                inds = [i for i, e in enumerate(ast) if isinstance(e[0], tuple)]
                for i in reversed(inds):
                        ast = ast[:i] + list(ast[i]) + ast[i + 1:]
        ast = tuple(ast)

        return ast

def remove_nothings(ast):
        """
        Removes NOTHINGs.
        """

        ast = [e for e in ast if e != NOTHING]
        for i, e in enumerate(ast):
                if isinstance(e, tuple):
                        ast[i] = remove_nothings(e)
        ast = ast[0] if len(ast) == 1 else tuple(ast)

        return ast

def remove_temp(ast, names):
        """
        Removes the temporary elements added to the abstract syntax trees.
        """

        ast = remove_prods(ast, names)
        ast = remove_tuples(ast)
        ast = remove_nothings(ast)

        return ast
