# Fungey
*Befunge-93/98 interpreter written in Python.*

***

### Usage

`cd` into the root directory:

	$ ./interpreter.exe PROGRAM [--raw]

where `PROGRAM` is the path to a Befunge source file.

#### `--raw`
The interpeter outputs a newline after the program output if stdout is to the terminal. To keep raw output in the terminal, use the `--raw` flag. Piping and redirecting uses the raw output.

#### `--help`
Prints program help message.