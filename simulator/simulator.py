from pathlib import Path
from lamport_clock import LamportClock


class ProcessNode:
    def __init__(self, pid):
        self.clock = LamportClock(pid)
        self.process_id = pid

    def internal_event(self, description):
        timestamp = self.clock.internal_event()
        return {"process_id": self.process_id, "event_type": "internal", "description": description, "timestamp": timestamp}

    def send_message(self, receiver, description):
        timestamp = self.clock.send_message()
        return {"process_id": self.process_id, "event_type": "message_send", "description": description, "timestamp": timestamp, "receiver": receiver.process_id}

    def receive_message(self, sender, description, received_time):
        timestamp = self.clock.receive_message(received_time)
        return {"process_id": self.process_id, "event_type": "message_receive", "description": description, "timestamp": timestamp, "sender": sender.process_id}


def run_simulation():
    p1 = ProcessNode("P1")
    p2 = ProcessNode("P2")
    p3 = ProcessNode("P3")

    events = []
    events.append(p1.internal_event("start local computation"))
    events.append(p2.internal_event("prepare to communicate"))
    events.append(p3.internal_event("idle waiting"))

    send_event = p1.send_message(p2, "send heartbeat")
    events.append(send_event)

    receive_event = p2.receive_message(p1, "receive heartbeat", send_event["timestamp"])
    events.append(receive_event)

    events.append(p2.internal_event("process received message"))
    events.append(p3.internal_event("observe state change"))

    send_event_2 = p2.send_message(p3, "forward update")
    events.append(send_event_2)

    receive_event_2 = p3.receive_message(p2, "receive update", send_event_2["timestamp"])
    events.append(receive_event_2)

    events.append(p1.internal_event("finalize state"))

    events.sort(key=lambda event: (event["timestamp"], event["process_id"]))
    timeline = build_timeline(events)
    return events, timeline


def build_timeline(events):
    lines = []
    process_ids = sorted({event["process_id"] for event in events})
    for process_id in process_ids:
        lines.append(f"{process_id}:")
        for event in events:
            if event["process_id"] == process_id:
                lines.append(f"  t={event['timestamp']} {event['event_type']} :: {event['description']}")
        lines.append("")

    lines.append("Cross-process view:")
    lines.append("  P1 -> P2: heartbeat message at t=2")
    lines.append("  P2 -> P3: update message at t=6")
    return lines


def write_outputs(events, timeline):
    output_dir = Path(__file__).resolve().parent
    log_file = output_dir / "event_log.txt"
    timeline_file = output_dir / "timeline_diagram.txt"
    analysis_file = output_dir / "performance_analysis.txt"
    reflection_file = output_dir / "reflection.txt"

    with log_file.open("w", encoding="utf-8") as handle:
        handle.write("Event Log\n")
        handle.write("========\n")
        for event in events:
            handle.write(
                f"{event['timestamp']} | {event['process_id']} | {event['event_type']} | {event['description']}\n"
            )

    with timeline_file.open("w", encoding="utf-8") as handle:
        handle.write("Timeline Diagram\n")
        handle.write("================\n")
        handle.write("\n".join(timeline))
        handle.write("\n")

    with analysis_file.open("w", encoding="utf-8") as handle:
        handle.write("Performance Analysis\n")
        handle.write("====================\n")
        handle.write("- Total events: {}\n".format(len(events)))
        handle.write("- Number of processes: 3\n")
        handle.write("- Message exchanges: 2\n")
        handle.write("- Average event timestamp: {:.2f}\n".format(sum(event["timestamp"] for event in events) / len(events)))

    with reflection_file.open("w", encoding="utf-8") as handle:
        handle.write("Reflection on Lamport Clock Limitations\n")
        handle.write("======================================\n")
        handle.write("Lamport clocks provide a simple partial ordering for distributed events, but they do not capture the full causal relationship between events in all cases. They also cannot distinguish concurrent events that share the same timestamp, and they do not provide a true global view of wall-clock time.\n")

    return log_file, timeline_file, analysis_file, reflection_file


if __name__ == "__main__":
    events, timeline = run_simulation()
    write_outputs(events, timeline)

    print("Event Log")
    print("========")
    for event in events:
        print(f"{event['timestamp']} | {event['process_id']} | {event['event_type']} | {event['description']}")

    print("\nTimeline Diagram")
    print("================")
    print("\n".join(timeline))
