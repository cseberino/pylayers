HEADER = \
"""
# ==============================================================================
# header:
# ==============================================================================

              # Put encoding exp header in r1.

              copy  EXP_CUR,    r1
              load  r1,         r1
              load  r1,         r1

              # Stop if zero.

              copy  0x0,        r2
              copy  cont,       r3
              gjump r1,         r2, r3
              stop

              # Det path by if bool, int or str (0xc0000000 && [r1] = 0).

cont:         copy  0xc0000000, r2
              and   r1,         r2, r2
              copy  b_i_or_s,   r3
              zjump r2,         r3

not_b_i_or_s: stop

              # Update EXP_CUR

b_i_or_s:     copy  0x0fffffff, r2
              and   r1,         r2, r2         # r2 has value to add.
              copy  EXP_CUR,    r1
              load  r1,         r1             # r1 has old EXP_CUR add.
              add   r1,         r2, r1         # r1 has new EXP_CUR add.
              copy  EXP_CUR     r2
              store r1,         r2

              # Repeat everything.

              copy  0x0,        ip

# ==============================================================================
# encoded expressions:
# ==============================================================================

"""
