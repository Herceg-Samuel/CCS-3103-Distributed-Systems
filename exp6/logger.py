from lamport_clock import LamportClock
# A global list acting as our database or central logger
global_log = []


def log_event(process_id, event_type, timestamp):
    """Helper function to format and record events to the logger."""
    event = {
        "Process ID": process_id,
        "Event Type": event_type,
        "Timestamp": timestamp
    }
    global_log.append(event)


if __name__ == "__main__":
    # Setup processes
    p1 = LamportClock("P1")
    p2 = LamportClock("P2")

    # Simulating a sequence of distributed steps
    t = p1.internal_event()
    log_event(p1.process_id, "Internal Task", t)

    t = p2.internal_event()
    log_event(p2.process_id, "Internal Task", t)

    # P1 sends to P2
    msg_t = p1.send_message()
    log_event(p1.process_id, "Sent Message to P2", msg_t)

    recv_t = p2.receive_message(msg_t)
    log_event(p2.process_id, "Received Message from P1", recv_t)

    print(" Unsorted Logs \n\n")
    for log in global_log:
        print(f"[{log['Process ID']}] Type: {
              log['Event Type']:<25} | Timestamp: {log['Timestamp']}")

    print("\n Sorted Logs\n\n")
    # Sort using the 'Timestamp' key, breaking ties with the 'Process ID' key string
    global_log.sort(key=lambda x: (x["Timestamp"], x["Process ID"]))

    for log in global_log:
        print(f"Timestamp: {log['Timestamp']} | Node: {
              log['Process ID']} | Event: {log['Event Type']}")
