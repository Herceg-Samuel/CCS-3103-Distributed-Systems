from lamport_clock import LamportClock

if __name__ == "__main__":
    clock1 = LamportClock()
    clock2 = LamportClock()

    print("Simulating internal events....")
    clock1.internal_event()
    clock1.internal_event()
    # Simulate messages
    message_time1 = clock1.send_message()
    print(f"Clock1 Time after sending: {message_time1}")
    message_time2 = clock2.receive_message(message_time1)
    print(f"Clock2 Time after receiving: {message_time2}")
