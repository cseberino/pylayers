import sys
import os

BASE_FOL = os.path.dirname(os.path.abspath(__file__))
sys.path.append(f"{BASE_FOL}/../interpreter")
with open(f"{BASE_FOL}/../interpreter/interpreter") as f:
        with open("__interpreter__.py", "w") as g:
                interpreter_ = f.readlines()
                g.write("".join(interpreter_[:63] + interpreter_[67:-4]))
import __interpreter__ as interpreter
os.remove("__interpreter__.py")

tokenizer = interpreter.tokenizer
parser    = interpreter.parser
