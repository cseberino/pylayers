import hashlib
import re

star_comp = "\w+\*"
plus_comp = "\w+\+"

def find_optional(text):
        """
        Finds optionals.
        """

        beg = text.find("[")
        end = text.find("]", beg) + 1
        while "[" in text[beg + 1:end - 1]:
                beg = text.find("[", beg + 1)

        return text[beg:end]

def find_group(text):
        """
        Finds groups.
        """

        beg = text.find("(")
        end = text.find(")", beg) + 1
        while "(" in text[beg + 1:end - 1]:
                beg = text.find("(", beg + 1)

        return text[beg:end]

def replace_comp(right_comp, grammar):
        """
        Replaces right components with new productions and returns their names.
        """

        name = hashlib.sha1(right_comp.encode()).hexdigest()
        for e in grammar.prods:
                grammar.prods[e] = grammar.prods[e].replace(right_comp, name)

        return name

def add_prod_optional(name, match, grammar):
        """
        "[A]"            leads to "<name> : A | NOTHING".
        """

        grammar.prods[name] = match[1:-1] + " | ___NOTHING___"

def add_prod_group(name, match, grammar):
        """
        "(A | B | ... )" leads to "<name> : A | B | ...".
        """

        grammar.prods[name] = match[1:-1]

def add_prod_star(name, match, grammar):
        """
        "A*"             leads to "<name> : A <name> | NOTHING".
        """

        grammar.prods[name] = match[:-1] + " " + name + " | ___NOTHING___"

def add_prod_plus(name, match, grammar):
        """
        "A+"             leads to "<name> : A <name> | A".
        """

        grammar.prods[name] = match[:-1] + " " + name + " | " + match[:-1]

def add_prods_(regex_or_func, add_prod, grammar):
        """
        helper function
        """

        names = []
        match = True
        while match:
                for e in grammar.prods:
                        if isinstance(regex_or_func, str):
                                match = re.search(regex_or_func,
                                                  grammar.prods[e])
                        else:
                                match = regex_or_func(grammar.prods[e])
                        if match:
                                if not isinstance(match, str):
                                        match = match.group(0)
                                names.append(replace_comp(match, grammar))
                                add_prod(names[-1], match, grammar)
                                break

        return names

def add_prods(grammar):
        """
        Adds productions to simplify the right sides and returns their names.
        """

        names  = []
        names += add_prods_(find_optional, add_prod_optional, grammar)
        names += add_prods_(find_group,    add_prod_group,    grammar)
        names += add_prods_(star_comp,     add_prod_star,     grammar)
        names += add_prods_(plus_comp,     add_prod_plus,     grammar)

        return names
