"""Transmission signal utility: models dynamic cost/utility of transmissions."""
import math
import time


class TransmissionSignalUtility:
    """Manage message counts and calculate transmission cost.

    The cost function is illustrative: a logarithmic factor times squared
    message_count to introduce diminishing/accelerating cost behavior.
    """
    def __init__(self):
        self.message_count = 0
        self.last_transmission_time = time.time()

    def calculate_cost(self) -> float:
        time_since_last = time.time() - self.last_transmission_time
        if self.message_count == 0:
            return 1.0
        return math.log(self.message_count + 1) * (self.message_count ** 2) / max(1.0, time_since_last)

    def transmit(self) -> float:
        cost = self.calculate_cost()
        self.message_count += 1
        self.last_transmission_time = time.time()
        return cost


def example():
    util = TransmissionSignalUtility()
    for _ in range(5):
        print("Cost:", util.transmit())


if __name__ == "__main__":
    example()
