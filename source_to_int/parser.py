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


Contains the parser.

Parsers covert tokens into abstract syntax trees.  Abstract syntax trees
are program encodings based on grammars.  Grammars specify valid programs in
programming languages.  Tools referred to as parser generators exist which can
automatically convert grammars into parsers.  A parser generator is used to
create this parser.
"""

import grammar
import parser_gen

parser = parser_gen.parser_gen(grammar.GRAMMAR)
