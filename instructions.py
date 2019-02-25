from typing import Dict, Callable, List, Union
import sys

from click import prompt, getchar as getch

from classes import FungeSpace


def _cmd_unknown(space: FungeSpace) -> None:
    print(f"unknown: {chr(space.val())}")
    sys.exit()


def _cmd_null(space: FungeSpace) -> None:
    pass


def _cmd_stop(space: FungeSpace) -> None:
    space.running = False


def _cmd_jump(space: FungeSpace) -> None:
    space.move()


def _cmd_push_digit(space: FungeSpace) -> int:
    return int(chr(space.val()))


def _cmd_push_hex(space: FungeSpace) -> int:
    return space.val() - 86


def _cmd_maths_add(space: FungeSpace) -> int:
    return space.stack.pop() + space.stack.pop()


def _cmd_maths_mul(space: FungeSpace) -> int:
    return space.stack.pop() * space.stack.pop()


def _cmd_maths_sub(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b - a


def _cmd_maths_div(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b // a


def _cmd_maths_mod(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b % a


def _cmd_logic_not(space: FungeSpace) -> int:
    return int(not space.stack.pop())


def _cmd_logic_gt(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return int(b > a)


def _cmd_stack_dup(space: FungeSpace) -> List[int]:
    return [space.stack.pop()] * 2


def _cmd_stack_swp(space: FungeSpace) -> List[int]:
    return list(space.stack.pop(2))


def _cmd_stack_pop(space: FungeSpace) -> None:
    space.stack.pop()


def _cmd_space_get(space: FungeSpace) -> int:
    y, x = space.stack.pop(2)
    return space[x, y]


def _cmd_space_put(space: FungeSpace) -> None:
    y, x, v = space.stack.pop(3)
    space[x, y] = v


def _cmd_drctn_N(space: FungeSpace) -> None:
    space.ip.north()


def _cmd_drctn_S(space: FungeSpace) -> None:
    space.ip.south()


def _cmd_drctn_E(space: FungeSpace) -> None:
    space.ip.east()


def _cmd_drctn_W(space: FungeSpace) -> None:
    space.ip.west()


def _cmd_drctn_rot_left(space: FungeSpace) -> None:
    space.ip.rotate(90)


def _cmd_drctn_rot_right(space: FungeSpace) -> None:
    space.ip.rotate(-90)


def _cmd_drctn_rand(space: FungeSpace) -> None:
    space.ip.random()


def _cmd_drctn_H_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.west()
    else:
        space.ip.east()


def _cmd_drctn_V_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.north()
    else:
        space.ip.south()


def _cmd_io_out_digit(space: FungeSpace) -> None:
    sys.stdout.write(f"{space.stack.pop()} ")
    sys.stdout.flush()


def _cmd_io_out_char(space: FungeSpace) -> None:
    sys.stdout.write(chr(space.stack.pop()))
    sys.stdout.flush()


def _cmd_io_in_line(space: FungeSpace) -> int:
    return int(input("=>"))


def _cmd_io_in_char(space: FungeSpace) -> int:
    sys.stdout.write(">")
    sys.stdout.flush()
    return ord(getch())


_command_routes: Dict[str, Callable] = {
    # control
    " ": _cmd_null,
    "#": _cmd_jump,
    "@": _cmd_stop,
    # binary ops
    "+": _cmd_maths_add,
    "-": _cmd_maths_sub,
    "*": _cmd_maths_mul,
    "/": _cmd_maths_div,
    "%": _cmd_maths_mod,
    # logic
    "!": _cmd_logic_not,
    "`": _cmd_logic_gt,
    # stack manipulation
    ":": _cmd_stack_dup,
    "\\": _cmd_stack_swp,
    "$": _cmd_stack_pop,
    # FungeSpace manipulation
    "g": _cmd_space_get,
    "p": _cmd_space_put,
    # pointer directions
    "^": _cmd_drctn_N,
    "v": _cmd_drctn_S,
    ">": _cmd_drctn_E,
    "<": _cmd_drctn_W,
    "[": _cmd_drctn_rot_left,
    "]": _cmd_drctn_rot_right,
    "?": _cmd_drctn_rand,
    "_": _cmd_drctn_H_or,
    "|": _cmd_drctn_V_or,
    # i/o
    ".": _cmd_io_out_digit,
    ",": _cmd_io_out_char,
    "&": _cmd_io_in_line,
    "~": _cmd_io_in_char,
}
_command_routes.update(dict.fromkeys("0123456789", _cmd_push_digit))
_command_routes.update(dict.fromkeys("abcdef", _cmd_push_hex))


def run_instruction(char: str, space: FungeSpace) -> None:
    """Get and run instruction. If value returned, push onto stack"""
    res = _command_routes.get(char, _cmd_unknown)(space)
    if res is not None:
        space.stack.push(res)
