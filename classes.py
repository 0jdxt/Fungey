from typing import (
    List,
    Union,
    Optional,
    Tuple,
    Callable,
    Any,
    Dict,
    overload,
    ByteString,
)
import random
import math
from collections import namedtuple
import sys


Vector = namedtuple("Vector", ("x", "y"))


class InstructionPointer:
    def __init__(self, init_vec: Vector = Vector(0, 0)) -> None:
        """Funge space instruction pointer"""
        self._pos = init_vec
        self._dirs: List[Vector] = []
        self.north = self._card_dir(Vector(0, -1))
        self.south = self._card_dir(Vector(0, 1))
        self.east = self._card_dir(Vector(1, 0))
        self.west = self._card_dir(Vector(-1, 0))
        self.east()

    def _card_dir(self, vec: Vector) -> Callable:
        """Returns a function setting the pointer's heading"""
        self._dirs.append(vec)

        def fn() -> None:
            self._delta = vec

        return fn

    def loc(self) -> Vector:
        """Return current position of pointer"""
        return self._pos

    def random(self) -> None:
        """Set pointer to random direction"""
        self._delta = random.choice(self._dirs)

    def move(self, space_data: List[bytearray]) -> None:
        """Move pointer in given direction, wraps around edges"""
        y = (self._pos.y + self._delta.y) % len(space_data)
        x = (self._pos.x + self._delta.x) % len(space_data[self._pos.y])
        self._pos = Vector(x, y)

    def rotate(self, deg: int) -> None:
        if deg % 90:
            raise ValueError("Rotation is only allowed in multiples of 90deg.")
        sT = round(math.sin(math.radians(deg)))
        cT = round(math.cos(math.radians(deg)))
        x = cT * self._pos.x - sT * self._pos.y
        y = sT * self._pos.x + cT * self._pos.y
        self._pos = Vector(x, y)


class Stack:
    def __init__(self) -> None:
        """Simple Funge stack"""
        self._data: List[int] = []

    @overload
    def pop(self) -> int:
        ...

    @overload
    def pop(self, n: int) -> Tuple[int, ...]:
        ...

    def pop(self, n: int = 1) -> Union[int, Tuple[int, ...]]:
        o: List[int] = []
        for _ in range(n):
            try:
                o.append(self._data.pop())
            except IndexError:
                o.append(0)
        return tuple(o) if len(o) > 1 else o[0]

    def push(self, *args: Union[int, List[int]]) -> None:
        for arg in args:
            if isinstance(arg, list):
                self._data.extend(arg)
            else:
                self._data.append(arg)

    def __len__(self) -> int:
        """Returns size of data"""
        return len(self._data)

    def __repr__(self) -> str:
        """Shows stack from top to bottom"""
        return f"<Stack {self._data[::-1]}>"


class StateManager:
    def __init__(self, mapping: Dict[str, Callable[[], Any]]) -> None:
        """Keeps track of special states/modes."""
        self._state = False
        self._active = ""
        self._data: Dict[str, Callable] = {}
        for char, fn in mapping.items():
            self._data[char] = fn

    def update(self, char: str) -> bool:
        # If end state found, Toggle state off
        if self._active == char:
            self._state = False
            self._active = ""
            return False

        # If state found, Toggle state on
        func = self._data.get(self._active or char)
        if func:
            if self._state:
                func()
            else:
                self._state = True
                self._active = char
            return False

        # Instruction not a state modifier
        return True


# define type for FungeSpace indexing
FSidx = Union[Vector, Tuple[int, int]]


class FungeSpace:
    def __init__(self, space: bytes) -> None:
        """Funge Space class"""
        self._data = [bytearray(x) for x in space.split(b"\n")]
        self.ip = InstructionPointer()
        self.running = True
        self.stack = Stack()

        def state_string() -> None:
            self.stack.push(self.val())

        def state_jump() -> None:
            pass

        self._state_manager = StateManager({'"': state_string, ";": state_jump})

    def toggle_states(self, char: str) -> bool:
        return self._state_manager.update(char)

    def __getitem__(self, idx: FSidx) -> int:
        """Get int value from cell in position x, y"""
        if isinstance(idx, Vector):
            self.__check_coords(idx)
            return self._data[idx.y][idx.x]

        if isinstance(idx, tuple):
            return self.__getitem__(Vector(*idx))
        raise IndexError("Index must be Vector(x, y)")

    def __setitem__(self, idx: FSidx, val: int) -> None:
        """Set cell in position x, y to int value"""
        if isinstance(idx, Vector):
            self.__check_coords(idx)
            self._data[idx.y][idx.x] = val

        elif isinstance(idx, tuple):
            self.__setitem__(Vector(*idx), val)
        else:
            raise IndexError("Index must be Vector(x, y)")

    def __check_coords(self, idx: Vector) -> None:
        """Only get and put commands can extend the space."""
        col_len = len(self._data)
        if idx.y >= col_len:
            self._data.append(bytearray(idx.y - col_len + 1))

        row_len = len(self._data[idx.y])
        if idx.x >= row_len:
            self._data[idx.y].extend([ord(" ")] * (idx.x - row_len + 1))

    def val(self) -> int:
        return self[self.ip.loc()]

    def move(self) -> None:
        self.ip.move(self._data)

    def __repr__(self) -> str:
        """Show current position of instruction pointer"""
        return "<FungeSpace [%d,%d]>" % self.ip.loc()
