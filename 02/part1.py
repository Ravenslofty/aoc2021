from enum import Enum

from nmigen import *

# Okay, I needed to take some small liberties here.
# It doesn't make sense to parse full strings in HDL, so I'm using a direction enum instead.
class Direction(Enum):
    UP       = 0
    DOWN     = 1
    FORWARD  = 2


class Aoc02(Elaboratable):
    def __init__(self):
        self.i_dirctn = Signal(Direction)
        self.i_amount = Signal(5)

        self.o_result = Signal(32)

    def elaborate(self, platform):
        m = Module()

        hrzntl = Signal(16)
        depth  = Signal(16)

        with m.Switch(self.i_dirctn):
            with m.Case(Direction.UP):
                m.d.sync += depth.eq(depth - self.i_amount)
            with m.Case(Direction.DOWN):
                m.d.sync += depth.eq(depth + self.i_amount)
            with m.Case(Direction.FORWARD):
                m.d.sync += hrzntl.eq(hrzntl + self.i_amount)
        m.d.comb += self.o_result.eq(hrzntl * depth)

        return m


from nmigen.sim import *

aoc02 = Aoc02()
sim = Simulator(aoc02)

def example():
    with open("input") as f:
        for line in f.read().splitlines():
            direction, amount = line.split()
            if direction == "up":
                yield aoc02.i_dirctn.eq(Direction.UP)
            elif direction == "down":
                yield aoc02.i_dirctn.eq(Direction.DOWN)
            elif direction == "forward":
                yield aoc02.i_dirctn.eq(Direction.FORWARD)
            yield aoc02.i_amount.eq(int(amount))
            yield
        yield
        result = yield aoc02.o_result
        print("{}".format(result))

sim.add_sync_process(example)
sim.add_clock(1e-9)
with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run()