from blink.counter import UpCounter
from amaranth.back import verilog


def test_counter(sync_sim):
    dut = UpCounter(25)

    with open("up_counter.v", "w") as f:
        f.write(verilog.convert(dut, ports=[dut.en, dut.ovf]))

    def bench():
        # Disabled counter should not overflow.
        yield dut.en.eq(0)
        for _ in range(30):
            yield
            assert not (yield dut.ovf)

        # Once enabled, the counter should overflow in 25 cycles.
        yield dut.en.eq(1)
        for _ in range(25):
            yield
            assert not (yield dut.ovf)
        yield
        assert (yield dut.ovf)

        # The overflow should clear in one cycle.
        yield
        assert not (yield dut.ovf)

    sync_sim(dut, bench)
