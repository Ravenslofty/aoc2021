from nmigen import *


class Aoc01(Elaboratable):
    def __init__(self):
        self.i_sample = Signal(16)
        self.i_incr   = Signal()

        self.o_result = Signal(16)

    def elaborate(self, platform):
        m = Module()
        last1 = Signal(16)
        last2 = Signal(16)
        last3 = Signal(16)

        with m.If(((self.i_sample + last1 + last2) > (last1 + last2 + last3)) & self.i_incr):
            m.d.sync += self.o_result.eq(self.o_result + 1)

        m.d.sync += [
            last3.eq(last2),
            last2.eq(last1),
            last1.eq(self.i_sample)
        ]

        return m


from nmigen.sim import *

aoc01 = Aoc01()
sim = Simulator(aoc01)

def incr():
    yield aoc01.i_incr.eq(0)
    yield
    yield
    yield
    yield aoc01.i_incr.eq(1)
    yield

def example():
    with open("input") as f:
        for line in f.read().splitlines():
            yield aoc01.i_sample.eq(int(line))
            yield
        yield aoc01.i_incr.eq(0)
        yield
        result = yield aoc01.o_result
        print("{}".format(result))

sim.add_sync_process(incr)
sim.add_sync_process(example)
sim.add_clock(1e-9)
with sim.write_vcd("test.vcd", "test.gtkw"):
    sim.run()
