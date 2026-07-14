class LamportClock:
    """Simple implementation of Lamport's logical clock."""

    def __init__(self, pid=0):
        self.time = 0
        self.process_id = pid

    def internal_event(self):
        self.time += 1
        return self.time

    def send_message(self):
        self.time += 1
        return self.time

    def receive_message(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time
