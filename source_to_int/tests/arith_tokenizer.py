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


Contains a test tokenizer.

Tokenizer is for a mathematical language.
"""

import re

regexes = {"NATURAL" : r"[0-9]+",
           "LPARENS" : r"\(",
           "RPARENS" : r"\)",
           "MULT"    : r"\*",
           "DIV"     : r"/",
           "PLUS"    : r"\+",
           "MINUS"   : r"-"}

def tokenizer(text):
        """
        tokenizer
        """

        tokens = []
        index  = 0
        while index < len(text):
                for e in regexes:
                        match = re.match(regexes[e], text[index:])
                        if match:
                                tokens.append((e, match.group(0)))
                                index += len(match.group(0))
                                break

        return tokens
