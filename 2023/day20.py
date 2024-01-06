from __future__ import annotations

import collections
import itertools
import math
import util


class Relay:
    """Relay between the modules. This is the "brain" of it all."""

    def __init__(self):
        self.modules: dict[str, Module] = {}
        self.pulses: collections.deque[tuple[str, str, bool]] = collections.deque()
        self.pulsecounter: dict[bool, int] = {True: 0, False: 0}
        self.presscounter: int = 0

    @classmethod
    def from_input(cls, lines: util.Generator[str]) -> Relay:
        """Create a new Relay from the input `lines`."""
        relay = cls()
        for line in lines:
            name, line = line.split(" -> ")
            targets = line.split(", ")
            if name == "broadcaster":
                relay.modules[name] = Broadcaster(name, relay, targets)
            elif name.startswith("%"):
                name = name[1:]
                relay.modules[name] = FlipFlop(name, relay, targets)
            elif name.startswith("&"):
                name = name[1:]
                relay.modules[name] = Conjunction(name, relay, targets)
        for module in relay.modules.values():
            module.ready()
        return relay

    def find_sources(self, name: str) -> list[Module]:
        """Return all modules that have `name` as a target."""
        return [module for module in self.modules.values() if name in module.targets]

    def relay(self, source: str, target: str, pulse: bool):
        """Schedule a `pulse` to be sent from `source` to `target`."""
        # print(f"{source} -{'high' if pulse else 'low'}-> {target}")
        self.pulsecounter[pulse] += 1
        self.pulses.append((source, target, pulse))

    def press_button(self):
        """
        Press the button! This starts the process by sending a low pulse to the
        "broadcaster" module.
        """
        self.presscounter += 1
        self.relay("button", "broadcaster", False)
        while self.pulses:
            source, target, pulse = self.pulses.popleft()
            if target in self.modules:
                self.modules[target].receive(source, pulse)


class Module:
    """Base class for all modules."""

    def __init__(self, name: name, relay: Relay, targets: list[str]):
        self.name = name
        self.relay = relay
        self.targets = targets

    def ready(self):
        """Called when the relay of this module is ready."""
        pass

    def receive(self, source: str, pulse: bool):
        """Called when a `pulse` is received from a `source`."""
        pass

    def send(self, pulse: bool):
        """Send a `pulse` to all targets of this module."""
        for target in self.targets:
            self.relay.relay(self.name, target, pulse)


class Broadcaster(Module):
    """This module propagates any pulse received to all its targets."""

    def receive(self, source: str, pulse: bool):
        """Called when a `pulse` is received from a `source`."""
        self.send(pulse)


class FlipFlop(Module):
    """
    This module ignores high pulses and sends alternating high and low pulses
    when receiving a low pulse.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.state = False

    def receive(self, source: str, pulse: bool):
        """Called when a `pulse` is received from a `source`."""
        if pulse is False:
            self.state = not self.state
            self.send(self.state)


class Conjunction(Module):
    """
    This module remembers the pulses last received by each source. Upon
    receiving a pulse it sends a low pulse if the last received pulses were
    high, otherwise it sends a high pulse.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.memory = None
        self.firsthigh = 0

    def ready(self):
        """Called when the relay of this module is ready."""
        self.memory = {
            module.name: False for module in self.relay.find_sources(self.name)
        }

    def receive(self, source, pulse):
        """Called when a `pulse` is received from a `source`."""
        self.memory[source] = pulse
        self.send(not all(self.memory.values()))

    def send(self, pulse):
        """
        Send a `pulse` to all targets of this module. Also record the first
        high pulse sent by this module.
        """
        if pulse and self.firsthigh == 0:
            self.firsthigh = self.relay.presscounter
        super().send(pulse)


if __name__ == "__main__":
    # Part 1
    relay = Relay.from_input(util.readlines())
    for _ in range(1000):
        relay.press_button()
    print(math.prod(relay.pulsecounter.values()))

    # Part 2
    relay = Relay.from_input(util.readlines())
    name = "rx"
    # Turns out that the relevant modules to look at are the sources of the
    # source of "rx". We need to find the number of button presses required to
    # activate each of those.
    relevant = list(
        itertools.chain.from_iterable(
            relay.find_sources(sourcemodule.name)
            for sourcemodule in relay.find_sources(name)
        )
    )
    while any(module.firsthigh == 0 for module in relevant):
        relay.press_button()
    print(math.lcm(*(module.firsthigh for module in relevant)))
