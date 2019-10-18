#!/usr/bin/env python3
import click
from sys import stdout

from instructions import run_instruction
from classes import FungeSpace


@click.command()
@click.argument("program", type=click.File(mode="rb"))
@click.option("--raw", is_flag=True, help="Remove newline after program output.")
def main(program: click.File, raw: bool = False) -> None:
    space = FungeSpace(program.read())  # type: ignore

    # TODO: logging, commenting

    # If no state activated, continue processing of char
    # else, move to next cell
    while space.running:
        cmd = space.val()
        char = chr(cmd)

        if space.toggle_states(char):
            run_instruction(char, space)

        space.move()

    # output newline to terminal unless --raw
    if (not raw) and stdout.isatty():
        click.echo("")


if __name__ == "__main__":
    main()
