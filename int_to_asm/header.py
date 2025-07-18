HEADER = \
"""
# ==============================================================================
# header:
# ==============================================================================

              # Puts encoded exp header in r1.

              copy  EXP_CUR    r1
              load  r1         r1
              load  r1         r1

              # Stops if zero.

              copy  0x0        r2
              copy  cont       r3
              gjump r1         r2 r3
              stop

              # Stored constants.

const_1:      0xc0000000
const_2:      0x0fffffff
const_3:      0xf0000000

              # Path depends on if non_var atom exp (0xc0000000 && [r1] = 0).

              # r2 0xc0000000 then has piece of exp header.

cont:         copy  const_1    r2
              load  r2         r2
              and   r1         r2 r2
              copy  b_i_or_s   r3
              zjump r2         r3

              # path when not non_var atom exp

              # r2 0xf0000000 then has exp type.

not_b_i_or_s: copy  const_3    r2
              load  r2         r2
              and   r1         r2 r2
              copy  0x4        r3
              copy  not_atom   r4
              gjump r2         r3 r4

var:          stop

              # r2 has 0x0fffffff then has exp length.

not_atom:     copy  const_2    r2
              load  r2         r2
              and   r1         r2 r2
              copy  0x4        r3
              copy  not_empty  r4
              gjump r2         r3 r4

empty:        stop

not_empty:    stop

              # path when non_var atom exp

              # r2 0x0fffffff then length in bytes then what to add.
              # r3 has length in bytes mod 4 and used to det what to add.
              # r1 has old EXP_CUR then new EXP_CUR.
              # Will repeat until header is 0x0.

b_i_or_s:     copy  const_2    r2
              load  r2         r2
              and   r1         r2 r2
              copy  0x3        r3
              and   r2         r3 r3
              copy  0x4        r4
              sub   r4         r3 r3
              add   r2         r3 r2
              copy  EXP_CUR    r1
              load  r1         r1
              add   r1         r2 r1
              copy  EXP_CUR    r2
              store r1         r2
              copy  0x0        r1
              zjump r1         r1

# ==============================================================================
# encoded expressions:
# ==============================================================================

"""
