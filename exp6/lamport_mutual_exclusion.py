from lamport_clock import LamportClock
from logger import global_log, log_event


class ProcessNode(LamportClock):
    def __init__(self, pid, clock):
        super().__init__(pid)
        self.clock = clock

    def tick(self):
        self.time = max(self.time, self.clock.time) + 1
        self.clock.time = self.time
        return self.time

    def event(self, name):
        t = self.tick()
        log_event(self.process_id, name, t)
        return t

    def internal(self, n=2):
        for _ in range(n):
            self.event("Internal Event")

    def request(self):
        t = self.event("REQUEST")
        return {"process_id": self.process_id, "timestamp": t}

    def reply(self, request):
        t = self.tick()
        log_event(self.process_id, f"REPLY to {request['process_id']}", t)
        return {"process_id": self.process_id, "timestamp": t, "to": request["process_id"]}

    def release(self):
        return self.event("RELEASE")


class ResourceManager:
    def __init__(self, name):
        self.resource = name
        self.owner = None
        self.waiting = []
        self.clock = LamportClock("Global")

    def request_access(self, process):
        req = process.request()

        if not self.owner:
            process.reply(req)
            self.owner = process.process_id
            log_event(process.process_id, f"Granted {self.resource}", req["timestamp"])
            print(f"{process.process_id} gets {self.resource} at logical time {req['timestamp']}")
        else:
            self.waiting.append((process, req))
            log_event(process.process_id, "Waiting for Resource", req["timestamp"])
            print(f"{process.process_id} waits for {self.resource} at logical time {req['timestamp']}")

    def release_access(self, process):
        if self.owner != process.process_id:
            return

        process.internal()
        t = process.release()
        self.owner = None
        self.clock.time = max(self.clock.time, t) + 1

        if self.waiting:
            next_process, req = self.waiting.pop(0)
            next_process.reply(req)
            self.owner = next_process.process_id
            log_event(next_process.process_id, f"Granted {self.resource}", req["timestamp"])
            print(f"{next_process.process_id} gets {self.resource} at logical time {req['timestamp']}")

    def simulate(self, processes):
        print("Simulating Lamport mutual exclusion")
        self.request_access(processes[0])
        processes[0].internal()
        self.request_access(processes[1])
        self.request_access(processes[2])
        self.release_access(processes[0])
        self.release_access(processes[1])


if __name__ == "__main__":
    global_log.clear()

    manager = ResourceManager("Printer")
    processes = [
        ProcessNode("P1", manager.clock),
        ProcessNode("P2", manager.clock),
        ProcessNode("P3", manager.clock),
    ]

    manager.simulate(processes)

    print("\nSorted Event Log")
    global_log.sort(key=lambda event: (event["Timestamp"], event["Process ID"]))

    for event in global_log:
        print(f"Timestamp: {event['Timestamp']} | Node: {event['Process ID']} | Event: {event['Event Type']}")
