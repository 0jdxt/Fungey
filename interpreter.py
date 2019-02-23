#!/usr/bin/env python3
import click
from sys import stdout

from instructions import get_instruction
from classes import FungeSpace


@click.command()
@click.argument("program", type=click.File(mode="rb"))
@click.option("--raw", is_flag=True, help="Remove newline after program output.")
def main(program: click.File, raw: bool = False) -> None:
    space = FungeSpace(program.read())  # type: ignore

    # TODO: logging, commenting

    # If no state activated, continue processing of char
    # else, move to next instruction
    while space.running:
        cmd = space.val()
        char = chr(cmd)
        # print(space.ip.loc(), ":", cmd, char, end=" ")

        if space.toggle_states(char):
            # Get and run instruction. If value returned, push onto stack
            res = get_instruction(char)(space)
            if res is not None:
                space.stack.push(res)

        # print(space.stack)
        space.move()
        # print(space.ip.loc(), space.val())

    if (not raw) and stdout.isatty():
        click.echo("")


if __name__ == "__main__":
    main()
