import ast.parser_gen.parser_gen
import ast.pythonic_tokenizer
import ast.pythonic_grammar

parser_ = ast.parser_gen.parser_gen.parser_gen_(ast.pythonic_tokenizer,
                                                ast.pythonic_grammar)

def parser(program):
        return parser_(program)
