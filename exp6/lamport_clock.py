# Lamport's Logical Clock
class LamportClock:
    process_id = None

    def __init__(self, pid=0):
        self.time = 0
        self.process_id = pid

    def send_message(self):
        self.time += 1
        return self.time

    def receive_message(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time

    def internal_event(self):
        self.time += 1
        return self.time


if __name__ == "__main__":
    # Example usage
    clock1 = LamportClock()
    clock2 = LamportClock()
    # Simulate messages
    message_time1 = clock1.send_message()
    print(f"Clock1 Time after sending: {message_time1}")
    message_time2 = clock2.receive_message(message_time1)
    print(f"Clock2 Time after receiving: {message_time2}")
