from typing import Dict, Callable, List
import sys

from click import prompt, getchar as getch

from classes import FungeSpace


_command_routes: Dict[str, Callable] = {}


def _instruction(chars: str) -> Callable:
    """Instruction decorator"""

    def decorator(fn: Callable) -> Callable:
        """Wrap instruction and add to _command_routes"""

        def wrapped(space: FungeSpace) -> None:
            """Run instruction, if return value push value to stack"""
            res = fn(space)
            if res is not None:
                space.stack.push(res)

        _command_routes.update(dict.fromkeys(chars, wrapped))
        return wrapped

    return decorator


@_instruction(" ")
def _cmd_null(space: FungeSpace) -> None:
    pass


@_instruction("@")
def _cmd_stop(space: FungeSpace) -> None:
    space.running = False


@_instruction("#")
def _cmd_jump(space: FungeSpace) -> None:
    space.move()


@_instruction("0123456789")
def _cmd_push_digit(space: FungeSpace) -> int:
    return int(chr(space.val()))


@_instruction("abcdef")
def _cmd_push_hex(space: FungeSpace) -> int:
    return space.val() - 86


@_instruction("+")
def _cmd_maths_add(space: FungeSpace) -> int:
    return space.stack.pop() + space.stack.pop()


@_instruction("*")
def _cmd_maths_mul(space: FungeSpace) -> int:
    return space.stack.pop() * space.stack.pop()


@_instruction("-")
def _cmd_maths_sub(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b - a


@_instruction("/")
def _cmd_maths_div(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b // a


@_instruction("%")
def _cmd_maths_mod(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return b % a


@_instruction("!")
def _cmd_logic_not(space: FungeSpace) -> int:
    return int(not space.stack.pop())


@_instruction("`")
def _cmd_logic_gt(space: FungeSpace) -> int:
    a, b = space.stack.pop(2)
    return int(b > a)


@_instruction(":")
def _cmd_stack_dup(space: FungeSpace) -> List[int]:
    return [space.stack.pop()] * 2


@_instruction("\\")
def _cmd_stack_swp(space: FungeSpace) -> List[int]:
    return list(space.stack.pop(2))


@_instruction("$")
def _cmd_stack_pop(space: FungeSpace) -> None:
    space.stack.pop()


@_instruction("g")
def _cmd_space_get(space: FungeSpace) -> int:
    y, x = space.stack.pop(2)
    return space[x, y]


@_instruction("p")
def _cmd_space_put(space: FungeSpace) -> None:
    y, x, v = space.stack.pop(3)
    space[x, y] = v


@_instruction("^")
def _cmd_drctn_N(space: FungeSpace) -> None:
    space.ip.north()


@_instruction("v")
def _cmd_drctn_S(space: FungeSpace) -> None:
    space.ip.south()


@_instruction(">")
def _cmd_drctn_E(space: FungeSpace) -> None:
    space.ip.east()


@_instruction("<")
def _cmd_drctn_W(space: FungeSpace) -> None:
    space.ip.west()


@_instruction("[")
def _cmd_drctn_rot_left(space: FungeSpace) -> None:
    space.ip.rotate(90)


@_instruction("]")
def _cmd_drctn_rot_right(space: FungeSpace) -> None:
    space.ip.rotate(-90)


@_instruction("?")
def _cmd_drctn_rand(space: FungeSpace) -> None:
    space.ip.random()


@_instruction("_")
def _cmd_drctn_H_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.west()
    else:
        space.ip.east()


@_instruction("|")
def _cmd_drctn_V_or(space: FungeSpace) -> None:
    if space.stack.pop():
        space.ip.north()
    else:
        space.ip.south()


@_instruction(".")
def _cmd_io_out_digit(space: FungeSpace) -> None:
    sys.stdout.write(f"{space.stack.pop()} ")
    sys.stdout.flush()


@_instruction(",")
def _cmd_io_out_char(space: FungeSpace) -> None:
    sys.stdout.write(chr(space.stack.pop()))
    sys.stdout.flush()


@_instruction("&")
def _cmd_io_in_line(space: FungeSpace) -> int:
    return int(input("=>"))


@_instruction("~")
def _cmd_io_in_char(space: FungeSpace) -> int:
    sys.stdout.write(">")
    sys.stdout.flush()
    return ord(getch())


def _cmd_unknown(space: FungeSpace) -> None:
    print(f"unknown: {chr(space.val())}")
    sys.exit()


def run_instruction(char: str, space: FungeSpace) -> None:
    """Get and run instruction"""
    fn = _command_routes.get(char, _cmd_unknown)
    # print(char, fn.__name__, space.stack)
    fn(space)
