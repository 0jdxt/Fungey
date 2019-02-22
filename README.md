# Fungey
Befunge-93/98 interpreter written in Python.*

*98 is only partially supported. Check [instructions.py](https://github.com/0jdxt/Fungey/blob/6842928c16b1599f43c6b35bbe958a20909f5217/instructions.py#L150) for available commands.*

***

### Usage

`cd` into the root directory:

	$ ./interpreter.exe PROGRAM [--raw]

where `PROGRAM` is the path to a Befunge source file.

#### `--raw`
The interpeter outputs a newline after the program output if stdout is to the terminal. To keep raw output in the terminal, use the `--raw` flag. Piping and redirecting uses the raw output.

#### `--help`
Prints program help message.