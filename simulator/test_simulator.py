import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from lamport_clock import LamportClock
from simulator import run_simulation


class SimulatorTests(unittest.TestCase):
    def test_lamport_clock_updates(self):
        clock1 = LamportClock("P1")
        clock2 = LamportClock("P2")

        self.assertEqual(clock1.internal_event(), 1)
        self.assertEqual(clock2.internal_event(), 1)
        self.assertEqual(clock1.send_message(), 2)
        self.assertEqual(clock2.receive_message(2), 3)

    def test_simulation_generates_expected_outputs(self):
        events, timeline = run_simulation()
        self.assertGreaterEqual(len(events), 8)
        self.assertIn("P1", {event["process_id"] for event in events})
        self.assertIn("P2", {event["process_id"] for event in events})
        self.assertIn("P3", {event["process_id"] for event in events})
        self.assertTrue(any(event["event_type"] == "message_send" for event in events))
        self.assertTrue(any(event["event_type"] == "message_receive" for event in events))
        self.assertTrue(any("P1" in line and "P2" in line for line in timeline))


if __name__ == "__main__":
    unittest.main()
