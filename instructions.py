from typing import Dict, Callable, List
import sys

from click import prompt, getchar as getch

from classes import FungeSpace


def cmd_unknown(space: FungeSpace) -> None:
    print(f"unknown: {chr(space.val())}")
    sys.exit()


def cmd_null(space: FungeSpace) -> None:
    pass


def cmd_stop(space: FungeSpace) -> None:
    space.running = False


def cmd_jump(space: FungeSpace) -> None:
    space.move()


def cmd_push_digit(space: FungeSpace) -> int:
    return int(chr(space.val()))


def cmd_push_hex(space: FungeSpace) -> int:
    return space.val() - 86


def cmd_maths_add(space: FungeSpace) -> int:
    return space.stack.pop() + space.stack.pop()


def cmd_maths_mul(space: FungeSpace) -> int:
    return space.stack.pop() * space.stack.pop()


def cmd_maths_sub(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b - a


def cmd_maths_div(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b // a


def cmd_maths_mod(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b % a


def cmd_logic_not(space: FungeSpace) -> int:
    return int(not space.stack.pop())


def cmd_logic_gt(space: FungeSpace) -> int:
    a, b = space.stack.pop(), space.stack.pop()
    return int(b > a)


def cmd_stack_dup(space: FungeSpace) -> List[int]:
    return [space.stack.pop()] * 2


def cmd_stack_swp(space: FungeSpace) -> List[int]:
    return list(space.stack.pop(2))


def cmd_stack_pop(space: FungeSpace) -> None:
    space.stack.pop()


def cmd_space_get(space: FungeSpace) -> int:
    y, x = space.stack.pop(2)
    return space[x, y]


def cmd_space_put(space: FungeSpace) -> None:
    y, x, v = space.stack.pop(3)
    space[x, y] = v


def cmd_drctn_N(space: FungeSpace) -> None:
    space.ip.north()


def cmd_drctn_S(space: FungeSpace) -> None:
    space.ip.south()


def cmd_drctn_E(space: FungeSpace) -> None:
    space.ip.east()


def cmd_drctn_W(space: FungeSpace) -> None:
    space.ip.west()


def cmd_drctn_rot_left(space: FungeSpace) -> None:
    space.ip.rotate(90)


def cmd_drctn_rot_right(space: FungeSpace) -> None:
    space.ip.rotate(-90)


def cmd_drctn_rand(space: FungeSpace) -> None:
    space.ip.random()


def cmd_drctn_H_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.west()
    else:
        space.ip.east()


def cmd_drctn_V_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.north()
    else:
        space.ip.south()


def cmd_io_out_digit(space: FungeSpace) -> None:
    sys.stdout.write(f"{space.stack.pop()} ")
    sys.stdout.flush()


def cmd_io_out_char(space: FungeSpace) -> None:
    sys.stdout.write(chr(space.stack.pop()))
    sys.stdout.flush()


def cmd_io_in_line(space: FungeSpace) -> int:
    return int(input("=>"))


def cmd_io_in_char(space: FungeSpace) -> int:
    sys.stdout.write(">")
    sys.stdout.flush()
    return ord(getch())


command_routes: Dict[str, Callable] = {
    # control
    " ": cmd_null,
    "#": cmd_jump,
    "@": cmd_stop,
    # binary ops
    "+": cmd_maths_add,
    "-": cmd_maths_sub,
    "*": cmd_maths_mul,
    "/": cmd_maths_div,
    "%": cmd_maths_mod,
    # logic
    "!": cmd_logic_not,
    "`": cmd_logic_gt,
    # stack manipulation
    ":": cmd_stack_dup,
    "\\": cmd_stack_swp,
    "$": cmd_stack_pop,
    # FungeSpace manipulation
    "g": cmd_space_get,
    "p": cmd_space_put,
    # pointer directions
    "^": cmd_drctn_N,
    "v": cmd_drctn_S,
    ">": cmd_drctn_E,
    "<": cmd_drctn_W,
    "[": cmd_drctn_rot_left,
    "]": cmd_drctn_rot_right,
    "?": cmd_drctn_rand,
    "_": cmd_drctn_H_or,
    "|": cmd_drctn_V_or,
    # i/o
    ".": cmd_io_out_digit,
    ",": cmd_io_out_char,
    "&": cmd_io_in_line,
    "~": cmd_io_in_char,
}
command_routes.update(dict.fromkeys("0123456789", cmd_push_digit))
command_routes.update(dict.fromkeys("abcdef", cmd_push_hex))


def get_instruction(char: str) -> Callable:
    return command_routes.get(char, cmd_unknown)
