#!/usr/bin/env python3.7
import click
from sys import stdout

from instructions import get_instruction
from classes import FungeSpace


@click.command()
@click.argument("program", type=click.File(mode="rb"))
@click.option("--raw", is_flag=True, help="Remove newline after program output.")
def main(program: click.File, raw: bool = False) -> None:
    space = FungeSpace(program.read())  # type: ignore
    while space.running:
        cmd = space.val()
        char = chr(cmd)
        # print(space.ip.loc(), ":", cmd, char, end=" ")

        if space.toggle_states(char):
            func = get_instruction(char)
            res = func(space)
            if res is not None:
                space.stack.push(res)

        # print(space.stack)
        space.move()
        # print(space.ip.loc(), space.val())

    if (not raw) and stdout.isatty():
        click.echo("")


if __name__ == "__main__":
    main()
