from nmigen import *


class Aoc01(Elaboratable):
    def __init__(self):
        self.i_sample = Signal(16)
        self.i_incr   = Signal()

        self.o_result = Signal(16)

    def elaborate(self, platform):
        m = Module()
        last = Signal(16)

        with m.If((self.i_sample > last) & self.i_incr):
            m.d.sync += self.o_result.eq(self.o_result + 1)

        m.d.sync += last.eq(self.i_sample)

        return m


from nmigen.sim import *

aoc01 = Aoc01()
sim = Simulator(aoc01)

def incr():
    yield aoc01.i_incr.eq(0)
    yield
    yield aoc01.i_incr.eq(1)
    yield

def example():
    with open("input") as f:
        for line in f.read().splitlines():
            yield aoc01.i_sample.eq(int(line))
            yield
        yield
        result = yield aoc01.o_result
        print("{}".format(result))

sim.add_sync_process(incr)
sim.add_sync_process(example)
sim.add_clock(1e-9)
sim.run()
