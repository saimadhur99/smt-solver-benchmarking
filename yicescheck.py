import os
from ctypes import CDLL

# Path to the libyices.dll file using a raw string to handle backslashes correctly
dll_path = r"C:\\Users\\Sai Madhur\\Downloads\\yices-2.6.4-x86_64-pc-mingw32-static-gmp\\yices-2.6.4\bin\\libyices.dll"

# Load the DLL using its full path
libyices = CDLL(dll_path)

# Now import yices
from yices import *

cfg = Config()
cfg.default_config_for_logic('QF_LRA')
ctx = Context(cfg)

real_t = Types.real_type()
x = Terms.new_uninterpreted_term(real_t, 'x')
y = Terms.new_uninterpreted_term(real_t, 'y')

fmla0 = Terms.parse_term('(> (+ x y) 0)')
fmla1 = Terms.parse_term('(or (< x 0) (< y 0))')

ctx.assert_formulas([fmla0, fmla1])

status = ctx.check_context()

if status == Status.SAT:
    model = Model.from_context(ctx, 1)
    model_string = model.to_string(80, 100, 0)
    print(model_string)
    xval = model.get_value(x)
    yval = model.get_value(y)
    print('x = {0}, y = {1}'.format(xval, yval))
