import time
from typing import Optional


class PulseAccumulator:

    def __init__(self, accumulationPeriodLengthSeconds: int):
        self._accumulationPeriodLengthSeconds = accumulationPeriodLengthSeconds
        self._accumulatedPeriodPulses = 0
        self._accumulationPeriodStartSeconds = time.time()

    def accumulate(self, pulseCount: int) -> Optional[int]:
        # TODO: Should all the time.time() calls be made outside to support synchronous operations for multiple PulseAccumulators?

        # Increment period pulses
        self._accumulatedPeriodPulses += pulseCount

        # Check if accumulation period has ended
        now = time.time()
        if (now - self._accumulationPeriodStartSeconds >= self._accumulationPeriodLengthSeconds):
            # Take counter value and clear counter to start counting anew
            # TODO: This should have some thread safety features
            lastAccPeriodPulses = self._accumulatedPeriodPulses
            self._accumulatedPeriodPulses = 0
            self._accumulationPeriodStartSeconds = now

            # Make the callback with number of pulses
            return lastAccPeriodPulses
        
        # Otherwise period has not ended and we continue
        return None

